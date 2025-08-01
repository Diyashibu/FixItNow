#!/usr/bin/env python3
"""
Storage Setup Script for FixItNow Application
This script helps set up the Supabase storage bucket with proper configuration.
"""

from clients.supabase_client import supabase
import sys

def setup_storage_bucket():
    """Set up the photos bucket with proper configuration."""
    try:
        print("🔧 Setting up Supabase storage bucket...")
        
        # Check if bucket already exists
        try:
            bucket_info = supabase.storage.get_bucket("photos")
            print(f"✅ Bucket 'photos' already exists!")
            print(f"   - Public: {bucket_info.public}")
            print(f"   - ID: {bucket_info.id}")
            return True
        except Exception as e:
            print(f"📦 Bucket 'photos' doesn't exist. Creating it...")
            
        # Create the bucket with public access
        try:
            result = supabase.storage.create_bucket(
                "photos",
                {
                    "public": True,
                    "allowedMimeTypes": ["image/jpeg", "image/jpg", "image/png", "image/gif", "image/webp"],
                    "fileSizeLimit": 5242880  # 5MB in bytes
                }
            )
            print("✅ Successfully created 'photos' bucket!")
            print("   - Public access: Enabled")
            print("   - File size limit: 5MB")
            print("   - Allowed types: JPEG, JPG, PNG, GIF, WebP")
            return True
            
        except Exception as create_error:
            print(f"❌ Failed to create bucket: {create_error}")
            return False
            
    except Exception as e:
        print(f"❌ Error during bucket setup: {e}")
        return False

def test_storage_connection():
    """Test the storage connection."""
    try:
        print("\n🧪 Testing storage connection...")
        buckets = supabase.storage.list_buckets()
        print(f"✅ Successfully connected to storage!")
        print(f"   Available buckets: {[bucket.name for bucket in buckets]}")
        return True
    except Exception as e:
        print(f"❌ Storage connection failed: {e}")
        return False

def setup_storage_policies():
    """Set up storage policies for public access."""
    print("\n🔐 Setting up storage policies...")
    print("NOTE: You need to manually set up the following policies in your Supabase dashboard:")
    print("1. Go to Storage > Policies in your Supabase dashboard")
    print("2. Create a new policy for the 'photos' bucket:")
    print("   - Policy name: 'Public read access'")
    print("   - Operation: SELECT")
    print("   - Target roles: public")
    print("   - USING expression: true")
    print("3. Create another policy:")
    print("   - Policy name: 'Authenticated users can upload'")
    print("   - Operation: INSERT")
    print("   - Target roles: authenticated")
    print("   - USING expression: true")
    print("4. Create another policy:")
    print("   - Policy name: 'Users can update own files'")
    print("   - Operation: UPDATE")
    print("   - Target roles: authenticated")
    print("   - USING expression: auth.uid()::text = (storage.foldername(name))[1]")

def main():
    """Main setup function."""
    print("🚀 FixItNow Storage Setup")
    print("=" * 50)
    
    # Test connection
    if not test_storage_connection():
        print("\n❌ Please check your Supabase credentials in .env file")
        sys.exit(1)
    
    # Setup bucket
    if not setup_storage_bucket():
        print("\n❌ Bucket setup failed!")
        sys.exit(1)
    
    # Show policy instructions
    setup_storage_policies()
    
    print("\n✅ Storage setup completed!")
    print("\n📝 Next steps:")
    print("1. Set up the storage policies manually in Supabase dashboard (see instructions above)")
    print("2. Update your .env file with correct Supabase credentials")
    print("3. Restart your backend server")
    print("4. Test image upload functionality")

if __name__ == "__main__":
    main()