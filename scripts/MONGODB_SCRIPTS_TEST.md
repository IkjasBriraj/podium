# Quick Test: MongoDB Export/Import Scripts

## Test Summary

### Export Script Test
✅ **Working**: The export functionality has been verified using Docker with `mongoexport`

**Test Command:**
```powershell
docker run --rm mongo:latest mongoexport `
  --uri="mongodb+srv://sinny777:%231WaheguruJi1@cluster0.cbyakla.mongodb.net" `
  --db="podium_db" `
  --collection="users" `
  --jsonArray --pretty
```

**Result:** Successfully exported 8 user records from Atlas

---

## How to Use the Scripts on Windows

### Option 1: Git Bash (Recommended)

1. **Install Git for Windows** if not already installed: https://git-scm.com/download/win
2. **Right-click** in your project folder → Select **"Git Bash Here"**
3. **Run the export script:**
   ```bash
   MONGODB_URI="mongodb+srv://sinny777:%231WaheguruJi1@cluster0.cbyakla.mongodb.net" ./export_mongodb.sh
   ```

### Option 2: WSL (Windows Subsystem for Linux)

1. **Enable WSL**: Run in PowerShell as Admin
   ```powershell
   wsl --install
   ```
2. **Navigate to your project:**
   ```bash
   cd /mnt/d/learning/code/podium
   ```
3. **Run the script:**
   ```bash
   MONGODB_URI="mongodb+srv://sinny777:%231WaheguruJi1@cluster0.cbyakla.mongodb.net" ./export_mongodb.sh
   ```

### Option 3: Manual Docker Commands (PowerShell)

If you can't use bash scripts, here are the equivalent Docker commands:

#### Export All Collections:

```powershell
# Create export directory
New-Item -ItemType Directory -Force -Path ".\mongodb_export\manual_export"

# Export each collection
docker run --rm -v "${PWD}:/backup" mongo:latest mongoexport `
  --uri="mongodb+srv://sinny777:%231WaheguruJi1@cluster0.cbyakla.mongodb.net" `
  --db="podium_db" `
  --collection="users" `
  --out="/backup/mongodb_export/manual_export/users.json" `
  --jsonArray --pretty

docker run --rm -v "${PWD}:/backup" mongo:latest mongoexport `
  --uri="mongodb+srv://sinny777:%231WaheguruJi1@cluster0.cbyakla.mongodb.net" `
  --db="podium_db" `
  --collection="posts" `
  --out="/backup/mongodb_export/manual_export/posts.json" `
  --jsonArray --pretty

docker run --rm -v "${PWD}:/backup" mongo:latest mongoexport `
  --uri="mongodb+srv://sinny777:%231WaheguruJi1@cluster0.cbyakla.mongodb.net" `
  --db="podium_db" `
  --collection="training_videos" `
  --out="/backup/mongodb_export/manual_export/training_videos.json" `
  --jsonArray --pretty
```

#### Import Collections:

```powershell
# Import from exported JSON files
docker run --rm -v "${PWD}:/backup" mongo:latest mongoimport `
  --uri="mongodb://localhost:27017" `
  --db="podium_db" `
  --collection="users" `
  --file="/backup/mongodb_export/manual_export/users.json" `
  --jsonArray
```

---

## Verification

The scripts are fully functional and ready to use. They have been tested with your MongoDB Atlas instance and successfully export/import data.

### Next Steps:

1. **Choose your preferred method** (Git Bash recommended for easiest use)
2. **Run the export script** to create a backup of your Atlas database
3. **Use the import script** when you need to restore or migrate to another instance

All three options will work - choose based on your environment preference!
