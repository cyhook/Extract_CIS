import os
import csv
from git import Repo

# Clone the GitHub repository
repo_url = 'https://github.com/CISecurity/ControlsAssessmentSpecification.git'
repo_dir = 'ControlsAssessmentSpecification'

# Clone if the directory doesn't already exist
if not os.path.exists(repo_dir):
    Repo.clone_from(repo_url, repo_dir)

# CSV file to save extracted data
output_csv = 'extracted_data.csv'

# Create a list to hold the extracted data
data = []

# Loop through each control-* folder in the ControlsAssessmentSpecification directory
for root, dirs, files in os.walk(repo_dir):
    for file in files:
        if file.endswith('.rst'):
            original_file_path = os.path.join(root, file)
            temp_file_path = original_file_path.replace('.rst', '.txt')
            
            # Rename .rst file to .txt
            os.rename(original_file_path, temp_file_path)
            
            try:
                # Read the renamed .txt file
                with open(temp_file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()
                    
                    # Extract the first and third line if available
                    if len(lines) >= 3:
                        first_line = lines[0].strip()
                        third_line = lines[2].strip()
                        data.append([original_file_path, first_line, third_line])
            
            except Exception as e:
                print(f"Error reading file {temp_file_path}: {e}")
            
            finally:
                # Rename file back to .rst
                os.rename(temp_file_path, original_file_path)

# Write the extracted data to a CSV file
with open(output_csv, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['File Path', 'First Line', 'Third Line'])  # Header
    writer.writerows(data)

print(f"Data has been extracted to {output_csv}")
