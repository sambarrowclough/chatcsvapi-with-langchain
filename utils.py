import os
import supabase
import uuid
from dotenv import load_dotenv
import io

# load env variables
load_dotenv()

supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_API_KEY")
supabase_client = supabase.create_client(supabase_url, supabase_key)
bucket_name = 'public'

def save_file(file_name):
    with open(file_name, 'rb') as f:
        result = supabase_client.storage.from_(bucket_name).upload(file_name, f)
        url = supabase_url + '/storage/v1/object/public/' + bucket_name + '/' + file_name
        os.remove(file_name)
    return url