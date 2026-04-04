from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from google.oauth2 import id_token
from google.auth.transport import requests
from backend.app.db.mongodb import db

router = APIRouter(prefix="/auth", tags=["auth"])

# Google OAuth Client ID
GOOGLE_CLIENT_ID = "874807563899-6fv6stnt81m92cmm6fedocojj0748fd3.apps.googleusercontent.com"

class GoogleAuthRequest(BaseModel):
    id_token: str

class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    role: str
    sport: str
    profile_image: str | None = None

@router.post("/google", response_model=UserResponse)
async def google_auth(request: GoogleAuthRequest):
    """
    Authenticate user with Google ID token.
    Creates new user if first login, otherwise returns existing user.
    """
    try:
        # Verify the Google ID token
        idinfo = id_token.verify_oauth2_token(
            request.id_token,
            requests.Request(),
            GOOGLE_CLIENT_ID
        )
        print(f"idinfo: {idinfo}")
        # Get user info from token
        google_email = idinfo.get('email')
        google_name = idinfo.get('name', 'User')
        google_picture = idinfo.get('picture', '')
        
        if not google_email:
            raise HTTPException(status_code=400, detail="Email not found in Google token")
        
        # Get database
        database = db.get_db()
        
        # Check if user exists in database
        existing_user = await database["users"].find_one({"email": google_email})
        
        if existing_user:
            # Return existing user
            user_id = str(existing_user.get("_id", existing_user.get("id", "")))
            return UserResponse(
                id=user_id,
                name=existing_user.get("name", google_name),
                email=existing_user["email"],
                role=existing_user.get("role", "athlete"),
                sport=existing_user.get("sport", "Badminton"),
                profile_image=existing_user.get("profile_image", google_picture)
            )
        else:
            # Create new user
            new_user = {
                "name": google_name,
                "email": google_email,
                "username": google_email.split("@")[0],
                "role": "athlete",
                "sport": "Badminton",
                "profile_image": google_picture,
                "bio": f"Welcome to Podium, {google_name}!",
                "location": "",
                "achievements": [],
                "google_auth": True
            }
            
            result = await database["users"].insert_one(new_user)
            
            return UserResponse(
                id=str(result.inserted_id),
                name=google_name,
                email=google_email,
                role="athlete",
                sport="Badminton",
                profile_image=google_picture
            )
            
    except ValueError as e:
        # Invalid token
        raise HTTPException(status_code=401, detail=f"Invalid Google token: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Authentication failed: {str(e)}")
