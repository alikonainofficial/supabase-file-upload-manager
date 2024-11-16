Supabase File Check and Upload Script

This script is designed to identify and upload missing files from a local directory to a specified Supabase storage bucket. It cross-references a list of files provided in a CSV file with the files currently present in the storage bucket and offers a retry mechanism for uploading missing files.

Features

	•	Dynamic File Comparison: Fetches and compares files from Supabase storage against the file IDs listed in a CSV file.
	•	Retry Mechanism: Prompts users to retry uploading missing files from a specified local directory.
	•	Customizable Paths: Allows users to define the local directory for missing files during retries.
	•	Error Handling and Logging: Provides detailed feedback and handles errors gracefully.

Requirements

	•	Python 3.7+
	•	Dependencies listed in requirements.txt

Setup

	1.	Install Required Libraries:

pip install -r requirements.txt


	2.	Set Up Environment Variables:
Create a .env file in the project directory and add the following:

SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_api_key


	3.	Prepare Input Files:
	•	A CSV file with an id column that contains file identifiers.
	•	The files in the local directory should be named <id>.txt.

Usage

	1.	Run the Script:
Execute the script using the command:

python script_name.py


	2.	Follow the Prompts:
	•	If missing files are identified, you’ll be prompted to retry uploading them.
	•	Provide the path to the local directory containing the missing files when prompted.
	3.	View Output:
The script will display a list of missing files and log the success or failure of each upload attempt.

Functions Overview

	•	fetch_file_list_from_bucket(bucket, bucket_dir): Retrieves the list of files in the specified bucket directory.
	•	get_missing_files_from_csv(csv_path, file_list): Compares the IDs in the CSV with the fetched file list to identify missing files.
	•	upload_missing_files(missing_files, directory_path, bucket, bucket_dir): Uploads missing files to the specified bucket directory.
	•	check_file_in_bucket(file_name, file_list): Checks if a specific file exists in the fetched file list.

Example

	1.	A CSV file (supernatural_fanfiction_db.csv) contains:

id
123
456
789


	2.	The bucket directory (supernatural) in the bucket (fanfiction) contains:
	•	123.txt
	•	456.txt
	3.	Missing files:
	•	789.txt
	4.	The script identifies 789 as missing and allows you to upload it from your local directory.

Notes

	•	Ensure the CSV file and local directory have correct and matching file names.
	•	Files are expected to have a .txt extension.
	•	Adjust the bucket and directory paths in the script as needed.

License

This project is licensed under the MIT License. See LICENSE for details.