"""
This script facilitates checking and uploading missing files from a local directory
to a Supabase storage bucket. It compares files listed in a CSV with the files
present in the bucket. If files are missing, it provides an option to retry
uploading from a user-specified directory.

Key Features:
- Fetches and compares file lists dynamically.
- Prompts user to retry uploads for missing files.
- Allows specifying the local directory for missing files during retries.
- Includes detailed logging and error handling for improved user feedback.
"""

import json
import os
import csv
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def fetch_file_list_from_bucket(bucket, bucket_dir, limit=10000):
    """
    Fetch the list of files in a specific Supabase storage bucket directory.

    Args:
        bucket (str): The name of the bucket.
        bucket_dir (str): The directory path inside the bucket.
        limit (int): Maximum number of files to fetch.

    Returns:
        set: A set containing filenames from the specified bucket directory.
    """
    try:
        available_files = set()
        zero_byte_files = set()
        offset = 0
        while True:
            response = supabase.storage.from_(bucket).list(
                bucket_dir, {"limit": limit, "offset": offset}
            )
            if not response:
                print(f"Stopping fetch: No more files found.")
                break

            # Check file sizes and add zero-byte files
            for item in response:
                if item.get("metadata") and item.get("metadata").get("size", 0) == 0:
                    zero_byte_files.add(item.get("name", ""))
                available_files.add(item.get("name", ""))

            print(f"Fetched {len(response)} files (offset: {offset}).")

            # Stop if fewer files than the limit were returned (end of results)
            if len(response) < limit:
                break

            # Increment the offset for the next page
            offset += limit

        print(f"Fetched a total of {len(available_files)} files from Supabase storage.")
        return available_files, zero_byte_files

    except Exception as e:
        print(f"Error fetching files from bucket: {e}")
        return set(), set()


def is_file_valid(file_name, file_list, zero_byte_list):
    """
    Check if a file exists in the fetched file list and is not in the list of zero byte files.

    Args:
        file_name (str): Name of the file to check.
        file_list (set): Set of filenames fetched from the bucket.
        zero_byte_list (set): Set of filenames that have 0 byte size.

    Returns:
        bool: True if the file is valid (exists and is not zero-byte), False otherwise.
    """

    return file_name in file_list and not file_name in zero_byte_list


def upload_missing_files(missing_files, directory_path, bucket, bucket_dir, file_extension):
    """
    Upload missing files to Supabase storage.

    Args:
        missing_files (list): List of missing file names.
        directory_path (str): Path to the local directory containing the files.
        bucket (str): Name of the Supabase bucket.
        bucket_dir (str): Directory path in the bucket to upload files to.
    """
    for file_id in missing_files:
        file_name = f"{file_id}.{file_extension}"
        local_file_path = os.path.join(directory_path, file_name)

        # Check if the file exists in the local path
        if os.path.exists(local_file_path):
            try:
                # Upload the file to the Supabase storage
                with open(local_file_path, "rb") as file_data:
                    response = supabase.storage.from_(bucket).upload(
                        f"{bucket_dir}/{file_name}", file_data.read()
                    )

                if response.status_code == 200:
                    print(f"Successfully uploaded: {file_name}")
                else:
                    # Attempt to parse the response content if it is JSON
                    try:
                        error_content = response.json()
                        print(
                            f"Failed to upload {file_name}: {error_content.get('error', 'Unknown error')}"
                        )
                    except json.JSONDecodeError:
                        print(f"Failed to upload {file_name}. Response: {response.text}")

            except Exception as e:
                print(f"An error occurred while uploading {file_name}: {e}")
        else:
            print(f"File {file_name} not found in local directory '{directory_path}'.")


def get_missing_files_from_csv(csv_path, file_list, zero_byte_list, file_extension):
    """
    Identify missing files by comparing IDs in a CSV file against the bucket file list.

    Args:
        csv_path (str): Path to the CSV file.
        file_list (set): Set of filenames fetched from the bucket.
        zero_byte_list (set): Set of filenames that have 0 byte size.

    Returns:
        list: List of IDs that do not have corresponding files in the bucket.
    """
    missing_ids = []

    try:
        with open(csv_path, mode="r", encoding="utf-8-sig") as csvfile:
            csvreader = csv.DictReader(csvfile)
            for row in csvreader:
                id_value = row.get("id")
                if not id_value:
                    continue

                file_name = f"{id_value}.{file_extension}"
                if not is_file_valid(file_name, file_list, zero_byte_list):
                    missing_ids.append(id_value)
    except Exception as e:
        print(f"Error reading CSV file: {e}")

    return missing_ids


def delete_missing_ids_from_database(missing_ids, table_name, column_name, supabase_client):
    """
    Deletes rows from the database where the specified column matches the IDs in missing_ids.

    :param missing_ids: List of IDs that need to be deleted from the database.
    :param table_name: Name of the database table.
    :param column_name: Column name to match the IDs against.
    :param supabase_client: Initialized Supabase client.
    """
    try:
        response = (
            supabase_client.table(table_name)
            .delete()
            .in_(column_name, missing_ids)
            .eq("source", "archive_of_our_own")  # Additional condition
            .execute()
        )
        print(f"Removed IDs from the database. Response: {response}")

    except Exception as e:
        print(f"An error occurred while removing data from the database: {e}")


if __name__ == "__main__":
    bucket = "fictionpress"
    bucket_dir = "contents"
    # Specify the path to your CSV file
    csv_file_path = "input.csv"

    file_extension = "txt"

    # Fetch the list of files in the bucket
    bucket_file_list, zero_byte_file_list = fetch_file_list_from_bucket(bucket, bucket_dir)

    if bucket_file_list is None:
        print("Could not fetch bucket file list. Exiting.")
        exit()

    # Identify missing files
    missing_file_ids = get_missing_files_from_csv(
        csv_file_path, bucket_file_list, zero_byte_file_list, file_extension
    )

    # Print IDs that do not have a corresponding file
    if missing_file_ids:
        print("IDs with no corresponding file in the bucket:")
        for id_ in missing_file_ids:
            print(id_)

        print("missing file count", len(missing_file_ids))
        # Prompt user for action
        print("Choose an option:")
        print("1. Retry uploading the missing files.")
        print("2. Remove the missing ID data from the database.")
        print("3. Do nothing.")
        choice = input("Enter your choice (1/2/3): ").strip()

        if choice == "1":
            retry_directory = input("Enter the directory path to retry uploading from: ").strip()

            if os.path.isdir(retry_directory):
                upload_missing_files(
                    missing_file_ids, retry_directory, bucket, bucket_dir, file_extension
                )
            else:
                print(f"Invalid directory path: {retry_directory}")
        elif choice == "2":
            table_name = input("Enter the table name: ").strip()
            column_name = input("Enter the column name: ").strip()
            delete_missing_ids_from_database(missing_file_ids, table_name, column_name, supabase)
        else:
            print("No retry selected. Exiting.")
    else:
        print("All IDs have corresponding files in the bucket.")
