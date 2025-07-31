if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from clients.supabase_client import supabase
from passlib.context import CryptContext
from typing import Optional
from routes import issues

app = FastAPI(title="FixItNow API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", 
        "http://localhost:5173", 
        "http://localhost:5174",
        "http://localhost:5175",
        "http://localhost:5176",
        "http://localhost:5177",
        "http://localhost:5178",
        "http://localhost:5179",
        "http://localhost:5180"
    ], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(issues.router)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



class UserSignup(BaseModel):
    email: EmailStr
    password: str
    username: str  


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class AuthorityLogin(BaseModel):
    username: str
    password: str



def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)



@app.post("/user/signup")
def user_signup(payload: UserSignup):
   
    try:
        res = supabase.auth.sign_up({
            "email": payload.email,
            "password": payload.password
        })
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Auth signup failed: {e}")

    user_obj = res.user
    if not user_obj:
        raise HTTPException(status_code=400, detail="Signup failed; no user returned.")

   
    try:
        supabase.table("users").insert({
            "id": user_obj.id,          
            "email": payload.email,
            "username": payload.username
        }).execute()
    except Exception as e:
       
        raise HTTPException(status_code=500, detail=f"Failed to store user metadata: {e}")

    return {
        "message": "User signup successful",
        "user_id": user_obj.id,
        "email": payload.email
    }


@app.post("/user/login")
def user_login(payload: UserLogin):
    try:
        res = supabase.auth.sign_in_with_password({
            "email": payload.email,
            "password": payload.password
        })
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    session = getattr(res, "session", None)
    if not session:
        raise HTTPException(status_code=401, detail="Login failed; no session returned.")

    return {
        "message": "User login successful",
        "access_token": session.access_token,
        "refresh_token": session.refresh_token,
        "expires_at": session.expires_at
    }



@app.post("/authority/login")
def authority_login(payload: AuthorityLogin):
    
    response = supabase.table("authority").select("*").eq("username", payload.username).limit(1).execute()
    data = response.data
    if not data or len(data) == 0:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    auth_record = data[0]
    stored_hashed = auth_record.get("password_hash")  

    if not stored_hashed or not verify_password(payload.password, stored_hashed):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    
    if not auth_record.get("approved", False):
        raise HTTPException(status_code=403, detail="Authority not approved yet")

   
    return {
        "message": "Authority login successful",
        "authority_id": auth_record.get("id"),
        "username": auth_record.get("username")
    }



class AuthorityCreate(BaseModel):
    username: str
    password: str
    approved: Optional[bool] = False  


@app.post("/authority/create")
def create_authority(payload: AuthorityCreate):
    hashed = hash_password(payload.password)
    try:
        res = supabase.table("authority").insert({
            "username": payload.username,
            "password_hash": hashed,
            "approved": payload.approved
        }).execute()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create authority: {e}")
    return {"message": "Authority record created", "data": res.data}



@app.get("/user/profile")
def user_profile(token: str):

    user = supabase.auth.get_user(token)
    if not getattr(user, "data", None):
        raise HTTPException(status_code=401, detail="Invalid token")
    return user.data
