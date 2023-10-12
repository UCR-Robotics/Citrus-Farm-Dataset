import wget
import os
import yaml
import requests

def DownloadFiles(base_url, folder_dict, folder_list, modality_list):
  exempt_folders = ['Calibration', 'Calibration/config', 'Calibration/data', 
                    'Calibration/results', 'Calibration/scripts']

  for folder in folder_list:
    filenames = folder_dict.get(folder, [])
    # Create folder locally if not exists
    if not os.path.exists(folder):
      os.makedirs(folder)

    for filename in filenames:
      # Apply modality filter, with exemptions for certain folders
      if folder not in exempt_folders and not any(filename.startswith(modality) for modality in modality_list):
        continue

      # Generate the download URL
      download_url = f"{base_url}/{folder}/{filename}"

      # Download the file into the specified folder
      print(f"Downloading {filename} from {folder}")
      wget.download(download_url, f"{folder}/{filename}")

if __name__ == "__main__":
  # Base URL for the S3 bucket and YAML config
  base_url = "https://ucr-robotics.s3.us-west-2.amazonaws.com/citrus-farm-dataset"
  yaml_url = "https://raw.githubusercontent.com/UCR-Robotics/Citrus-Farm-Dataset/main/dataset_file_list.yaml"

  # Download and parse YAML config file
  response = requests.get(yaml_url)
  config_data = yaml.safe_load(response.text)

  folder_dict = config_data.get("folders", {})

  # List of folders you want to download
  folder_list = ["01_13B_Jackal", "02_13B_Jackal", "03_13B_Jackal",
                 "04_13D_Jackal", "05_13D_Jackal", "06_14B_Jackal", 
                 "07_14B_Jackal", "Calibration", "Calibration/config",
                 "Calibration/data", "Calibration/results", "Calibration/scripts"]

  # List of modalities you want to download
  modality_list = ["adk",      # thermal
                   "base",     # LiDAR, IMU, GPS-RTK raw data
                   "blackfly", # Monochrome
                   "mapir",    # NIR
                   "odom",     # wheel odom, GPS-RTK odom (post-processed from raw data)
                   "zed"       # RGB, depth
                   ]

  DownloadFiles(base_url, folder_dict, folder_list, modality_list)
