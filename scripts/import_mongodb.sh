#!/bin/bash

# MongoDB Import Script
# Imports JSON files into a MongoDB database

set -e  # Exit on error

# Configuration
IMPORT_DIR="${1:-}"
DB_NAME="${DB_NAME:-podium_db}"

# MongoDB Connection (set via environment variables or use defaults)
MONGODB_URI="${MONGODB_URI:-mongodb://localhost:27017}"
MONGODB_USER="${MONGODB_USER:-}"
MONGODB_PASSWORD="${MONGODB_PASSWORD:-}"
AUTH_DB="${AUTH_DB:-admin}"

# Options
DROP_COLLECTIONS="${DROP_COLLECTIONS:-false}"  # Set to 'true' to drop existing collections before import

echo "========================================="
echo "MongoDB Import Script"
echo "========================================="

# Check if import directory is provided
if [ -z "$IMPORT_DIR" ]; then
    echo "Error: Import directory not specified"
    echo ""
    echo "Usage: $0 <import_directory>"
    echo ""
    echo "Example:"
    echo "  $0 ./mongodb_export/podium_db_20241130_123456"
    echo ""
    echo "Environment Variables:"
    echo "  MONGODB_URI          - MongoDB connection URI (default: mongodb://localhost:27017)"
    echo "  DB_NAME              - Target database name (default: podium_db)"
    echo "  MONGODB_USER         - MongoDB username (optional)"
    echo "  MONGODB_PASSWORD     - MongoDB password (optional)"
    echo "  AUTH_DB              - Authentication database (default: admin)"
    echo "  DROP_COLLECTIONS     - Drop existing collections before import (default: false)"
    exit 1
fi

# Check if directory exists
if [ ! -d "$IMPORT_DIR" ]; then
    echo "Error: Directory not found: $IMPORT_DIR"
    exit 1
fi

echo "Import Directory: $IMPORT_DIR"
echo "Target Database: $DB_NAME"
echo "MongoDB URI: ${MONGODB_URI%%@*}@***"  # Hide credentials in output
echo "Drop Collections: $DROP_COLLECTIONS"
echo "========================================="

# Build authentication parameters
AUTH_PARAMS=""
if [ -n "$MONGODB_USER" ] && [ -n "$MONGODB_PASSWORD" ]; then
    AUTH_PARAMS="--username $MONGODB_USER --password $MONGODB_PASSWORD --authenticationDatabase $AUTH_DB"
fi

# Read metadata if available
METADATA_FILE="${IMPORT_DIR}/export_metadata.json"
if [ -f "$METADATA_FILE" ]; then
    echo ""
    echo "Export Metadata:"
    cat "$METADATA_FILE"
    echo ""
fi

# Find all JSON files (excluding metadata)
JSON_FILES=$(find "$IMPORT_DIR" -name "*.json" ! -name "export_metadata.json" -type f)

if [ -z "$JSON_FILES" ]; then
    echo "Error: No JSON files found in $IMPORT_DIR"
    exit 1
fi

FILE_COUNT=$(echo "$JSON_FILES" | wc -l)
echo "Found $FILE_COUNT collection file(s) to import"
echo ""

# Import each collection
IMPORTED_COUNT=0
TOTAL_DOCS=0

for JSON_FILE in $JSON_FILES; do
    # Extract collection name from filename
    COLLECTION=$(basename "$JSON_FILE" .json)
    
    echo "Importing collection: $COLLECTION"
    echo "  Source: $(basename "$JSON_FILE")"
    
    # Drop collection if requested
    if [ "$DROP_COLLECTIONS" = "true" ]; then
        echo "  Dropping existing collection..."
        if command -v mongosh &> /dev/null; then
            mongosh "$MONGODB_URI/$DB_NAME" $AUTH_PARAMS --quiet --eval "db.$COLLECTION.drop()"
        elif command -v mongo &> /dev/null; then
            mongo "$MONGODB_URI/$DB_NAME" $AUTH_PARAMS --quiet --eval "db.$COLLECTION.drop()"
        else
            docker run --rm mongo:latest mongosh "$MONGODB_URI/$DB_NAME" $AUTH_PARAMS --quiet --eval "db.$COLLECTION.drop()"
        fi
    fi
    
    # Import the collection
    if command -v mongoimport &> /dev/null; then
        # Using local mongoimport
        RESULT=$(mongoimport --uri="$MONGODB_URI" \
            --db="$DB_NAME" \
            --collection="$COLLECTION" \
            $AUTH_PARAMS \
            --file="$JSON_FILE" \
            --jsonArray \
            2>&1)
    else
        # Using Docker with mongoimport
        echo "  Using Docker to run mongoimport..."
        DOCKER_PATH="/backup/$(realpath --relative-to="$(pwd)" "$JSON_FILE")"
        RESULT=$(docker run --rm -v "$(pwd):/backup" mongo:latest \
            mongoimport --uri="$MONGODB_URI" \
            --db="$DB_NAME" \
            --collection="$COLLECTION" \
            $AUTH_PARAMS \
            --file="$DOCKER_PATH" \
            --jsonArray \
            2>&1)
    fi
    
    # Extract imported document count from result
    DOC_COUNT=$(echo "$RESULT" | grep -oP '\d+(?= document)' | tail -1 || echo "0")
    
    if [ -n "$DOC_COUNT" ] && [ "$DOC_COUNT" -gt 0 ]; then
        echo "  ✓ Imported $DOC_COUNT documents"
        IMPORTED_COUNT=$((IMPORTED_COUNT + 1))
        TOTAL_DOCS=$((TOTAL_DOCS + DOC_COUNT))
    else
        echo "  ⚠ Import completed but document count unclear"
        echo "$RESULT"
    fi
    echo ""
done

# Verify imports
echo "========================================="
echo "Import Complete!"
echo "========================================="
echo "Imported: $IMPORTED_COUNT collections"
echo "Total Documents: $TOTAL_DOCS"
echo "========================================="
echo ""
echo "Verifying collections in $DB_NAME..."

if command -v mongosh &> /dev/null; then
    mongosh "$MONGODB_URI/$DB_NAME" $AUTH_PARAMS --eval "
        print('\\nCollections and document counts:');
        db.getCollectionNames().forEach(function(coll) {
            var count = db[coll].countDocuments();
            print('  ' + coll + ': ' + count + ' documents');
        });
    "
elif command -v mongo &> /dev/null; then
    mongo "$MONGODB_URI/$DB_NAME" $AUTH_PARAMS --eval "
        print('\\nCollections and document counts:');
        db.getCollectionNames().forEach(function(coll) {
            var count = db[coll].count();
            print('  ' + coll + ': ' + count + ' documents');
        });
    "
else
    docker run --rm mongo:latest mongosh "$MONGODB_URI/$DB_NAME" $AUTH_PARAMS --eval "
        print('\\nCollections and document counts:');
        db.getCollectionNames().forEach(function(coll) {
            var count = db[coll].countDocuments();
            print('  ' + coll + ': ' + count + ' documents');
        });
    "
fi

echo ""
echo "Import completed successfully!"
