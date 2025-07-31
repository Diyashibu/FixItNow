from fastapi import APIRouter, HTTPException, Form, File, UploadFile
from clients.supabase_client import supabase

router = APIRouter()

@router.post("/report-issue")
async def report_issue(
    description: str = Form(...),
    category: str = Form(...),
    intensity: int = Form(...),
    location: str = Form(...),
    photo: UploadFile = File(None)
):
    try:
        photo_url = None

        if photo:
            contents = await photo.read()
            path = f"issues/{photo.filename}"
            supabase.storage.from_("photos").upload(path, contents)
            photo_url = f"https://hwkjkmzwspmgfjqloypj.supabase.co/storage/v1/object/public/photos/{path}"

        res = supabase.table("issues").insert({
            "description": description,
            "category": category,
            "scale": intensity,  # Frontend sends 'intensity', DB expects 'scale'
            "location": location,
            "photo_url": photo_url
        }).execute()

        return {"message": "Issue reported successfully", "data": res.data}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))