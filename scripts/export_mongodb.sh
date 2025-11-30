#!/bin/bash

# MongoDB Export Script
# Exports all collections from a MongoDB database to JSON files

set -e  # Exit on error

# Configuration
DB_NAME="${DB_NAME:-podium_db}"
EXPORT_DIR="${EXPORT_DIR:-./mongodb_export}"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
EXPORT_PATH="${EXPORT_DIR}/${DB_NAME}_${TIMESTAMP}"

# MongoDB Connection (set via environment variables or use defaults)
MONGODB_URI="${MONGODB_URI:-mongodb://localhost:27017}"
MONGODB_USER="${MONGODB_USER:-}"
MONGODB_PASSWORD="${MONGODB_PASSWORD:-}"
AUTH_DB="${AUTH_DB:-admin}"

echo "========================================="
echo "MongoDB Export Script"
echo "========================================="
echo "Database: $DB_NAME"
echo "Export Path: $EXPORT_PATH"
echo "MongoDB URI: ${MONGODB_URI%%@*}@***"  # Hide credentials in output
echo "========================================="

# Create export directory
mkdir -p "$EXPORT_PATH"

# Build authentication parameters
AUTH_PARAMS=""
if [ -n "$MONGODB_USER" ] && [ -n "$MONGODB_PASSWORD" ]; then
    AUTH_PARAMS="--username $MONGODB_USER --password $MONGODB_PASSWORD --authenticationDatabase $AUTH_DB"
fi

# Get list of collections
echo "Fetching collection list from $DB_NAME..."

if command -v mongosh &> /dev/null; then
    # Using mongosh (MongoDB 5.0+)
    COLLECTIONS=$(mongosh "$MONGODB_URI/$DB_NAME" $AUTH_PARAMS --quiet --eval "db.getCollectionNames().join('\n')")
elif command -v mongo &> /dev/null; then
    # Using legacy mongo shell
    COLLECTIONS=$(mongo "$MONGODB_URI/$DB_NAME" $AUTH_PARAMS --quiet --eval "db.getCollectionNames().join('\n')")
else
    # Use Docker with mongosh
    echo "Using Docker to run mongosh..."
    COLLECTIONS=$(docker run --rm mongo:latest mongosh "$MONGODB_URI/$DB_NAME" $AUTH_PARAMS --quiet --eval "db.getCollectionNames().join('\n')")
fi

if [ -z "$COLLECTIONS" ]; then
    echo "Error: No collections found or unable to connect to database"
    exit 1
fi

echo "Found collections:"
echo "$COLLECTIONS"
echo ""

# Export each collection
COLLECTION_COUNT=0
TOTAL_DOCS=0

for COLLECTION in $COLLECTIONS; do
    echo "Exporting collection: $COLLECTION"
    
    OUTPUT_FILE="${EXPORT_PATH}/${COLLECTION}.json"
    
    if command -v mongoexport &> /dev/null; then
        # Using local mongoexport
        mongoexport --uri="$MONGODB_URI" \
            --db="$DB_NAME" \
            --collection="$COLLECTION" \
            $AUTH_PARAMS \
            --out="$OUTPUT_FILE" \
            --jsonArray \
            --pretty
    else
        # Using Docker with mongoexport
        echo "Using Docker to run mongoexport..."
        docker run --rm -v "$(pwd):/backup" mongo:latest \
            mongoexport --uri="$MONGODB_URI" \
            --db="$DB_NAME" \
            --collection="$COLLECTION" \
            $AUTH_PARAMS \
            --out="/backup/${OUTPUT_FILE}" \
            --jsonArray \
            --pretty
    fi
    
    if [ -f "$OUTPUT_FILE" ]; then
        DOC_COUNT=$(grep -c '"_id"' "$OUTPUT_FILE" || echo "0")
        FILE_SIZE=$(du -h "$OUTPUT_FILE" | cut -f1)
        echo "  ✓ Exported $DOC_COUNT documents ($FILE_SIZE)"
        COLLECTION_COUNT=$((COLLECTION_COUNT + 1))
        TOTAL_DOCS=$((TOTAL_DOCS + DOC_COUNT))
    else
        echo "  ✗ Export failed for $COLLECTION"
    fi
    echo ""
done

# Create metadata file
METADATA_FILE="${EXPORT_PATH}/export_metadata.json"
cat > "$METADATA_FILE" << EOF
{
  "database": "$DB_NAME",
  "export_date": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "mongodb_uri": "${MONGODB_URI%%\?*}",
  "total_collections": $COLLECTION_COUNT,
  "total_documents": $TOTAL_DOCS,
  "collections": [
$(echo "$COLLECTIONS" | sed 's/^/    "/' | sed 's/$/",/' | sed '$ s/,$//')
  ]
}
EOF

echo "========================================="
echo "Export Complete!"
echo "========================================="
echo "Exported: $COLLECTION_COUNT collections"
echo "Total Documents: $TOTAL_DOCS"
echo "Location: $EXPORT_PATH"
echo "========================================="
echo ""
echo "Files created:"
ls -lh "$EXPORT_PATH"

# Create compressed archive
ARCHIVE_FILE="${EXPORT_DIR}/${DB_NAME}_${TIMESTAMP}.tar.gz"
echo ""
echo "Creating compressed archive: $ARCHIVE_FILE"
tar -czf "$ARCHIVE_FILE" -C "$EXPORT_DIR" "$(basename "$EXPORT_PATH")"
echo "✓ Archive created: $(du -h "$ARCHIVE_FILE" | cut -f1)"
echo ""
echo "To import this data, use: ./import_mongodb.sh $EXPORT_PATH"
