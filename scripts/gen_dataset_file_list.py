import os
import yaml

def GenerateYAMLConfig(root_dir):
  config_dict = {'folders': {}}

  # Traverse the directory tree rooted at root_dir
  for dirpath, dirnames, filenames in os.walk(root_dir):
    # Skip the root directory itself
    if dirpath == root_dir:
      continue
    
    # Extract the relative directory name
    rel_dir = os.path.relpath(dirpath, root_dir)

    # Sort filenames alphanumerically
    sorted_filenames = sorted(filenames)
    
    # Update the dictionary
    config_dict['folders'][rel_dir] = sorted_filenames

  # Serialize to YAML
  with open("dataset_file_list.yaml", "w") as yaml_file:
    yaml.dump(config_dict, yaml_file)

if __name__ == "__main__":
  root_dir = "."  # Replace with the path to your local root directory
  GenerateYAMLConfig(root_dir)

