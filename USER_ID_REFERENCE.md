# User ID Reference Guide

## ✅ Authentication System Now Active

The application now features a fully functional login system. You no longer need to hardcode user IDs in the code.

### How to Switch Users

1. **Logout** using the button in the bottom-left of the sidebar.
2. **Login** with the credentials of the user you want to test.

**Universal Password:** `password123`

## Available Test Users

### Athletes

| User ID | Name | Sport | Username | Email |
|---------|------|-------|----------|-------|
| `athlete1` | PV Sindhu | Badminton | pvsindhu | pv.sindhu@podium.com |
| `athlete2` | Kento Momota | Badminton | kmomota | k.momota@podium.com |
| `athlete3` | An Se Young | Badminton | cseyoung | an.seyoung@podium.com |
| `athlete4` | Viktor Axelsen | Badminton | vaxelsen | v.axelsen@podium.com |
| `athlete5` | Lee Chong Wei | Badminton | lcwei | lc.wei@podium.com |

### Coaches

| User ID | Name | Sport | Username | Email |
|---------|------|-------|----------|-------|
| `coach1` | Pullela Gopichand | Badminton | pmgopichand | p.gopichand@podium.com |
| `coach2` | Park Joo-bong | Badminton | parkjungbong | park.jungbong@podium.com |


## All Users Share the Same Password

**Password:** `password123`

## API Endpoints

You can also access user data directly via API:

- **Single User:** `http://localhost:8000/users/{user_id}`
- **All Users:** `http://localhost:8000/users`
- **User Profile:** `http://localhost:8000/profiles/{user_id}`
- **User Posts:** `http://localhost:8000/users/{user_id}/posts`

### Examples:

```
http://localhost:8000/users/athlete1        # PV Sindhu
http://localhost:8000/users/coach1          # Gopichand
http://localhost:8000/profiles/athlete2     # Kento Momota's profile
```

## Note About the Old ID

The previous mock data used `u1` as the user ID for Lee Chong Wei. The new mock data uses more descriptive IDs:
- `athlete1` through `athlete5` for athletes
- `coach1` through `coach2` for coaches

This makes it easier to identify users in the code and API calls.
