# Smart File Manager & Storage Optimizer

A robust Python automation tool designed to declutter local directories, categorize files based on extensions, and optimize storage by detecting and eliminating cryptographic duplicates.

## Key Features
* **Cryptographic Duplicate Detection:** Uses MD5 hashing to uniquely identify file contents and permanently remove exact duplicates to save space.
* **Smart Categorization:** Automatically scans and sorts files into dedicated folders such as Documents, Images, Code Files, Media, and Archives.
* **Execution Log Generation:** Generates a real-time `execution_report.txt` after every cleanup session, detailing the action summary and timestamps.
* **Safe Folder Handling:** Purposefully skips directories to ensure only loose files within the target folder are processed safely.

## Technical Stack
* **Language:** Python 3.x
* **Core Modules:** `os`, `shutil`, `hashlib`, `datetime`

## How It Works
1. Run the script and input the absolute path of the directory you want to organize.
2. The script hashes each file to check for duplicates.
3. Loose files are sorted instantly into their respective category folders.
4. A full execution report is generated in the root directory.
