# User Images Setup - S3 Integration

## Overview

All user profiles now have profile and cover images. Images are stored using a combination of:
1. **S3 Bucket** - Custom generated images uploaded to your AWS S3 bucket
2. **CDN Placeholders** - High-quality Unsplash images for remaining users

## Current Image Setup

### Images Stored in S3 Bucket

| User | Profile Image | Cover Image |
|------|---------------|-------------|
| athlete1 (PV Sindhu) | ✅ S3 | ✅ S3 |
| athlete2 (Kento Momota) | ✅ S3 | ✅ S3 |
| athlete3 (An Se Young) | ✅ S3 | CDN Placeholder |

### Images from CDN (Unsplash)

| User | Profile Image | Cover Image |
|------|---------------|-------------|
| athlete4 (Viktor Axelsen) | Unsplash | Unsplash |
| athlete5 (Lee Chong Wei) | Unsplash | Unsplash |
| coach1 (Pullela Gopichand) | Unsplash | Unsplash |
| coach2 (Park Joo-bong) | Unsplash | Unsplash |

## S3 Bucket Structure

```
podium-bucket-ikjas/
├── profiles/
│   ├── athlete1_profile.png  (PV Sindhu)
│   ├── athlete2_profile.png  (Kento Momota)
│   └── athlete3_profile.png  (An Se Young)
└── covers/
    ├── athlete1_cover.png    (PV Sindhu) 
    └── athlete2_cover.png    (Kento Momota)
```

## Scripts Created

### 1. upload_images_to_s3.py
Uploads generated images from the artifacts directory to S3 bucket.

**Usage:**
```bash
python backend/upload_images_to_s3.py
```

**Features:**
- Uploads profile and cover images to S3
- Organizes files in `profiles/` and `covers/` folders
- Returns public URLs for uploaded images
- Handles errors gracefully

### 2. update_user_images.py
Updates MongoDB users collection with image URLs (S3 + CDN placeholders).

**Usage:**
```bash
python backend/update_user_images.py
```

**Features:**
- Updates all 7 users with profile and cover image URLs
- Verifies updates after completion
- Shows status for each user

## Generated Images

The following images were AI-generated and uploaded to S3:

1. **PV Sindhu Profile** - Female Indian badminton athlete portrait
2. **PV Sindhu Cover** - Professional badminton court background
3. **Kento Momota Profile** - Male Japanese badminton athlete portrait
4. **Kento Momota Cover** - Modern training facility
5. **An Se Young Profile** - Female Korean badminton athlete portrait

## Adding More S3 Images

To replace the placeholder images with custom S3 images:

### Step 1: Generate or Obtain Images

You can either:
- Use AI image generation
- Take actual photos
- Use stock photos (with proper licensing)

### Step 2: Save Images

Save images to a local directory with naming pattern:
- `{user_id}_profile.png` for profile images
- `{user_id}_cover.png` for cover images

### Step 3: Upload to S3

Update `upload_images_to_s3.py` to include your new images:

```python
images = [
    (Path("path/to/viktor_profile.png"), "profiles/athlete4_profile.png", "athlete4", "profile"),
    (Path("path/to/viktor_cover.png"), "covers/athlete4_cover.png", "athlete4", "cover"),
]
```

Then run:
```bash
python backend/upload_images_to_s3.py
```

### Step 4: Update Database

Update `update_user_images.py` with the new S3 URLs:

```python
"athlete4": {
    "profile_image": f"{S3_BASE}/profiles/athlete4_profile.png",
    "cover_image": f"{S3_BASE}/covers/athlete4_cover.png"
}
```

Then run:
```bash
python backend/update_user_images.py
```

## Image Requirements

### Profile Images
- **Recommended Size:** 400x400px (square)
- **Format:** PNG or JPG
- **Content:** Headshot or portrait photo
- **File Size:** < 2MB for optimal loading

### Cover Images
- **Recommended Size:** 1920x400px (panoramic)
- **Format:** PNG or JPG
- **Content:** Landscape or background image
- **File Size:** < 3MB for optimal loading

## S3 Configuration

Make sure your `.env` file has the following variables set:

```env
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=ap-south-1
S3_BUCKET_NAME=podium-bucket-ikjas
```

## Image URLs

All image URLs follow this pattern:

**S3 Images:**
```
https://podium-bucket-ikjas.s3.ap-south-1.amazonaws.com/profiles/{user_id}_profile.png
https://podium-bucket-ikjas.s3.ap-south-1.amazonaws.com/covers/{user_id}_cover.png
```

**Unsplash Placeholders:**
```
https://images.unsplash.com/photo-{id}?w=800&h=800&fit=crop
```

## Verification

To verify images are correctly set:

1. **Check MongoDB:**
```bash
python backend/verify_data.py
```

2. **Check Frontend:**
Navigate to: http://localhost:4200/app/profile

3. **Check S3 Bucket:**
Visit AWS S3 Console and browse the `podium-bucket-ikjas` bucket

## Troubleshooting

### Images Not Displaying

1. **Check S3 bucket permissions** - Ensure bucket allows public read access
2. **Check CORS settings** - S3 bucket should allow cross-origin requests
3. **Check image URLs** - Verify URLs in MongoDB match S3 URLs
4. **Check network tab** - Look for 404 or 403 errors in browser console

### Slow Image Loading

1. **Optimize image sizes** - Compress images before uploading
2. **Use CloudFront** - Add CDN in front of S3 for faster delivery
3. **Lazy loading** - Implement image lazy loading in frontend

## Next Steps

1. **Replace all placeholders** - Generate/upload images for remaining 4 users
2. **Optimize images** - Compress images to reduce file sizes
3. **Add image variants** - Create thumbnails for faster loading
4. **Implement caching** - Add browser caching headers to S3 objects

---

**Last Updated:** 2025-11-28  
**Images in S3:** 5 (3 profile + 2 cover)  
**Placeholder Images:** 9 (4 profile + 5 cover)
