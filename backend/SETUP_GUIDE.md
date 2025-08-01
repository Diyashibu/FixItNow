# FixItNow Image Upload Setup Guide 🚀

## 📋 Prerequisites
1. Active Supabase project
2. Python 3.7+ installed
3. Required Python packages installed

## 🔧 Step-by-Step Setup

### 1. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Update the `.env` file in the root directory with your Supabase credentials:

```env
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_ANON_KEY=your_actual_anon_key_here
```

**How to find your credentials:**
1. Go to your [Supabase Dashboard](https://app.supabase.com)
2. Select your project
3. Go to Settings → API
4. Copy the "Project URL" and "anon public" key

### 3. Test Your Connection
```bash
cd backend
python test_connection.py
```

This will verify:
- ✅ Environment variables are set
- ✅ Connection to Supabase works
- ✅ Storage access is available

### 4. Set Up Storage Bucket
```bash
cd backend
python setup_storage.py
```

This will:
- ✅ Create the "photos" bucket if it doesn't exist
- ✅ Configure it for public access
- ✅ Set file size limits (5MB max)
- ✅ Restrict to image files only

### 5. Configure Storage Policies (Manual Step)

**Important:** You need to set up storage policies in your Supabase dashboard:

1. Go to **Storage → Policies** in your Supabase dashboard
2. Create these policies for the "photos" bucket:

#### Policy 1: Public Read Access
- **Policy name:** `Public read access`
- **Operation:** `SELECT`
- **Target roles:** `public`
- **USING expression:** `true`

#### Policy 2: Authenticated Upload
- **Policy name:** `Authenticated users can upload`
- **Operation:** `INSERT`
- **Target roles:** `authenticated`
- **USING expression:** `true`

#### Policy 3: User File Management
- **Policy name:** `Users can update own files`
- **Operation:** `UPDATE`
- **Target roles:** `authenticated`
- **USING expression:** `auth.uid()::text = (storage.foldername(name))[1]`

### 6. Start the Backend Server
```bash
cd backend
uvicorn app:app --reload --host 127.0.0.1 --port 8000
```

### 7. Test Image Upload
1. Go to your frontend application
2. Navigate to "Report Issue" page
3. Try uploading an image
4. Check the backend logs for any errors

## 🐛 Troubleshooting

### Backend Server Won't Start
**Error:** `NameError: name 'Optional' is not defined`
**Fix:** Make sure all imports are correct (this is now fixed)

### Connection Failed
**Error:** Storage connection failed
**Fixes:**
1. Check your `.env` file has correct credentials
2. Verify your Supabase project is active
3. Check internet connection
4. Ensure you're using the correct variable names (`SUPABASE_ANON_KEY`)

### Image Upload Fails
**Possible causes:**
1. **Storage bucket doesn't exist** → Run `python setup_storage.py`
2. **Missing storage policies** → Follow step 5 above
3. **File too large** → Max 5MB allowed
4. **Wrong file type** → Only images allowed (JPG, PNG, GIF, WebP)
5. **Network issues** → Check frontend console for errors

### Images Upload But URLs Don't Work
**Cause:** Storage policies not configured
**Fix:** Complete step 5 (storage policies) in Supabase dashboard

### Database Errors
**Error:** Missing fields in issues table
**Fix:** Make sure your issues table has these columns:
- `id` (uuid, primary key)
- `title` (text)
- `description` (text)
- `category` (text)
- `scale` (int4)
- `location` (text)
- `photo_url` (text, nullable)
- `user_id` (uuid, nullable)
- `status` (text, default: 'pending')
- `upvotes` (int8, default: 0)
- `created_at` (timestamptz)
- `updated_at` (timestamptz)

## 📁 File Structure
```
backend/
├── routes/
│   └── issues.py          # ✅ Updated with image upload
├── config/
│   └── settings.py        # ✅ Fixed environment variables
├── clients/
│   └── supabase_client.py # ✅ Supabase connection
├── test_connection.py     # ✅ New - Test your setup
├── setup_storage.py       # ✅ New - Set up storage bucket
└── .env                   # ✅ Updated - Add your credentials
```

## 🎯 What's Fixed
1. ✅ Import errors resolved
2. ✅ Environment variable naming fixed
3. ✅ File type validation added
4. ✅ File size limits enforced
5. ✅ Unique filename generation
6. ✅ Bucket auto-creation
7. ✅ Better error handling
8. ✅ User ID association
9. ✅ Comprehensive logging

## 📞 Support
If you're still having issues:
1. Check the backend logs for detailed error messages
2. Run `python test_connection.py` to diagnose connection issues
3. Verify your Supabase dashboard settings match the guide
4. Ensure all required policies are set up