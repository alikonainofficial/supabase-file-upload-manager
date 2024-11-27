"""
Supabase Storage Folder Deletion Script

This script connects to a Supabase project and allows for the deletion of all files
within a specified folder in a given storage bucket. It uses the Supabase Python client
and environment variables for configuration.

Functionality:
- Connects to a Supabase instance using `SUPABASE_URL` and `SUPABASE_KEY` from environment variables.
- Deletes all files within a specified folder inside a Supabase storage bucket.
- Validates folder contents and handles errors appropriately.

Dependencies:
- `os` for environment variable management.
- `supabase` Python client for interacting with Supabase.
- `dotenv` for loading environment variables from a `.env` file.

Usage:
1. Set up a `.env` file containing:
    SUPABASE_URL=<your_supabase_url>
    SUPABASE_KEY=<your_supabase_api_key>
2. Update the `bucket_name` and `folder_name` variables in the `__main__` block.
3. Run the script to delete all files in the specified folder.

Functions:
- `delete_folder(bucket_name, folder_name)`: Deletes all files in the specified folder within a Supabase storage bucket.

Example:
    $ python delete_folder.py
    Folder 'bucket_folder_name' is empty, does not exist, or an error occurred.
    Deleted: ['bucket_folder_name/file1.txt', 'bucket_folder_name/file2.txt']
    All files in folder 'bucket_folder_name' have been deleted.
"""

import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def delete_folder(bucket_name, folder_name):
    """
    Deletes all files in a specified folder within a Supabase storage bucket.

    Args:
        bucket_name (str): The name of the Supabase storage bucket.
        folder_name (str): The folder path inside the bucket to delete.
    """
    # Initialize response
    response = None
    try:
        # List all files in the folder
        response = supabase.storage.from_(bucket_name).list(folder_name, {"limit": 10000})
        print(response)
        # Check if the response is valid
        if not response or not isinstance(response, list):
            print(f"Folder '{folder_name}' is empty, does not exist, or an error occurred.")
            return

        file_path_list = [f"{folder_name}/{file['name']}" for file in response]

        delete_response = supabase.storage.from_(bucket_name).remove(file_path_list)

        if delete_response["httpStatusCode"] == 200:
            print(f"Deleted: {file_path_list}")
        else:
            print(f"Failed to delete: {file_path_list}")

        print(f"All files in folder '{folder_name}' have been deleted.")
    except Exception as e:
        print(f"An error occurred while deleting folder '{folder_name}': {e}")


if __name__ == "__main__":
    bucket_name = "bucket_name"
    folder_name = "bucket_folder_name"

    delete_folder(bucket_name, folder_name)
