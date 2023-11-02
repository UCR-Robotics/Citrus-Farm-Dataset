# File: download_citrusfarm.py
# Authors: Hanzhe Teng et al.
# Date: 2023-10-11
# Description: This script is part of the CitrusFarm Dataset (https://ucr-robotics.github.io/Citrus-Farm-Dataset/),
#   which is released under the Attribution-ShareAlike 4.0 International (CC BY-SA 4.0) license.

"""
This script downloads the CitrusFarm Dataset from the AWS S3 bucket and verifies the MD5 checksums.
"""

import wget
import os
import yaml
import requests
import hashlib

def ComputeMD5(file_path):
  hash_md5 = hashlib.md5()
  with open(file_path, "rb") as f:
    for chunk in iter(lambda: f.read(4096), b""):
      hash_md5.update(chunk)
  return hash_md5.hexdigest()

def DownloadFiles(base_url, folder_dict, folder_list, modality_list):
  data_folders = ["01_13B_Jackal", "02_13B_Jackal", "03_13B_Jackal", "04_13D_Jackal",
                  "05_13D_Jackal", "06_14B_Jackal", "07_14B_Jackal"]
  files_to_verify = []

  # Download Phase
  for folder in folder_list:
    filenames = folder_dict.get(folder, {})
    
    # Create folder locally if not exists
    if not os.path.exists(folder):
      os.makedirs(folder)

    for filename in filenames.keys():
      # Apply modality filter on data folders
      if folder in data_folders and not any(filename.startswith(modality) for modality in modality_list):
        continue

      local_file_path = f"{folder}/{filename}"

      # Skip download if file already exists
      if os.path.exists(local_file_path):
        print(f"File {local_file_path} already exists, skipping download.")
        files_to_verify.append((folder, filename))
        continue

      # Generate the download URL
      download_url = f"{base_url}/{folder}/{filename}"
      
      # Download the file into the specified folder
      print(f"Downloading {local_file_path}")
      wget.download(download_url, local_file_path)
      print()

      # Add to list of files to verify
      files_to_verify.append((folder, filename))

  # MD5 Verification Phase
  print(f"Verifying MD5 for downloaded files.")
  for folder, filename in files_to_verify:
    local_file_path = f"{folder}/{filename}"
    expected_md5 = folder_dict[folder][filename]['md5']
    computed_md5 = ComputeMD5(local_file_path)

    while expected_md5 != computed_md5:
      print(f"MD5 mismatch for {local_file_path}. Removing current file and Redownloading.")
      os.remove(local_file_path)
      download_url = f"{base_url}/{folder}/{filename}"
      wget.download(download_url, local_file_path)
      print()
      print(f"Redownloaded {local_file_path}. Verifying again.")
      computed_md5 = ComputeMD5(local_file_path)

    print(f"MD5 verified for {local_file_path}.")
  print(f"MD5 verified for all downloaded files.")

if __name__ == "__main__":
  # Base URL for the S3 bucket and YAML config
  base_url = "https://ucr-robotics.s3.us-west-2.amazonaws.com/citrus-farm-dataset"
  yaml_url = "https://raw.githubusercontent.com/UCR-Robotics/Citrus-Farm-Dataset/main/dataset_file_list.yaml"

  # Download and parse YAML config file
  response = requests.get(yaml_url)
  config_data = yaml.safe_load(response.text)

  folder_dict = config_data.get("citrus-farm-dataset", {})

  # List of folders you want to download
  folder_list = ["01_13B_Jackal", "02_13B_Jackal", "03_13B_Jackal", "04_13D_Jackal",
                 "05_13D_Jackal", "06_14B_Jackal", "07_14B_Jackal",
                 "Calibration", "Calibration/config", "Calibration/data",
                 "Calibration/results", "Calibration/scripts",
                 "ground_truth/01_13B_Jackal", "ground_truth/02_13B_Jackal",
                 "ground_truth/03_13B_Jackal", "ground_truth/04_13D_Jackal",
                 "ground_truth/05_13D_Jackal", "ground_truth/06_14B_Jackal",
                 "ground_truth/07_14B_Jackal"]

  # List of modalities you want to download
  modality_list = ["adk",      # thermal
                   "base",     # LiDAR, IMU, GPS-RTK raw data
                   "blackfly", # Monochrome
                   "mapir",    # NIR
                   "odom",     # wheel odom, GPS-RTK odom (post-processed from raw data)
                   "zed"       # RGB, depth
                   ]

  DownloadFiles(base_url, folder_dict, folder_list, modality_list)
