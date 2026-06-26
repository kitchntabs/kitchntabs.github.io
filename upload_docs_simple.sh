#!/bin/bash
# Simple bash script to upload markdown docs to ClickUp

CLICKUP_API_TOKEN="${CLICKUP_API_TOKEN}"
DOCUMENT_ID="2ky5d730-1053"  # KitchnTabs Documentation
DOCS_DIR="/Users/farandal/DASH-FRAMEWORK/kitchntabs-github-io/docs"
MAPPING_FILE="/Users/farandal/DASH-FRAMEWORK/kitchntabs-github-io/DOCS_TO_CLICKUP_MAPPING.md"
RATE_LIMIT_DELAY=60
BATCH_SIZE=10

if [ -z "$CLICKUP_API_TOKEN" ]; then
    echo "❌ CLICKUP_API_TOKEN not set"
    exit 1
fi

echo "🚀 KitchnTabs Docs → ClickUp Upload (Simple)"
echo ""

# Counter
files_processed=0
files_created=0
files_failed=0

# Parse mapping file and upload docs
# This is a simplified version that reads the mapping and uploads files one by one

echo "📖 Parsing mapping file..."
files_to_upload=()

# Extract all file paths from the mapping
while IFS= read -r line; do
    # Match lines like: - `docs/path/file.md` — description
    if [[ $line =~ \`(docs/[^\`]+)\` ]]; then
        file_path="${BASH_REMATCH[1]}"
        files_to_upload+=("$file_path")
    fi
done < "$MAPPING_FILE"

echo "Found ${#files_to_upload[@]} files to upload"
echo ""

# Upload each file
for file_path in "${files_to_upload[@]}"; do
    ((files_processed++))

    # Check if file exists
    full_path="$DOCS_DIR/${file_path#docs/}"
    if [ ! -f "$full_path" ]; then
        echo "⏭️  Skipped: $file_path (not found)"
        ((files_failed++))
        continue
    fi

    # Read file content
    content=$(cat "$full_path")

    # Get file name for page title
    filename=$(basename "$file_path")

    # Create page via ClickUp API
    # Note: The correct endpoint should create a page under the document
    echo "📄 Uploading: $filename..."

    response=$(curl -s -X POST "https://api.clickup.com/api/v2/doc/${DOCUMENT_ID}/page" \
        -H "Authorization: $CLICKUP_API_TOKEN" \
        -H "Content-Type: application/json" \
        -d @- <<EOF
{
    "name": "$filename",
    "content": "$content"
}
EOF
    )

    # Check response
    if echo "$response" | grep -q '"id"'; then
        echo "✅ Created: $filename"
        ((files_created++))
    else
        echo "❌ Failed: $filename"
        echo "   Response: ${response:0:100}"
        ((files_failed++))
    fi

    # Rate limiting
    if [ $((files_processed % BATCH_SIZE)) -eq 0 ]; then
        echo "⏸️  Rate limit pause: ${RATE_LIMIT_DELAY}s ($files_processed/${#files_to_upload[@]})"
        sleep $RATE_LIMIT_DELAY
    fi
done

echo ""
echo "📊 Summary"
echo "  Total: ${#files_to_upload[@]}"
echo "  Created: $files_created"
echo "  Failed: $files_failed"
echo ""
echo "✅ Done!"
