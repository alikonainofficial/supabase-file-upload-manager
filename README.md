# Supabase File Management Scripts

This repository contains scripts designed for managing files in a Supabase storage bucket. It includes functionality for checking and uploading missing files as well as deleting all files within a specific folder.

## Purpose

### 1. Supabase File Check and Upload Script

This script is designed to identify and upload missing files from a local directory to a specified Supabase storage bucket. It cross-references a list of files provided in a CSV file with the files currently present in the storage bucket and offers a retry mechanism for uploading missing files.

### 2. Supabase Folder Deletion Script

This script allows for the deletion of all files within a specified folder in a Supabase storage bucket. It is particularly useful for cleaning up storage or removing outdated files in bulk.

## Features

### File Check and Upload Script

- **Dynamic File Comparison**: Fetches and compares files from Supabase storage against the file IDs listed in a CSV file.
- **Retry Mechanism**: Prompts users to retry uploading missing files from a specified local directory.
- **Customizable Paths**: Allows users to define the local directory for missing files during retries.
- **Error Handling and Logging**: Provides detailed feedback and handles errors gracefully.

### Folder Deletion Script

- **Bulk Deletion**: Deletes all files in a specified folder within a Supabase storage bucket.
- **Folder Validation**: Checks if the folder exists and contains files before deletion.
- **Error Handling**: Handles potential errors during the deletion process and provides detailed feedback.

## Requirements

- Python 3.7+
- Dependencies listed in `requirements.txt`

## Setup

1. Install Required Libraries:

   ```bash
   pip install -r requirements.txt
   ```

2. Set Up Environment Variables:

   Create a `.env` file in the project directory and add the following:

   ```bash
   SUPABASE_URL=your_supabase_project_url
   SUPABASE_KEY=your_supabase_api_key
   ```

3. Prepare Input Files:

   - For the file check and upload script:
     - A CSV file with an id column that contains file identifiers.
     - The files in the local directory should be named `file_id.txt`.

## Usage

### File Check and Upload Script

1. Run the Script:

   Execute the script using the command:

   ```bash
   python missing_file_uploader.py
   ```

2. Follow the Prompts:

   - If missing files are identified, you’ll be prompted to retry uploading them.
   - Provide the path to the local directory containing the missing files when prompted.

3. View Output:
   - The script will display a list of missing files and log the success or failure of each upload attempt.

### Folder Deletion Script

1. Update the script with the desired bucket name and folder name.
2. Run the script:

   ```bash
   python bucket_folder_deleter.py
   ```

3. View Output:
   - The script will confirm the deletion of all files in the specified folder or report any errors encountered.

## Functions Overview

### File Check and Upload Script

- `fetch_file_list_from_bucket(bucket, bucket_dir)`: Retrieves the list of files in the specified bucket directory.
- `get_missing_files_from_csv(csv_path, file_list)`: Compares the IDs in the CSV with the fetched file list to identify missing files.
- `upload_missing_files(missing_files, directory_path, bucket, bucket_dir)`: Uploads missing files to the specified bucket directory.
- `check_file_in_bucket(file_name, file_list)`: Checks if a specific file exists in the fetched file list.

### Folder Deletion Script

- `delete_folder(bucket_name, folder_name)`: Deletes all files in the specified folder within a Supabase storage bucket.

## Example Scenarios

### File Check and Upload Script

1.  A CSV file (`supernatural_fanfiction_db.csv`) contains:

        id
        123
        456
        789

2.  The bucket directory (`supernatural`) in the bucket (`fanfiction`) contains:

        123.txt
        456.txt

3.  Missing files:

        789.txt

4.  The script identifies `789.txt` as missing and allows you to upload it from your local directory.

### Folder Deletion Script

1.  A folder (`old_data`) in a bucket (`project_assets`) contains:

        report1.pdf
        report2.pdf

2.  Running the script with `bucket_name="project_assets"` and `folder_name="old_data"` deletes all files in the folder.

## Notes

- Ensure input files and directories are correctly formatted and accessible.
- For the file check script, files are expected to have a `.txt` extension.
- Adjust bucket and directory paths in the scripts as needed.

## License

This project is licensed under the MIT License. See LICENSE for details.
