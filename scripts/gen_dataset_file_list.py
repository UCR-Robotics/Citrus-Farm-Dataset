import os
import hashlib
import yaml
from tqdm import tqdm

def ComputeMD5(file_path):
  hash_md5 = hashlib.md5()
  with open(file_path, "rb") as f:
    for chunk in iter(lambda: f.read(4096), b""):
      hash_md5.update(chunk)
  return hash_md5.hexdigest()

def GenerateYAMLConfig(root_dir):
  config_dict = {'citrus-farm-dataset': {}}

  # Count total number of files for the progress bar
  total_files = 0
  for _, _, filenames in os.walk(root_dir):
    total_files += len(filenames)

  pbar = tqdm(total=total_files, desc="Processing files", dynamic_ncols=True)

  # Traverse the directory tree rooted at root_dir
  for dirpath, dirnames, filenames in os.walk(root_dir):
    # Skip the root directory itself
    if dirpath == root_dir:
      continue

    # Extract the relative directory name
    rel_dir = os.path.relpath(dirpath, root_dir)

    # Sort filenames alphanumerically and compute MD5 checksums
    file_info = {}
    for file_name in sorted(filenames):
      full_file_path = os.path.join(dirpath, file_name)
      file_info[file_name] = {"md5": ComputeMD5(full_file_path)}
      pbar.update(1)  # Update the progress bar

    # Update the dictionary
    config_dict['citrus-farm-dataset'][rel_dir] = file_info

  pbar.close()

  # Serialize to YAML
  with open("dataset_file_list.yaml", "w") as yaml_file:
    yaml.dump(config_dict, yaml_file)

if __name__ == "__main__":
  root_dir = "."  # Replace with the path to your local root directory
  GenerateYAMLConfig(root_dir)
