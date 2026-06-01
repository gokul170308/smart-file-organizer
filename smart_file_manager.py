import os
import shutil
import hashlib
from datetime import datetime

def calculate_file_hash(file_path):
   """Calculates the MD5 hash of a file to uniquely identify its content."""
   hasher = hashlib.md5()
   try:
       with open(file_path, 'rb') as f:
           # Read the file in small chunks to handle large files smoothly
           buf = f.read(65536)
           while len(buf) > 0:
               hasher.update(buf)
               buf = f.read(65536)
       return hasher.hexdigest()
   except Exception:
       return None

def organize_and_cleanup(target_directory):
   if not os.path.exists(target_directory):
       print(f"Error: The directory '{target_directory}' does not exist.")
       return

   file_categories = {
       'Documents': ['.pdf', '.docx', '.txt', '.xlsx', '.pptx'],
       'Images': ['.jpg', '.jpeg', '.png', '.gif', '.svg'],
       'Code_Files': ['.py', '.cpp', '.c', '.html', '.css', '.js', '.json'],
       'Media': ['.mp3', '.mp4', '.mkv', '.wav'],
       'Archives': ['.zip', '.rar', '.tar', '.gz']
   }

   print(f"Scanning directory: {target_directory}\n" + "-"*40)
   
   seen_file_hashes = set()
   moved_counts = {category: 0 for category in file_categories}
   moved_counts['Others'] = 0
   deleted_duplicates_count = 0

   # Read all items in the folder
   for item in os.listdir(target_directory):
       item_path = os.path.join(target_directory, item)
       
       # Skip folders (we only want to process files)
       if os.path.isdir(item_path):
           continue

       # --- STEP 1: DUPLICATE DETECTION ---
       file_hash = calculate_file_hash(item_path)
       if file_hash:
           if file_hash in seen_file_hashes:
               print(f"Duplicate found! Deleting: {item}")
               os.remove(item_path)  # Permanently deletes the duplicate file
               deleted_duplicates_count += 1
               continue  # Skip to the next file since this one is deleted
           else:
               seen_file_hashes.add(file_hash)

       # --- STEP 2: CATEGORY SORTING ---
       filename, file_extension = os.path.splitext(item)
       file_extension = file_extension.lower()

       moved = False
       for category, extensions in file_categories.items():
           if file_extension in extensions:
               category_folder = os.path.join(target_directory, category)
               os.makedirs(category_folder, exist_ok=True)
               
               shutil.move(item_path, os.path.join(category_folder, item))
               moved_counts[category] += 1
               moved = True
               break
       
       if not moved and file_extension != '':
           others_folder = os.path.join(target_directory, 'Others')
           os.makedirs(others_folder, exist_ok=True)
           shutil.move(item_path, os.path.join(others_folder, item))
           moved_counts['Others'] += 1

   # --- STEP 3: LOG GENERATION ---
   log_path = os.path.join(target_directory, "execution_report.txt")
   with open(log_path, "w") as log_file:
       log_file.write(f"Smart Storage Cleanup Report\n")
       log_file.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
       log_file.write("-" * 40 + "\n")
       for cat, count in moved_counts.items():
           if count > 0:
               log_file.write(f"{cat}: {count} files organized.\n")
               print(f"Successfully moved {count} file(s) to '{cat}'")
       
       log_file.write(f"Duplicates Deleted: {deleted_duplicates_count} files removed.\n")
       print(f"Total duplicate files cleaned up: {deleted_duplicates_count}")

   print("-"*40 + f"\nSuccess! Summary report generated: {log_path}")

if __name__ == "__main__":
   folder_to_clean = input("Enter the absolute path of the folder to clean: ").strip()
   organize_and_cleanup(folder_to_clean)