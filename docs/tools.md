---
layout: article
title: Tools
---

## Python Scripts
Dataset-related scripts:
- [gen_dataset_file_list.py](https://raw.githubusercontent.com/UCR-Robotics/Citrus-Farm-Dataset/main/scripts/gen_dataset_file_list.py) Script to generate file list for this dataset
- [download_citrusfarm.py](https://raw.githubusercontent.com/UCR-Robotics/Citrus-Farm-Dataset/main/scripts/download_citrusfarm.py) Script to help download this dataset
- [bag2files.py](https://raw.githubusercontent.com/UCR-Robotics/Citrus-Farm-Dataset/main/scripts/bag2files.py) Convert downloaded rosbags into individual files (images, pcd and csv files)
- [imu_filter.py](https://raw.githubusercontent.com/UCR-Robotics/Citrus-Farm-Dataset/main/scripts/imu_filter.py) Script to filter IMU timestamps (to avoid duplicated timestamps) using a Kalman filter

For sensor calibration:
- [kalibr_create_target_pdf.py](https://ucr-robotics.s3.us-west-2.amazonaws.com/citrus-farm-dataset/Calibration/scripts/kalibr_create_target_pdf.py) This script is modified from Kalibr toolbox, and it can generate the 24-inch checkerboard and april-grid calibration targets used in this dataset
- [interactive_recording.py](https://ucr-robotics.s3.us-west-2.amazonaws.com/citrus-farm-dataset/Calibration/scripts/interactive_recording.py) Record image frames of all cameras when the user presses the Enter key, and save them into a rosbag in the end.
- [publish_camera_info.py](https://ucr-robotics.s3.us-west-2.amazonaws.com/citrus-farm-dataset/Calibration/scripts/publish_camera_info.py) Publish the `camera_info` topic of a camera, provided a yaml file specifying camera intrinsics. (Example: [flir_blackfly_cam_info.yaml](https://ucr-robotics.s3.us-west-2.amazonaws.com/citrus-farm-dataset/Calibration/scripts/flir_blackfly_cam_info.yaml))

Evaluation scripts for odometry algorithms:
- [Odometry-Benchmark](https://github.com/UCR-Robotics/Odometry-Benchmark) We have made our benchmark code available in this repository. It includes scripts for running algorithms on datasets in batch mode, as well as scripts for post-processing the recorded results and calculating error metrics.
