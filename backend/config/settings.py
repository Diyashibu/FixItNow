import os
from dotenv import load_dotenv

load_dotenv()

# Use environment variables if available, otherwise fallback to hardcoded values
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://hwkjkmzwspmgfjqloypj.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imh3a2prbXp3c3BtZ2ZqcWxveXBqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTM5NDQzMjcsImV4cCI6MjA2OTUyMDMyN30.RUKxX-ohXGVRoX6sr0t2Cf6vWefnreuDl8LSs5DDTns")
