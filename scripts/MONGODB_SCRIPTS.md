# MongoDB Export/Import Scripts

These bash scripts allow you to export MongoDB data to JSON files and import them to another MongoDB instance.

## Prerequisites

- **Git Bash** or **WSL** (for Windows users)
- **Docker** (if MongoDB tools are not installed locally)
- OR **MongoDB Database Tools** installed locally (`mongoexport`, `mongoimport`, `mongosh`)

## Scripts

### 1. `export_mongodb.sh` - Export MongoDB Data

Exports all collections from a MongoDB database to JSON files.

#### Basic Usage

```bash
./export_mongodb.sh
```

#### With Environment Variables

```bash
# Export from local MongoDB
DB_NAME=podium_db MONGODB_URI=mongodb://localhost:27017 ./export_mongodb.sh

# Export from Atlas with authentication
DB_NAME=podium_db \
MONGODB_URI="mongodb+srv://username:password@cluster.mongodb.net" \
./export_mongodb.sh

# Export with authentication (local MongoDB)
DB_NAME=podium_db \
MONGODB_URI=mongodb://localhost:27017 \
MONGODB_USER=admin \
MONGODB_PASSWORD=P@ssw0rd \
AUTH_DB=admin \
./export_mongodb.sh
```

#### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DB_NAME` | `podium_db` | Database name to export |
| `MONGODB_URI` | `mongodb://localhost:27017` | MongoDB connection URI |
| `MONGODB_USER` | (empty) | MongoDB username |
| `MONGODB_PASSWORD` | (empty) | MongoDB password |
| `AUTH_DB` | `admin` | Authentication database |
| `EXPORT_DIR` | `./mongodb_export` | Directory to store exports |

#### Output

The script creates:
- **JSON files**: One file per collection in `mongodb_export/<db_name>_<timestamp>/`
- **Metadata file**: `export_metadata.json` with export details
- **Compressed archive**: `<db_name>_<timestamp>.tar.gz`

Example output structure:
```
mongodb_export/
├── podium_db_20241130_153000/
│   ├── users.json
│   ├── posts.json
│   ├── training_videos.json
│   ├── comments.json
│   └── export_metadata.json
└── podium_db_20241130_153000.tar.gz
```

---

### 2. `import_mongodb.sh` - Import MongoDB Data

Imports JSON files into a MongoDB database.

#### Basic Usage

```bash
./import_mongodb.sh <import_directory>
```

#### Examples

```bash
# Import to local MongoDB
./import_mongodb.sh ./mongodb_export/podium_db_20241130_153000

# Import to a different database
DB_NAME=podium_production ./import_mongodb.sh ./mongodb_export/podium_db_20241130_153000

# Import to Atlas
MONGODB_URI="mongodb+srv://username:password@cluster.mongodb.net" \
DB_NAME=podium_db \
./import_mongodb.sh ./mongodb_export/podium_db_20241130_153000

# Import and drop existing collections first
DROP_COLLECTIONS=true ./import_mongodb.sh ./mongodb_export/podium_db_20241130_153000
```

#### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DB_NAME` | `podium_db` | Target database name |
| `MONGODB_URI` | `mongodb://localhost:27017` | MongoDB connection URI |
| `MONGODB_USER` | (empty) | MongoDB username |
| `MONGODB_PASSWORD` | (empty) | MongoDB password |
| `AUTH_DB` | `admin` | Authentication database |
| `DROP_COLLECTIONS` | `false` | Drop existing collections before import |

---

## Common Use Cases

### 1. Backup Local Database

```bash
# Export
./export_mongodb.sh

# Save the archive file
cp mongodb_export/podium_db_*.tar.gz ~/backups/
```

### 2. Migrate from Local to Atlas

```bash
# Step 1: Export from local
DB_NAME=podium_db \
MONGODB_URI=mongodb://localhost:27017 \
MONGODB_USER=admin \
MONGODB_PASSWORD=P@ssw0rd \
./export_mongodb.sh

# Step 2: Import to Atlas
MONGODB_URI="mongodb+srv://user:pass@cluster.mongodb.net" \
DB_NAME=podium_db \
./import_mongodb.sh ./mongodb_export/podium_db_20241130_153000
```

### 3. Clone Database

```bash
# Export from source
DB_NAME=podium_prod ./export_mongodb.sh

# Import to destination with different name
DB_NAME=podium_dev ./import_mongodb.sh ./mongodb_export/podium_prod_20241130_153000
```

### 4. Restore from Backup

```bash
# Extract archive
tar -xzf backups/podium_db_20241130_153000.tar.gz -C mongodb_export/

# Import
DROP_COLLECTIONS=true \
./import_mongodb.sh ./mongodb_export/podium_db_20241130_153000
```

---

## Windows Usage

### Option 1: Git Bash

1. Right-click in the project folder
2. Select "Git Bash Here"
3. Run the scripts:
   ```bash
   ./export_mongodb.sh
   ./import_mongodb.sh ./mongodb_export/podium_db_20241130_153000
   ```

### Option 2: WSL (Windows Subsystem for Linux)

```bash
wsl
cd /mnt/d/learning/code/podium
./export_mongodb.sh
```

### Option 3: PowerShell (requires conversion)

The scripts are bash scripts. For PowerShell, you would need to:
- Install Git Bash or WSL
- Or manually run the `mongoexport`/`mongoimport` commands

---

## Troubleshooting

### "Command not found: mongoexport"

The script will automatically fallback to using Docker if MongoDB tools aren't installed locally. Ensure Docker is running.

### "Permission denied"

Make scripts executable:
```bash
chmod +x export_mongodb.sh import_mongodb.sh
```

### "Connection refused"

Check that:
- MongoDB is running
- Connection URI is correct
- Authentication credentials are valid
- Network allows connections (for Atlas, check IP whitelist)

### Docker volume mounting issues (Windows)

If using Docker on Windows, ensure paths are correct:
```bash
# Use absolute paths
docker run --rm -v "d:/learning/code/podium:/backup" mongo:latest ...
```

---

## Notes

- JSON exports are **human-readable** but larger than binary archives
- Use `--jsonArray` format for easier processing
- Exports include all document fields and metadata
- Import preserves `_id` fields from source database
- Set `DROP_COLLECTIONS=true` to completely replace existing data
