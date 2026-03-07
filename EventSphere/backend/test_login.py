from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

supabase = create_client(url, key)

'''response = supabase.auth.sign_in_with_password({
    "email": "admin@test.com",
    "password": "123456"
})'''

'''response = supabase.auth.sign_in_with_password({
    "email": "participant1@test.com",
    "password": "123456"
})'''

response = supabase.auth.sign_in_with_password({
    "email": "judge1@test.com",
    "password": "123456"
})


print(response.session.access_token)