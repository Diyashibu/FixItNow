from fastapi import APIRouter, HTTPException, Form, File, UploadFile, Depends
from clients.supabase_client import supabase
from config.settings import SUPABASE_URL
from typing import Optional
import uuid
import os

router = APIRouter()

@router.post("/report-issue")
async def report_issue(
    description: str = Form(...),
    category: str = Form(...),
    intensity: int = Form(...),
    location: str = Form(...),
    user_id: str = Form(None),  # Add user_id parameter
    photo: UploadFile = File(None)
):
    try:
        photo_url = None

        if photo:
            # Validate file type
            if not photo.content_type or not photo.content_type.startswith('image/'):
                raise HTTPException(status_code=400, detail="Only image files are allowed")
            
            # Validate file size (5MB max)
            contents = await photo.read()
            if len(contents) > 5 * 1024 * 1024:  # 5MB in bytes
                raise HTTPException(status_code=400, detail="File size must be less than 5MB")
            
            # Generate unique filename to avoid conflicts
            file_extension = os.path.splitext(photo.filename)[1] if photo.filename else '.jpg'
            unique_filename = f"{uuid.uuid4()}{file_extension}"
            path = f"issues/{unique_filename}"

            # Upload to Supabase Storage
            try:
                # First, check if the bucket exists
                try:
                    bucket_info = supabase.storage.get_bucket("photos")
                    print(f"Bucket 'photos' found: {bucket_info}")
                except Exception as bucket_error:
                    print(f"Bucket check error: {bucket_error}")
                    # Try to create the bucket if it doesn't exist
                    try:
                        supabase.storage.create_bucket("photos", {"public": True})
                        print("Created 'photos' bucket")
                    except Exception as create_error:
                        print(f"Failed to create bucket: {create_error}")
                        raise HTTPException(status_code=500, detail="Storage bucket not available")

                # Upload the file
                upload_response = supabase.storage.from_("photos").upload(path, contents)
                print(f"Upload response: {upload_response}")
                
                # Generate public URL using environment variable
                if SUPABASE_URL:
                    photo_url = f"{SUPABASE_URL}/storage/v1/object/public/photos/{path}"
                else:
                    # Fallback to hardcoded URL if env var not set
                    photo_url = f"https://hwkjkmzwspmgfjqloypj.supabase.co/storage/v1/object/public/photos/{path}"
                    
                print(f"Generated photo URL: {photo_url}")
                
            except Exception as upload_error:
                print(f"Photo upload error: {upload_error}")
                # Don't fail the entire request if photo upload fails
                photo_url = None

        # Prepare issue data
        issue_data = {
            "title": description[:50] + "..." if len(description) > 50 else description,
            "description": description,
            "category": category,
            "scale": intensity,
            "location": location,
            "photo_url": photo_url,
            "status": "pending",  # Set default status
            "upvotes": 0  # Set default upvotes
        }
        
        # Add user_id if provided
        if user_id:
            issue_data["user_id"] = user_id

        # Insert into Supabase table
        res = supabase.table("issues").insert(issue_data).execute()
        
        if not res.data:
            raise HTTPException(status_code=500, detail="Failed to create issue record")

        return {
            "message": "Issue reported successfully", 
            "data": res.data,
            "photo_uploaded": photo_url is not None
        }

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in report_issue: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
