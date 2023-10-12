---
layout: article
title: Download
---

## Data Format and Usage
The primary data format we used in data collection is [ROS bags](http://wiki.ros.org/rosbag). To simplify data storage and transfer, we split recorded data into blocks of 4GB, and categorized them based on their respective modalities.

You may download only those ROS bags that are of your interest. After download, simply place these ROS bags in the same folder and run `rosbag play *.bag`. ROS will automatically arrange the data across all bags and sequence the playback according to their timestamps.

To accomodate users from diverse application domains, we also provide a Python script that can extract data from rosbags and save them as indivisual files (images, pcd, csv files). See [tools](tools.html) for more information.

## Folder Structure
```
citrus-farm-dataset/
├── 01_13B_Jackal/
│   ├── adk_*.bag
│   ├── base_*.bag
│   ├── blackfly_*.bag
│   ├── mapir_*.bag
│   ├── odom_*.bag
│   └── zed_*.bag
├── 02_13B_Jackal/
├── 03_13B_Jackal/
├── 04_13D_Jackal/
├── 05_13D_Jackal/
├── 06_14B_Jackal/
├── 07_14B_Jackal/
└── Calibration/
    ├── README.docx
    ├── config/
    ├── data/
    ├── results/
    └── scripts/
```

For a complete file list, please see [dataset_file_list.yaml](https://raw.githubusercontent.com/UCR-Robotics/Citrus-Farm-Dataset/main/dataset_file_list.yaml).

## Download
We host our dataset on Amazon Web Services (AWS), sponsored by AWS [Open Data program](https://aws.amazon.com/opendata/open-data-sponsorship-program/).

You may use this Python script ([download_citrusfarm.py](https://raw.githubusercontent.com/UCR-Robotics/Citrus-Farm-Dataset/main/scripts/download_citrusfarm.py)) to download the dataset from AWS.
- By default, the script will download all sequences and all modalities.
- Change `folder_list` in the script to download only sequences of your interest.
- Change `modality_list` in the script to download only modalities of your interest.

If you are a user of AWS Command Line Interface, you can also download all data directly from the S3 bucket:
(You do not need to register any account to use this tool, but just `sudo apt install awscli`.)
```
aws s3 sync s3://ucr-robotics/citrus-farm-dataset/ /path/to/local/directory
```

Alternatively, you may download the dataset from two other backup sources:
- [Google Drive](https://drive.google.com/drive/folders/12h5CAagVVtz1Od9bK_O6hDMyG8Xh_DLG?usp=sharing)
- Baidu Pan (TODO)

## ROSbag Info
TBD.
