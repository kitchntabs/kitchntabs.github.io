# Upload All 195 Docs to ClickUp — Execution Guide

**Script:** `upload_docs_to_clickup.py`  
**Status:** Ready to run  
**Files to upload:** 195 markdown files  
**Execution time:** ~8 minutes (including rate-limit pauses)  
**Rate limit:** 30 req/min (script batches 25/burst, pauses 60s between)

---

## Prerequisites

### 1. ClickUp API Token

Get your ClickUp API token from your account:

1. Go to https://app.clickup.com/settings/integrations/api
2. Under "API Token" section, click "Generate"
3. Copy the token

### 2. Python & Dependencies

Ensure you have Python 3.8+:

```bash
python3 --version
```

Install the `requests` library (required for API calls):

```bash
pip install requests
```

Or use your project's virtual environment:

```bash
source venv/bin/activate
pip install requests
```

### 3. Current Directory

Navigate to the project root where `upload_docs_to_clickup.py` is located:

```bash
cd /Users/farandal/DASH-FRAMEWORK/kitchntabs-github-io/
ls upload_docs_to_clickup.py  # Should exist
```

---

## Running the Script

### Option 1: Dry Run (Recommended First)

Test the script without creating any pages:

```bash
export CLICKUP_API_TOKEN='your_token_here'
python3 upload_docs_to_clickup.py --dry-run
```

**Output:** Lists all 195 files that WOULD be created, without hitting the API.

**Check for:**
- ✅ Correct epic assignments
- ✅ All files found in `docs/` folder
- ✅ No errors parsing the mapping file

---

### Option 2: Full Upload (All 195 Files)

Once dry run looks good, proceed with the actual upload:

```bash
export CLICKUP_API_TOKEN='your_token_here'
python3 upload_docs_to_clickup.py
```

**Progress:** Real-time output shows:
- ✅ Created pages (green)
- ❌ Errors (red)
- ⏸️ Rate-limit pauses (every 25 requests)

**Time:** ~8 minutes total (including pauses)

---

### Option 3: Partial Upload (Resume / Test)

Upload only a subset of files:

```bash
# Start from epic F5 and upload max 50 files
export CLICKUP_API_TOKEN='your_token_here'
python3 upload_docs_to_clickup.py --start-epic=F5 --limit=50
```

**Flags:**
- `--start-epic=F1` — Start from a specific epic (F1, F9, N3, etc.)
- `--limit=50` — Stop after N files
- `--dry-run` — Preview without uploading

---

## Expected Output

### Dry Run

```
[14:23:45] ℹ️ Parsing mapping file...
[14:23:45] ℹ️ Found 30 epics with 195 files total
[14:23:45] 🔍 DRY RUN MODE — No pages will be created

================================================================================
EPIC                          | FILES  | STATUS
================================================================================
F1: Orders & Tabs            | 1      | [DRY] Would create: Orders & Tabs — Tab domain model
F1: Orders & Tabs            | 2      | [DRY] Would create: Orders & Tabs — Tab/mall architecture
...
[14:23:48] ✅ Upload Complete

📊 Upload Complete

  Total files processed: 195
  Successfully uploaded: 0 (dry run)
  Skipped/Errors: 0

📈 By Epic:
  F1: Orders & Tabs                            3/6 uploaded (dry)
  F2: Products & Catalog                       2/3 uploaded (dry)
  ...
```

### Real Run

```
[14:25:00] ℹ️ Parsing mapping file...
[14:25:01] ℹ️ Found 30 epics with 195 files total

================================================================================
EPIC                          | FILES  | STATUS
================================================================================
F1: Orders & Tabs            | 1      | ✅ Created: Orders & Tabs — Tab domain model
F1: Orders & Tabs            | 2      | ✅ Created: Orders & Tabs — Tab/mall architecture
F1: Orders & Tabs            | 3      | ✅ Created: Orders & Tabs — Order model reference
...
[14:25:30] ℹ️ Rate limit pause: 60s (25/195 files)
[14:26:30] ℹ️ Rate limit pause: 60s (50/195 files)
...
[14:32:15] ✅ Upload Complete

📊 Upload Complete

  Total files processed: 195
  Successfully uploaded: 195
  Skipped/Errors: 0

📈 By Epic:
  F1: Orders & Tabs                            6/6 uploaded
  F2: Products & Catalog                       3/3 uploaded
  ...
✅ All done! Visit: https://app.clickup.com/90132880480/docs/2ky5d730-1053
```

---

## Troubleshooting

### Error: `CLICKUP_API_TOKEN not set`

**Fix:** Set the environment variable before running:

```bash
export CLICKUP_API_TOKEN='pk_...'  # Your actual token
python3 upload_docs_to_clickup.py
```

Or set it inline:

```bash
CLICKUP_API_TOKEN='pk_...' python3 upload_docs_to_clickup.py
```

### Error: `requests library not installed`

**Fix:** Install the library:

```bash
pip install requests
```

### Error: `File not found` for a specific markdown file

**Cause:** The file path in `DOCS_TO_CLICKUP_MAPPING.md` doesn't match the actual file path.

**Fix:** Check the file path in the mapping and verify the file exists:

```bash
ls -la "docs/path/to/file.md"
```

If the file is missing or renamed, update `DOCS_TO_CLICKUP_MAPPING.md` with the correct path.

### Error: `Failed to create page (401 or 403)`

**Cause:** Invalid or expired API token.

**Fix:** 
1. Go to https://app.clickup.com/settings/integrations/api
2. Regenerate your token
3. Try again:

```bash
export CLICKUP_API_TOKEN='pk_new_token_here'
python3 upload_docs_to_clickup.py --dry-run
```

### Script stops after 25 requests

**This is normal!** The script pauses for 60 seconds to respect ClickUp's 30 req/min rate limit, then continues. You'll see:

```
[14:25:30] ℹ️ Rate limit pause: 60s (25/195 files)
```

Just wait — it will resume automatically.

---

## Monitoring Progress

While the script runs, you can check ClickUp in another browser window:

1. Open https://app.clickup.com/90132880480/docs/2ky5d730-1053
2. Refresh the page occasionally
3. New pages will appear as they're created

---

## After Upload

### 1. Verify All Pages Created

In ClickUp, expand the main **KitchnTabs Documentation** doc and check:

- ✅ 30 epic sections (F1–F20, N1–N10)
- ✅ Each epic has its mapped files as nested pages
- ✅ Total ~195+ pages

### 2. Publish to Web (Optional)

Make the docs publicly accessible:

1. In ClickUp, click "..." on **KitchnTabs Documentation**
2. Select "Share"
3. Toggle "Public" / "Publish to web"
4. Copy the public URL

Share with team, customers, partners.

### 3. Link Tasks to Docs (Optional, Manual)

For extra organization, link each epic's tasks to its documentation pages:

1. Open a task in an epic (e.g., F1 task)
2. Click "Link" → select the corresponding doc page from F1
3. Repeat for key tasks

This creates a bidirectional connection: Task ↔ Doc.

---

## Resuming a Failed Upload

If the script crashes or you interrupt it, you can resume from where it stopped:

```bash
# Resume from epic F7, limit to 50 files from that point
export CLICKUP_API_TOKEN='pk_...'
python3 upload_docs_to_clickup.py --start-epic=F7 --limit=50
```

The script will skip epics before F7 and upload from F7 onward.

---

## FAQ

### Q: Will duplicate pages be created if I run the script twice?

**A:** Currently, the script doesn't check for existing pages before creating. If you run it twice, you'll get duplicates. Future enhancement: check for existing pages first.

**Workaround:** Use `--dry-run` first, then run once with `--limit` to upload in batches.

### Q: Can I edit the script to customize page names or structure?

**A:** Yes! Edit `upload_docs_to_clickup.py` around line 115:

```python
# Customize page name here:
page_name = f"{epic.split(': ', 1)[1]} — {description}"
```

### Q: How long will the upload actually take?

**A:** 195 files ÷ 25 requests/burst = 8 bursts × 60s pause = **~8 minutes** (plus actual upload time).

### Q: Do I need to be online?

**A:** Yes, the script needs internet to reach the ClickUp API.

### Q: Can I run multiple script instances in parallel?

**A:** Not recommended. The rate limit is shared per account. Run one script at a time.

---

## Next Steps

1. **Run dry run first:**
   ```bash
   export CLICKUP_API_TOKEN='pk_...'
   python3 upload_docs_to_clickup.py --dry-run
   ```

2. **Review output** — check for any "File not found" errors

3. **Run full upload:**
   ```bash
   python3 upload_docs_to_clickup.py
   ```

4. **Monitor progress** — watch ClickUp Docs fill up in real-time

5. **Verify & share** — check all pages created, publish to web, share URL

---

## Support

If you hit an issue:

1. **Check the script output** — error messages are detailed
2. **Run `--dry-run`** — see what would happen
3. **Verify API token** — regenerate if unsure
4. **Check file paths** — ensure all files in mapping exist locally

---

**Time to completion: ~10 minutes (including dry run)**

Ready to go! 🚀
