# poc/improved-flow
# Conversational flow: streaming speech, holding phrases, echo cancellation, barge-in

> **Status:** 🧪 POC on branch `poc/improved-flow` (`kt-kiosk-agent`,
> `kitchntabs-backend-domain`, `vanexa-backend-domain`). Every feature is behind a
> flag and **off by default** — a device that upgrades and changes nothing behaves
> exactly as it did before. Not yet validated on real kiosk hardware; see
> [Not done](#not-done--known-gaps).
> **Layers:** the audio work is entirely in `kt-kiosk-agent`; the domain repos add
> one job and the settings schema. **`dash-backend` core needed no changes.**
> **Related:** [AI Tenant Settings](AI-TENANT-SETTINGS.md) ·
> [Kiosk Agent Backend](KIOSK-AGENT-BACKEND.md) ·
> [Python Kiosk Self-Service Voice](PYTHON-KIOSK-SELF-SERVICE-VOICE.md)

---

## 1. The problem

The kiosk spoke **once**, at the very end of a turn. `TenantAssistant._on_run_finished()`
waited for `RUN_FINISHED`, took the whole assembled reply, and synthesised one clip. So a
customer finishing their question stood in silence through a full model generation *plus*
every tool round-trip (`search_menu` → `show_products`) before hearing a word — then got a
wall of speech.

They also could not interrupt. `mute_while_speaking` substituted digital silence for the
whole clip, so the microphone was deaf exactly while the character talked.

This POC attacks both, in four independent layers:

| Layer | Flag | What it buys |
|---|---|---|
| Streaming speech | `VOICE_PIPELINE` | Character starts talking mid-generation instead of after it |
| Holding phrase | `FILLER_MODE` | Covers the silence that remains before sentence one |
| Echo cancellation | `AEC_BACKEND` | Removes the kiosk's own voice from its microphone |
| Barge-in | `BARGE_IN_ENABLED` | Customer can talk over the character and cut it off |

---

## 2. Two things that made this cheaper than expected

**The sentence splitter already existed and was switched off.** `split_flushable()`
(`pw/vanexa/agent_stream.py`) and the `on_speak` → `_speak_chunk` wiring have been in the
tree, tested, all along. What kept them disabled was a comment in
`pw/kitchntabs/tenant_assistant.py` naming the real blocker: `AudioPlayer` cancelled
whatever was playing the instant a new clip was requested, so a multi-sentence reply
cancelled itself down to its last sentence. Fixing the audio player unlocked the rest.

**`send_message_simple()` was fully built and never called** — a tool-less,
single-Bedrock-call endpoint. It ultimately wasn't used (see §4), but it proved the shape
was already understood.

---

## 3. Streaming speech (`VOICE_PIPELINE`)

```yaml
VOICE_PIPELINE: "classic"    # classic | streaming
```

- **`classic`** — assemble the whole turn, speak it as one clip at `RUN_FINISHED`. The
  default, byte-for-byte the old path.
- **`streaming`** — queue each sentence as it completes.

### 3.1 The audio queue, and why it had to come first

`AudioPlayer._dispatch_generate_audio()` did this on **every** request:

```python
if self.current_thread and self.current_thread.is_alive():
    self.stop_audio(); self.current_thread.join()
```

Correct for the SKIP interrupt, fatal for a reply arriving as several sentences. It was
replaced with **one playback owner**: a long-lived play worker is now the only thing that
touches PyAudio, fed by a prep worker that synthesises ahead. Cancel-and-replace stopped
being a property of dispatch and became one of two queue policies:

| Call | Policy |
|---|---|
| `thread_generate_audio()` | cancel, append, seal — **unchanged semantics**, so SKIP, error lines and the welcome clip still pre-empt |
| `enqueue_audio()` | append, play back to back |
| `seal_queue()` | declare the batch complete |
| `cancel_queue()` | drop everything and cut what is playing |

**Cancellation is by generation counter**, not by interrupting work in flight: a synthesis
request that lands after a cancel finds its item stale and is discarded, so an ElevenLabs
call never has to be aborted mid-request.

**`PREP_AHEAD = 1`, and the reason is money, not memory.** ElevenLabs bills per synthesis;
preparing a whole six-sentence reply up front pays for six clips when a customer who
interrupts after the first hears one. One ahead still hides the synthesis round-trip in the
gap between sentences.

### 3.2 Three things the queue broke, and how they were fixed

| Was | Problem | Fix |
|---|---|---|
| `audio/pitched_audio.wav` | ONE shared scratch path for every clip — safe only while one clip could exist | Clips render to memory (`_render_pcm`). Serialisation goes through an in-memory WAV via `soundfile`, the *same libsndfile path* the disk version used, so bytes are provably identical — a hand-rolled `* 32767` cast is **not** equivalent and differs on every non-silent input |
| `speech_progress()` / `time_remaining()` | Described only the current clip: progress would run 0→1 three times per reply (revealing the whole subtitle during sentence one) and report ~0s remaining three times (unmuting the mic between sentences) | Both read a single immutable snapshot tuple spanning the **batch**. Progress is monotonic, because `batch_total` grows as sentences arrive and the raw fraction would make the subtitle *retract* text already heard |
| `audio_playing` per clip | Would flicker once per sentence, chattering the subtitle hold, character zoom, salute suppression and the mute gate | Set once per batch, cleared on drain |

`audio_playing` is also an **external kill switch** (`_close_conversation`, SKIP clear it
directly). When the write loop exits early, the worker distinguishes an external clear
(abandon the batch) from `thread_generate_audio`'s own cancel (a replacement is already
queued under a new generation — leave it alone) by comparing generations. Getting that
wrong ate the replacement clip; it is pinned by test.

### 3.3 `STRUCTURED_OUTPUT` means two different things

This is the subtlety most likely to bite a future change:

| | `STRUCTURED_OUTPUT = True` means |
|---|---|
| **VaneXa** | The reply is a JSON envelope. It genuinely **cannot** be spoken as it streams — half a JSON document read aloud is far worse than a pause |
| **KitchnTabs** | Only ever "keep `on_speak` unwired". Its prompt emits plain prose and never the envelope, which is exactly why `_on_run_finished` overrides instead of parsing |

Conflating them would either read half an envelope aloud or silently disable streaming on
the kiosk that asked for it. The distinction is now explicit as `_reply_is_prose()`, which
`TenantAssistant` overrides to `True`.

A **prose VaneXa Lab keeps speaking progressively regardless of pipeline** — that was always
the intent of wiring `on_speak` for it; it simply never worked. That is the one behaviour
that changes without a flag, and it changes from broken to correct.

### 3.4 Non-ElevenLabs providers

Only ElevenLabs can truly stream audio. Everything else (gTTS, piper, edge, pyttsx3,
sherpa) gets **sentence-chunking**: per-sentence clips played back to back from the queue.
Not true streaming, but it delivers most of the win and keeps the Pi's offline providers
improving too.

---

## 4. Holding phrases (`FILLER_MODE`)

Streaming shortens the wait; it cannot remove it. `FILLER_MODE` covers what is left.

```yaml
FILLER_MODE: "off"          # off | local | bedrock
FILLER_PHRASES:
  - "Déjame ver."
  - "Un momento, por favor."
  - "Voy a revisar eso."
  - "A ver qué tenemos."
```

### 4.1 `local` — from the device

Phrases come from **`FILLER_PHRASES` in `config*.yaml`**, or from the admin panel
(`kiosk_filler_phrases`, one per line — see §6). There is no separate phrase file.

Spoken **before** `send_message`, not after: `send_message` is itself a blocking HTTP call,
and the silence being covered starts the moment the customer stops talking. Zero latency,
zero cost, and a disk-cache hit after first use — so there is not even a synthesis delay.

It cannot refer to what was asked.

### 4.2 `bedrock` — generated, mentions the question

> **Answering the question directly: yes.** `FILLER_MODE: bedrock` plus
> `KT_AGENT_FILLER_ENABLED=true` sends a quick, tool-less request to the cheapest model on
> Bedrock and speaks the result while the real turn is still running.

`RunFillerTurnJob` (domain) broadcasts a `PREAMBLE_MESSAGE` stream event carrying one short
line — *"déjame ver qué tenemos de pad thai"*.

**Dispatched alongside `RunAgentTurnJob`, never from inside it.** That is the entire design:
run inline, this call's own latency would be added to the delay it exists to hide. Both land
on the `agent` queue and start together.

| | |
|---|---|
| Model | `us.amazon.nova-micro-v1:0` — cheapest on Bedrock, $0.035 / $0.14 per MTok |
| Cost | **~$0.00002 per turn** — judge it on latency, not on the bill |
| Tools | **Empty list.** `BedrockAgentRunner::params()` omits `toolConfig` entirely when empty, so the model is never offered a tool it could turn a holding phrase into a menu search with |

Nova Micro was rejected as the *main* agent model for weak tool-calling
(`kt_agent_defaults.php`). **That reason does not apply here** — this call has no tools.

⚠️ **The context key is `systemPrompt`, not `system`.** `params()` reads the former and
silently ignores anything else, so getting it wrong hands the model the bare question with
no instructions — and it answers it, which is exactly what the prompt spends most of its
words preventing.

### 4.3 Output is rejected, not salvaged

`cleanPhrase()` drops anything that is not one short plain sentence. Several sentences means
the model started answering — and the real turn is concurrently doing that, so two answers
disagreeing is worse than one slow one. Every rejection degrades to today's silence, which is
always safe; a bad *accept* is spoken aloud to a customer with no chance to retract it.
Length is counted in characters, not bytes, or accented Spanish would be rejected for being
multi-byte.

### 4.4 Kiosk-side handling

`PREAMBLE_MESSAGE` gets its **own callback**, not `on_speak`. Letting it into the buffer
would put it in `on_finished`'s text, in the transcript, and in the product-name recovery
scan — so a holding phrase mentioning a dish could make the *screen* show that dish.

At most one phrase per turn. A backend preamble arriving **after** the answer has started
speaking is dropped outright: the silence it exists to cover never happened, and queueing it
late would have the character announce it is about to look something up after it already
answered.

---

## 5. Echo cancellation (`AEC_BACKEND`) and barge-in

```yaml
AEC_BACKEND: "none"          # none | inprocess | system
AEC_NOISE_SUPPRESSION: True
AEC_AUTO_GAIN: False
BARGE_IN_ENABLED: False
BARGE_IN_FRAMES: 3
```

### 5.1 Why in-process is the baseline

There is **no single OS-level mechanism** across the targets — verified, not assumed:

| Target | Audio server | OS-level AEC |
|---|---|---|
| macOS (dev) | CoreAudio | none |
| Windows | WASAPI | none |
| Raspberry Pi (Bookworm/trixie) | **PipeWire** | `libpipewire-module-echo-cancel` — PipeWire-native config, *not* `pactl load-module` |
| TC191 / Bodhi | PulseAudio | `module-echo-cancel` *(unverified)* |

Checked on the live Pi: `pipewire` + `pipewire-pulse`, module present, **no PulseAudio module
directory at all**. So `inprocess` (`pywebrtc-audio`, WebRTC AEC3) is the baseline, and
`system` is a per-device override costing **zero code** — point `AUDIO_INPUT_DEVICE` at an
already-cancelled source.

⚠️ **`system` and `inprocess` are mutually exclusive.** Cancelling twice against a reference
already removed makes the adaptive filter diverge — worse than doing nothing.

### 5.2 `FarEndTap` — the actually hard part

AEC3 needs both the microphone signal and the speaker signal. Getting "both" is the
difficulty: playback writes a full **second** per `stream.write()` (a deliberate TC191
underrun fix), the mic reads ~85 ms chunks, and AEC3 works in 10 ms frames.

Rather than forcing them to agree, the buffer is **timestamped, not paced**: a writer says
*when* audio reaches the speaker, a reader asks *what was playing across an interval*. Chunk
sizes then stop mattering — which is what lets the 1-second write, and the underrun fix it
exists for, stay exactly as they are.

> This corrected a planning assumption. The 1-second chunk was expected to be a blocker for
> AEC. It isn't. What it *does* bound is barge-in cut latency.

### 5.3 Measured: both delay knobs are inert

`testing/aec_bench.py` sweeps `align_ms` × `stream_delay_ms` against simulated true delays of
10, 40 and 120 ms:

- `stream_delay_ms` changes ERLE by **0.0 dB in every cell of every sweep**
- `align_ms` only ever makes it **worse** (31.5 dB at 0, down to ~26 dB as it shifts)
- AEC3 converges to ~31.5 dB whatever the real delay is — **it estimates the delay itself**

**So the settings dialog deliberately has no delay slider.** A control an operator can turn,
hear the room change for unrelated reasons, and conclude is working is worse than no control.

What the Audio tab shows instead is the **measurement**: bypass (the honest A/B, in the real
room, in one click), noise suppression, AGC, and a live ERLE reading plus near/far/cleaned
levels. Those levels separate two failures that look identical from across a room — the
reference never arriving (*plumbing bug*, "altavoz" dead) versus the filter not converging
(*room/level problem*, "altavoz" alive, ERLE low). Opposite fixes.

### 5.4 Degradation is total

Missing library, unsupported rate, constructor throwing, or the processor failing at runtime
all return `None` or pass audio through untouched. A weak device must degrade to *no echo
cancellation*, never to *the mic falls behind* — a laggy mic reads as the kiosk ignoring the
customer, which is worse than the echo. A consecutive-strike fuse enforces that on both
exceptions and per-frame time.

### 5.5 Barge-in

With AEC in front of it, `speech_probability` describes the **cleaned** signal — the first
time the kiosk can tell "someone is talking" from "I am talking". Several consecutive frames
over threshold cancel playback through the same `cancel_queue()` the SKIP path uses.

- **Several frames, not one**: a single frame is a door, a chair, a laugh from the next
  table. Cutting the character off for that is worse than no barge-in at all.
- **Cancels the whole batch**: a customer who interrupts does not want the remaining two
  sentences of the old answer afterwards.
- **Replaces muting** rather than sitting alongside it — leaving the mute would make barge-in
  structurally impossible. A *manual* mute still wins.
- **Cannot be enabled without a canceller** — otherwise the kiosk interrupts itself on its
  own first syllable. Requesting it on a device without one logs why.

### 5.6 A pre-existing finding worth acting on

`_is_muted_now()` short-circuits on the character-name gate and returns `False`, **skipping
every automatic mute rule** — and `CHARACTER_NAME` is non-empty in every KitchnTabs config.
So today the mic is *already* open while the character talks, and self-transcription is
prevented by two **text-level filters** (the name gate, plus 0.85 string similarity), not by
muting.

Consequence: **`kiosk_mute_mic_while_speaking` and `kiosk_mic_unmute_lead_seconds` currently
do nothing on KitchnTabs.** That is a live admin-panel bug independent of this POC.

---

## 6. Configuration surfaces

Three layers, in precedence order — this is the existing `_kiosk_setting()` idiom, not a new
mechanism.

| Layer | Where | Scope |
|---|---|---|
| 1. Admin panel | Agent Configuration → **Kiosk Configuration** tab | Per tenant, remote |
| 2. `config*.yaml` | 19 variants on the device | Per machine |
| 3. Module constant | `kitchntabs.py` / `vanexa.py` | Fallback |

> **Note the surface.** These are **agent configuration** settings
> (`kt_agent_kiosk_settings.php`, `kiosk_`-prefixed, read by `_kiosk_setting()`) — *not* the
> tenant `ai` tab described in [AI Tenant Settings](AI-TENANT-SETTINGS.md), which holds
> provider API keys and the main agent prompt. Different files, different consumers.

### 6.1 Settings added

| id | type | notes |
|---|---|---|
| `kiosk_voice_pipeline` | select | `classic` \| `streaming` |
| `kiosk_filler_mode` | select | `off` \| `local` \| `bedrock` |
| `kiosk_filler_phrases` | textarea | One per line, picked at random. Mirrors `kiosk_greetings` |
| `kiosk_barge_in_enabled` | boolean | Needs `AEC_BACKEND` **on the device** — can be switched on centrally and still do nothing |

Mirrored into `vanexa-backend-domain/config/lab_project_settings.php`: both kiosks share
`pw/vanexa/assistant.py`, so both read these keys.

⚠️ **`tab` stays `'kiosk'` for all of them.** A second `tab` value does **not** create a
second admin tab — `DashAutoFormTabs` takes its single-group branch only while every entry
shares one tab, and a second value makes it emit `FormTab` elements nested inside the
already-active tab, which does not render. Visual grouping is what `group` is for.

### 6.2 Device-only settings

`AEC_BACKEND`, `AEC_*` and `MIC_SAMPLE_RATE` are **deliberately not tenant settings**. Echo
delay and cancellation quality are properties of *this* speaker, *this* microphone and the
distance between them — the same argument `_system_voice_id` already makes for pyttsx3 voice
ids being machine-specific.

### 6.3 Server-side

```bash
KT_AGENT_FILLER_ENABLED=false                    # off by default
KT_AGENT_FILLER_MODEL=us.amazon.nova-micro-v1:0
```

Off by default because it spends real money per turn and changes what the customer hears —
opt-in per environment, not something a deploy switches on silently.

---

## 7. Files changed

```
kt-kiosk-agent/                       (branch poc/improved-flow, 9 commits)
├── pw/audio_player.py                [queue + workers, in-memory render, batch timing,
│                                      far-end publishing]
├── pw/aec.py                         [new: FarEndTap, EchoCanceller, resampler chain]
├── pw/speech_recognizer.py           [AEC in _read_chunk, barge-in detection]
├── pw/vanexa/agent_stream.py         [PREAMBLE_MESSAGE + on_filler]
├── pw/vanexa/assistant.py            [VOICE_PIPELINE / FILLER_MODE gates, _reply_is_prose]
├── pw/kitchntabs/tenant_assistant.py [prose override, per-chunk markdown strip]
├── pw/ui/settings_dialog.py          [tabs + Audio tab + AEC diagnostics]
├── kitchntabs.py, vanexa.py          [config, wiring, _switch_aec, shutdown()]
├── config*.yaml                      [19 variants: 4 new blocks each]
├── requirements*.txt, *.spec         [pywebrtc-audio, optional at runtime]
└── testing/                          [test_aec.py, test_streaming_pipeline.py,
                                       test_audio_render.py, aec_bench.py]

kitchntabs-backend-domain/            (branch poc/improved-flow, 2 commits)
├── app/Jobs/AI/RunFillerTurnJob.php  [new]
├── config/kt_agent_filler.php        [new]
├── config/kt_agent_kiosk_settings.php[+4 conversation settings]
├── app/Http/.../AgentChatController.php [dispatch the filler job alongside the turn]
└── tests/PureUnit/AgentFillerPhraseTest.php [new, 11 tests]

vanexa-backend-domain/                (branch poc/improved-flow, 1 commit)
└── config/lab_project_settings.php   [+4 conversation settings, mirrored]

dash-backend/                          NO CHANGES
```

---

## 8. Test coverage

| Suite | Checks |
|---|---|
| `testing/test_aec.py` | 47 — tap arithmetic, wrapping, exact-length contract, degradation paths, real cancellation (51 dB), fuse, per-frame cost, **end-to-end publish→consume at mismatched rates (49.1 dB)**, barge-in |
| `testing/test_audio_render.py` | 44 — byte-identical rendering at 3 rates, no disk writes, concurrent-render independence, write-loop ordering, external kill switch, queue ordering, cancel-and-replace, batch timing |
| `testing/test_streaming_pipeline.py` | 33 — pipeline gate on **both** assistants, classic vs streaming, markdown stripping, filler modes, transcript non-contamination |
| `testing/test_settings_dialog.py` | 42 — tabs, pending-flush on switch, diagnostics availability and fault tolerance |
| `AgentFillerPhraseTest.php` | 11 — phrase filter: rejection over salvage, multi-byte length |
| Full kiosk suite | **19 files, all passing** |

`testing/aec_bench.py` is a harness, not a test: it sweeps the delay grid and prints ERLE per
cell with a plain-language reading of which knob is live.

---

## 9. Not done / known gaps

- **No real-hardware validation.** AEC costs 1% of frame time on an Intel Mac; the Pi and
  TC191 are the real test. ERLE figures are synthetic echo, not a room.
- **ElevenLabs still uses `.convert()`**, not the streaming/websocket endpoint, and
  `ELEVENLABS_MODEL` is still `eleven_multilingual_v2` rather than `eleven_flash_v2_5`
  (~75 ms inference). Sentence-chunking works today; true streaming is the next win.
- **Nova Sonic (speech-to-speech) not started.** Evaluated: PHP has no bidirectional
  streaming SDK, so it needs STS-vended short-lived credentials to the Python kiosk plus a
  session id on the `/mcp` path (currently unset, so every cart tool answers `noCart()`).
  Plausibly *cheaper* than the current ElevenLabs path — ~$0.03 vs ~$0.07–0.36 per
  conversation.
- **Gesture cues are suppressed per sentence.** `performance` cues anchor to spans of the
  *whole* reply, so splitting misplaces them; streaming falls back to `simulate_lipsync`
  per clip. Re-anchoring by offset is follow-up work.
- **Barge-in cut latency is bounded by the 1-second playback chunk.** PyAudio exposes no
  `Pa_AbortStream`, so a faster cut needs smaller writes — which is the TC191 underrun
  tradeoff.
- **`utterance handoff still polls a file on a 1-second sleep`** — a fixed latency floor on
  every turn that no amount of filler work removes. Cheap independent win.
- **`kiosk_mute_mic_while_speaking` / `kiosk_mic_unmute_lead_seconds` do nothing on
  KitchnTabs** (§5.6). Pre-existing, worth its own fix.
