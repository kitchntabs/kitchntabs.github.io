# AI Agents Documentation - Voice & Image Features

## Overview

The Dash POS system includes two powerful AI-powered features that enable hands-free and visual order processing:

1. **Voice Agent** - Processes spoken commands to add, remove, or modify products in an order
2. **Image Agent** - Analyzes images (photos of menus, handwritten orders, receipts) to extract order information

Both features follow a similar multi-step AI pipeline architecture and integrate seamlessly with the Tab management system.

---

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Voice Agent Feature](#voice-agent-feature)
3. [Image Agent Feature](#image-agent-feature)
4. [Shared Components](#shared-components)
5. [Status Indicators](#status-indicators)
6. [Analysis Drawer](#analysis-drawer)
7. [Action Processing Pipeline](#action-processing-pipeline)
8. [Modifier Resolution](#modifier-resolution)
9. [API Endpoints](#api-endpoints)
10. [Configuration Options](#configuration-options)
11. [Troubleshooting](#troubleshooting)

---

## Architecture Overview

### High-Level Flow

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Frontend UI   │────▶│   Backend API   │────▶│   OpenAI API    │
│  (React/MUI)    │     │   (Laravel)     │     │  (GPT-4/Whisper)│
└─────────────────┘     └─────────────────┘     └─────────────────┘
         │                       │                       │
         │                       ▼                       │
         │              ┌─────────────────┐              │
         │              │ Product Service │              │
         │              │ (Resolution)    │              │
         │              └─────────────────┘              │
         │                       │                       │
         ▼                       ▼                       │
┌─────────────────┐     ┌─────────────────┐              │
│ TabManager      │◀────│ Actions Array   │◀─────────────┘
│ Context         │     │ (Structured)    │
└─────────────────┘     └─────────────────┘
```

### Technology Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| Frontend UI | React + MUI | User interface components |
| State Management | React Context + Hooks | State and data flow |
| Voice Recording | Capacitor VoiceRecorder | Native voice capture |
| Image Capture | Capacitor Camera | Native camera/gallery |
| HTTP Client | Axios | API communication |
| Backend Framework | Laravel | API server |
| AI - Vision | GPT-4o (OpenAI) | Image analysis |
| AI - Voice | Whisper-1 (OpenAI) | Audio transcription |
| AI - Actions | GPT-4-turbo (OpenAI) | Action extraction & enhancement |

---

## Voice Agent Feature

### Components

#### 1. VoiceTabAgent (`VoiceTabAgent.tsx`)
The main UI component for voice recording and displaying results.

**File Location:** `dash-frontend/apps/dash/src/components/voice/VoiceTabAgent.tsx`

**Props:**

```typescript
interface VoiceTabAgentProps {
    tabId?: string | null;           // Current tab ID
    tabData?: any;                   // Tab context data
    onActionsDetected?: (actions: VoiceAction[]) => void;  // Callback
    onError?: (error: string) => void;
    disabled?: boolean;              // Disable recording
    autoApply?: boolean;             // Auto-apply actions to order
    layout?: 'vertical' | 'horizontal';  // UI layout mode
    showExamples?: boolean;          // Show command examples
    sessionId?: string;              // Session identifier
    debug?: boolean;                 // Enable debug mode
}
```

**Features:**
- Two layout modes: `horizontal` (compact) and `vertical` (full)
- Real-time recording status indicator
- Processing steps visualization
- Results display with product resolution status
- Debug information panel
- Command examples panel
- Analysis drawer for detailed AI results

#### 2. useVoiceAgent Hook (`useVoiceAgent.tsx`)
Custom React hook that handles all voice recording and processing logic.

**File Location:** `dash-frontend/apps/dash/src/components/voice/useVoiceAgent.tsx`

**Returns:**

```typescript
interface UseVoiceAgentReturn {
    // State
    isRecording: boolean;
    isProcessing: boolean;
    lastTranscription: string;
    lastActions: VoiceAction[];
    processingSteps: ProcessingSteps;
    hasEnhancedAnalysis: boolean;
    
    // Actions
    toggleRecording: (sessionId: string, tabId?: string, options?: object) => void;
    cleanup: () => void;
    
    // Helpers
    getModifierSuggestions: () => SuggestedModifier[];
    getAutoAddedProducts: () => VoiceAction[];
    getProcessingMetrics: () => ProcessingMetrics;
    getAudioChunksInfo: () => AudioChunksInfo;
    getDebugInfo: () => DebugInfo;
}
```

#### 3. VoiceAgentService (Backend)
Laravel service that handles audio transcription and action extraction.

**File Location:** `dash-backend/app/Services/OpenAI/VoiceAgentService.php`

**Key Methods:**
- `transcribeAudio()` - Converts audio to text using Whisper API
- `extractInitialActions()` - Step 1: Basic action extraction
- `resolveProducts()` - Step 2: Product name resolution
- `enhanceWithContext()` - Step 3: AI-enhanced analysis with modifiers

### Voice Action Types

```typescript
interface VoiceAction {
    action: 'add' | 'remove' | 'modify_quantity' | 'add_note';
    product_names: string[];         // Original product names from voice
    quantity?: number;               // Quantity to add/change
    note?: string;                   // Note to add to product
    confidence: number;              // AI confidence score (0-1)
    
    // Resolution
    resolved_products?: ResolvedProduct[];
    resolution_status?: 'found' | 'not_found' | 'multiple' | 'resolution_error';
    
    // Modifiers
    modifiers?: string[];            // Raw modifiers (e.g., ["con arroz"])
    suggested_modifiers?: SuggestedModifier[];  // AI-resolved with IDs
    
    // AI Enhancement
    auto_added?: boolean;            // AI auto-suggested this action
    auto_added_reason?: string;
    ai_analysis?: string;            // AI reasoning
    confidence_boost?: number;       // Additional confidence from enhancement
}
```

### Voice Command Examples

| Command (Spanish) | Action | Result |
|-------------------|--------|--------|
| "Agrega dos hamburguesas con queso" | add | 2x hamburguesas, modifier: queso |
| "Quiero un café grande para llevar" | add | 1x café grande, note: para llevar |
| "Elimina la pizza del pedido" | remove | Removes pizza from order |
| "Cambia la cantidad de tacos a tres" | modify_quantity | Updates tacos quantity to 3 |
| "Agrega nota: sin cebolla al burrito" | add_note | Adds note to burrito |

---

## Image Agent Feature

### Components

#### 1. ImageTabAgent (`ImageTabAgent.tsx`)
The main UI component for image capture and analysis.

**File Location:** `dash-frontend/apps/dash/src/components/image/ImageTabAgent.tsx`

**Props:**

```typescript
interface ImageTabAgentProps {
    tabId?: string | null;
    tabData?: any;
    onActionsDetected?: (actions: ImageAgentAction[]) => void;
    onError?: (error: string) => void;
    disabled?: boolean;
    autoApply?: boolean;
    layout?: 'vertical' | 'horizontal';
    showExamples?: boolean;
    sessionId?: string;
    debug?: boolean;
    analysisType?: 'menu' | 'receipt' | 'order' | 'general';
}
```

**Features:**
- Camera capture with countdown timer
- Gallery image selection
- Web camera support (on web platform)
- Multiple analysis types: menu, receipt, order, general
- Results display with product thumbnails
- Analysis drawer for detailed AI results

#### 2. useImageAgent Hook (`useImageAgent.tsx`)
Custom React hook for image processing.

**File Location:** `dash-frontend/apps/dash/src/components/tab/hooks/useImageAgent.tsx`

**Returns:**

```typescript
interface UseImageAgentReturn {
    // State
    isProcessing: boolean;
    result: ImageAgentResult | null;
    error: string | null;
    lastActions: ImageAgentAction[];
    processingSteps: ProcessingSteps;
    
    // Actions
    processImage: (options: ProcessImageOptions) => Promise<void>;
    clearResult: () => void;
    
    // Helpers
    getProcessingMetrics: () => ProcessingMetrics;
    getDebugInfo: () => DebugInfo;
}
```

#### 3. useImageCapture Hook (`useImageCapture.tsx`)
Handles camera/gallery image capture with countdown functionality.

**File Location:** `dash-frontend/apps/dash/src/components/tab/hooks/useImageCapture.tsx`

**Features:**
- Native camera capture (Capacitor)
- Photo gallery selection
- Web camera support with countdown
- Configurable countdown duration
- Capture cancellation support

#### 4. ImageAgentService (Backend)
Laravel service for image analysis using GPT-4 Vision.

**File Location:** `dash-backend/app/Services/OpenAI/ImageAgentService.php`

**Key Methods:**
- `analyzeImage()` - Vision API analysis
- `extractActionsFromAnalysis()` - Action extraction from analysis text
- `resolveProductsInActions()` - Product resolution
- `enhanceActionsWithProductContext()` - Modifier suggestion enhancement

### Image Action Types

```typescript
interface ImageAgentAction {
    action: 'add' | 'remove' | 'modify_quantity' | 'add_note';
    product_names: string[];
    quantity: number;
    note: string;
    confidence: number;
    source: string;                  // 'image_analysis'
    raw_text?: string;               // Original text from image
    
    // Resolution
    resolved_products?: ResolvedProduct[];
    resolution_status?: 'found' | 'multiple_found' | 'not_found';
    
    // Modifiers
    modifiers?: string[];            // Raw modifiers detected
    suggested_modifiers?: SuggestedModifier[];
    
    // AI Enhancement
    ai_analysis?: string;
    confidence_boost?: number;
}
```

### Analysis Types

| Type | Use Case | AI Focus |
|------|----------|----------|
| `menu` | Restaurant menu photos | Item names, prices, descriptions |
| `receipt` | Receipt/ticket photos | Items, quantities, prices |
| `order` | Handwritten orders | Item names, quantities, modifiers |
| `general` | Any image | General item detection |

---

## Shared Components

### ResolvedProduct Structure

```typescript
interface ResolvedProduct {
    id: number;
    name: string;
    sku: string;
    price: string;
    relevance_score: number;
    gallery?: any;
    primary_image_url?: string;
    product_data?: {
        modifier_groups?: ModifierGroup[];
        prices?: Price[];
        [key: string]: any;
    };
}
```

### SuggestedModifier Structure

```typescript
interface SuggestedModifier {
    product_id?: number;
    modifier_group_id?: number;
    modifier_option_id?: number;
    modifier_group_name?: string;
    modifier_option_name: string;
    detection_reason: string;
    confidence: number;
    matched_keywords?: string[];
    detection_type?: 'keyword_match' | 'context_inference' | 'default';
}
```

### ProcessingSteps Structure

```typescript
interface ProcessingSteps {
    step_0_image_analysis?: number;      // Image only
    step1_initial_extraction: string;    // Action extraction result
    step2_product_resolution: string;    // Product resolution status
    step3_enhanced_analysis: string;     // AI enhancement status
}
```

---

## Status Indicators

Both Voice and Image agents use consistent status indicators with UTF-8 colored circles:

| Circle | Color | Status | Description |
|--------|-------|--------|-------------|
| 🟢 | Green | Ready | System is ready to capture/record |
| 🟡 | Yellow | Processing | AI is processing the input |
| 🔴 | Red | Recording | Voice recording in progress (Voice only) |
| 🔵 | Blue | Success | Actions detected successfully |

### Implementation

```typescript
const getStatusCircle = () => {
    if (isProcessing) return '🟡'; // yellow - processing
    if (isRecording) return '🔴';  // red - recording (voice only)
    if (lastActions.length > 0) return '🔵'; // blue - success
    return '🟢'; // green - ready
};

const getStatusText = () => {
    if (isProcessing) return 'Procesando con IA...';
    if (isRecording) return 'Grabando...';
    if (lastActions.length > 0) return `${lastActions.length} acción(es) detectada(s)`;
    return 'Listo para grabar';
};
```

The status circle is displayed with a Tooltip that shows the full status text on hover.

---

## Analysis Drawer

Both Voice and Image agents include an Analysis Drawer feature accessible via an Info button (ℹ️).

### Features

The drawer displays:

1. **Transcription/Original Analysis** - Raw input text or image analysis
2. **Processing Steps** - Visual chips showing completion status
3. **Detected Actions** - List of actions with:
   - Action type (add, remove, modify)
   - Product names
   - Quantities
   - Resolved products with details
   - AI-suggested modifiers
   - Raw modifiers detected
   - Notes
   - AI analysis reasoning
4. **Processing Metrics** - Statistics about the analysis:
   - Total actions count
   - Products resolved count
   - Modifiers suggested count
   - Auto-added products count
5. **Debug Info** - (When debug mode enabled) Full JSON debug data

### Implementation

{% raw %}
```typescript
const renderAnalysisDrawer = () => (
    <SwipeableDrawer
        anchor="right"
        open={showAnalysisDrawer}
        onClose={() => setShowAnalysisDrawer(false)}
        onOpen={() => setShowAnalysisDrawer(true)}
    >
        <Box sx={{ width: 400, p: 2 }}>
            {/* Header */}
            {/* Transcription/Analysis */}
            {/* Processing Steps */}
            {/* Actions List */}
            {/* Metrics */}
            {/* Debug Info */}
        </Box>
    </SwipeableDrawer>
);
```
{% endraw %}

---

## Action Processing Pipeline

### Voice Agent Pipeline

```
┌──────────────────┐
│ 1. Audio Capture │  Capacitor VoiceRecorder
└────────┬─────────┘
         ▼
┌──────────────────┐
│ 2. Transcription │  OpenAI Whisper-1 (Spanish)
└────────┬─────────┘
         ▼
┌──────────────────┐
│ 3. Action        │  GPT-4-turbo-preview
│    Extraction    │  Extract actions from text
└────────┬─────────┘
         ▼
┌──────────────────┐
│ 4. Product       │  Elasticsearch/Database
│    Resolution    │  Match names to products
└────────┬─────────┘
         ▼
┌──────────────────┐
│ 5. AI            │  GPT-4-turbo-preview
│    Enhancement   │  Suggest modifiers, validate
└────────┬─────────┘
         ▼
┌──────────────────┐
│ 6. Apply to      │  TabManagerContext
│    Order         │  handleVoiceActions()
└──────────────────┘
```

### Image Agent Pipeline

```
┌──────────────────┐
│ 1. Image Capture │  Capacitor Camera / Gallery
└────────┬─────────┘
         ▼
┌──────────────────┐
│ 2. Vision        │  GPT-4o (Vision)
│    Analysis      │  Analyze image content
└────────┬─────────┘
         ▼
┌──────────────────┐
│ 3. Action        │  GPT-4-turbo-preview
│    Extraction    │  Extract actions from analysis
└────────┬─────────┘
         ▼
┌──────────────────┐
│ 4. Product       │  Elasticsearch/Database
│    Resolution    │  Match names to products
└────────┬─────────┘
         ▼
┌──────────────────┐
│ 5. Modifier      │  GPT-4-turbo-preview
│    Enhancement   │  Match modifiers to options
└────────┬─────────┘
         ▼
┌──────────────────┐
│ 6. Apply to      │  TabManagerContext
│    Order         │  handleVoiceActions()
└──────────────────┘
```

---

## Modifier Resolution

### The Challenge

AI models detect modifiers as natural language strings (e.g., "con arroz", "sin cebolla") but the POS system requires specific modifier option IDs to add them to an order.

### Solution: Multi-Level Resolution

#### Level 1: Backend AI Enhancement

The backend AI analyzes product modifier groups and attempts to match detected modifiers:

```php
// ImageAgentService.php - Enhancement Prompt
"For each action, analyze if the detected modifiers match any of the product's 
available modifier_groups.options. Match by semantic similarity, not exact match.
Example: 'con arroz' should match a modifier option named 'Arroz' or 'Con Arroz'"
```

#### Level 2: Frontend Fallback Resolution

If the backend doesn't resolve modifiers, the frontend attempts client-side resolution:

```typescript
// TabManagerContext.tsx
const resolveRawModifiersToProduct = (rawModifiers: string[], product: any) => {
    const modifierGroups = product.product_data?.modifier_groups || [];
    const resolved = [];
    
    for (const rawMod of rawModifiers) {
        const normalizedRaw = rawMod.toLowerCase().trim();
        
        for (const group of modifierGroups) {
            for (const option of group.options) {
                const optionName = option.name.toLowerCase();
                // Fuzzy matching
                if (optionName.includes(normalizedRaw) || 
                    normalizedRaw.includes(optionName)) {
                    resolved.push({
                        modifier_group_id: group.id,
                        modifier_option_id: option.id,
                        modifier_option_name: option.name
                    });
                    break;
                }
            }
        }
    }
    
    return resolved;
};
```

#### Level 3: Unresolved as Notes

Modifiers that cannot be matched to product options are converted to notes:

```typescript
const { resolved, unresolved } = resolveRawModifiersToProductWithUnresolved(
    action.modifiers, 
    product
);

if (unresolved.length > 0) {
    // Add unresolved modifiers to the product note
    note = note ? `${note} | ${unresolved.join(', ')}` : unresolved.join(', ');
}
```

### Modifier vs Note Distinction

The AI prompts distinguish between:

| Type | Description | Examples |
|------|-------------|----------|
| **MODIFIERS** | Preparation variations that match product options | "con arroz", "sin cebolla", "extra queso" |
| **NOTES** | Service instructions or special requests | "urgente", "para llevar", "mesa 5" |

---

## API Endpoints

### Voice Agent Endpoints

```
POST /api/voice-agent/process
```

**Request:**
```json
{
    "audio": "<base64 audio data>",
    "session_id": "voice_session_123",
    "tab_id": "456",
    "options": {
        "enhanced_analysis": true,
        "language": "es",
        "tab_context": {
            "current_order": {...},
            "table_number": "5"
        }
    }
}
```

**Response:**
```json
{
    "success": true,
    "data": {
        "id": 1,
        "original_transcription": "agrega dos hamburguesas con queso",
        "actions": [...],
        "processing_steps": {
            "step1_initial_extraction": "completed",
            "step2_product_resolution": "completed",
            "step3_enhanced_analysis": "completed"
        },
        "enhanced_analysis": true,
        "processing_time": 1234
    },
    "session_id": "voice_session_123"
}
```

### Image Agent Endpoints

```
POST /api/image-agent/analyze
```

**Request:**
```json
{
    "image": "<base64 image data>",
    "session_id": "image_session_123",
    "analysis_type": "order",
    "tab_id": "456",
    "context": {
        "table_number": "5"
    }
}
```

**Response:**
```json
{
    "success": true,
    "data": {
        "id": 1,
        "original_analysis": "Detected items: 2x Hamburguesa, 1x Coca Cola...",
        "actions": [...],
        "processing_steps": {
            "step_0_image_analysis": 2345,
            "step_1_action_extraction": 567,
            "step_2_product_resolution": 234,
            "step_3_modifier_enhancement": 456
        },
        "processing_time": 3602
    },
    "session_id": "image_session_123"
}
```

---

## Configuration Options

### Voice Agent Configuration

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `autoApply` | boolean | false | Auto-apply detected actions to order |
| `layout` | string | 'vertical' | UI layout: 'vertical' or 'horizontal' |
| `showExamples` | boolean | false | Show command examples panel |
| `debug` | boolean | false | Enable debug mode |
| `disabled` | boolean | false | Disable voice recording |

### Image Agent Configuration

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `autoApply` | boolean | false | Auto-apply detected actions to order |
| `layout` | string | 'vertical' | UI layout: 'vertical' or 'horizontal' |
| `analysisType` | string | 'order' | Analysis type: 'menu', 'receipt', 'order', 'general' |
| `showExamples` | boolean | false | Show usage examples |
| `debug` | boolean | false | Enable debug mode |
| `countdownSeconds` | number | 3 | Camera countdown duration |

### Backend Configuration

Environment variables in `.env`:

```env
OPENAI_API_KEY=sk-...
OPENAI_ORGANIZATION=org-...

# Model selection
OPENAI_VISION_MODEL=gpt-4o
OPENAI_CHAT_MODEL=gpt-4-turbo-preview
OPENAI_WHISPER_MODEL=whisper-1

# Processing options
VOICE_AGENT_MAX_AUDIO_SIZE=10485760
IMAGE_AGENT_MAX_IMAGE_SIZE=20971520
AI_AGENT_TIMEOUT=60
```

---

## Troubleshooting

### Common Issues

#### Voice Recording Not Working

1. **Check permissions**: Ensure microphone permissions are granted
2. **Check Capacitor**: Verify VoiceRecorder plugin is installed
3. **Check audio format**: WebM format is required for web

```typescript
// Debug: Check if VoiceRecorder is available
const isVoiceRecorderAvailable = (): boolean => {
    return !!(window as any)?.Capacitor?.Plugins?.VoiceRecorder;
};
```

#### Image Capture Not Working

1. **Check permissions**: Camera/gallery permissions required
2. **Check platform**: Different behavior on web vs native
3. **Check image size**: Large images may timeout

#### Modifiers Not Applied

1. **Check suggested_modifiers**: AI may not have resolved them
2. **Check product modifier_groups**: Product may lack modifier options
3. **Check raw modifiers**: See Analysis Drawer for detected modifiers
4. **Enable debug mode**: View full resolution process

#### Actions Not Detected

1. **Check transcription/analysis**: View in Analysis Drawer
2. **Check product names**: May not match catalog
3. **Check confidence scores**: Low confidence actions may be filtered
4. **Review AI analysis**: Check `ai_analysis` field for reasoning

### Debug Mode

Enable debug mode to see:
- Raw API responses
- Processing timestamps
- Resolution attempts
- Full action objects

```tsx
<VoiceTabAgent
    debug={true}
    tabId={tabId}
    onActionsDetected={handleActions}
/>
```

### Logging

Backend logs are available at:
```
dash-backend/storage/logs/laravel-YYYY-MM-DD.log
```

Key log prefixes:
- `VoiceAgentService::` - Voice processing logs
- `ImageAgentService::` - Image processing logs
- `ProductService::` - Product resolution logs

---

## File Reference

### Frontend Files

| File | Purpose |
|------|---------|
| `components/voice/VoiceTabAgent.tsx` | Voice UI component (937 lines) |
| `components/voice/useVoiceAgent.tsx` | Voice processing hook (1368 lines) |
| `components/image/ImageTabAgent.tsx` | Image UI component (1101 lines) |
| `components/tab/hooks/useImageAgent.tsx` | Image processing hook (485 lines) |
| `components/tab/hooks/useImageCapture.tsx` | Camera capture hook |
| `components/tab/contexts/TabManagerContext.tsx` | Action handling context |

### Backend Files

| File | Purpose |
|------|---------|
| `Services/OpenAI/VoiceAgentService.php` | Voice AI service |
| `Services/OpenAI/ImageAgentService.php` | Image AI service |
| `Http/Controllers/API/VoiceAgentController.php` | Voice API controller |
| `Http/Controllers/API/ImageAgentController.php` | Image API controller |

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-11-27 | Initial documentation |
| - | - | Voice and Image agents documented |
| - | - | Status indicators (🟢🟡🔴🔵) |
| - | - | Analysis drawer feature |
| - | - | Modifier resolution pipeline |

---

## Contributing

When modifying AI agent features:

1. Update both Voice and Image components consistently
2. Maintain status indicator conventions
3. Update Analysis Drawer to show new data fields
4. Add debug logging for troubleshooting
5. Update this documentation

---

*Documentation generated: November 27, 2025*
