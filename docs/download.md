---
layout: article
title: Download
---

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
├── Calibration/
│   ├── README.pdf
│   ├── config/
│   ├── data/
│   ├── results/
│   └── scripts/
└── ground_truth/
    ├── 01_13B_Jackal/
    │   ├── gt.bag
    │   └── gt.csv
    ├── 02_13B_Jackal/
    ├── 03_13B_Jackal/
    ├── 04_13D_Jackal/
    ├── 05_13D_Jackal/
    ├── 06_14B_Jackal/
    └── 07_14B_Jackal/
```

For a complete file list, please see [dataset_file_list.yaml](https://raw.githubusercontent.com/UCR-Robotics/Citrus-Farm-Dataset/main/dataset_file_list.yaml).

## Download
We host [our dataset](https://registry.opendata.aws/citrus-farm/) on Amazon Web Services (AWS), sponsored by AWS [Open Data program](https://aws.amazon.com/opendata/open-data-sponsorship-program/).

You may use this Python script ([download_citrusfarm.py](https://raw.githubusercontent.com/UCR-Robotics/Citrus-Farm-Dataset/main/scripts/download_citrusfarm.py)) to download the dataset from AWS.
- By default, the script will download all sequences and all modalities.
- Change `folder_list` in the script to download only sequences of your interest.
- Change `modality_list` in the script to download only modalities of your interest.

If you are a user of AWS, you can also download all data directly from the S3 bucket using AWS CLI tool:
```
aws s3 sync s3://ucr-robotics/citrus-farm-dataset/ /path/to/local/directory
```

Alternatively, you may download the dataset from two other backup sources:
- [Google Drive](https://drive.google.com/drive/folders/12h5CAagVVtz1Od9bK_O6hDMyG8Xh_DLG?usp=sharing)
- [Baidu Pan](https://pan.baidu.com/s/1NVRTHKvFUue2qaQsb7wlVQ?pwd=ilas) (Credits to Yicheng Jin & Qi Wu@SJTU; please contact robotics_qi@sjtu.edu.cn for any download issue.)

## Data Format and Usage
The primary data format we used in data collection is [ROS bags](http://wiki.ros.org/rosbag).
To simplify data storage and transfer, we split recorded data into blocks of 4GB, and categorized them based on their respective modalities.
You may download only those ROS bags that are of your interest. 

After download, simply place these ROS bags in the same folder and play rosbags of your interest at once.
**ROS will automatically read the data across all bags and play them in sequence according to their timestamps.**
There is no need to merge multiple rosbags before playing.
```
# playback only lidar, IMU and thermal data
rosbag play base_*.bag adk_*.bag

# playback all data
rosbag play *.bag
```

To accommodate users from diverse application domains, we also provide a Python script that can extract data from rosbags and save them as individual files (images, pcd, csv files). See [tools](tools.html) for more information.

## ROSbag Info

| ROS Bag        | ROS Topic                                 | Msg Type                                | Sensor         |
|----------------|-------------------------------------------|-----------------------------------------|----------------|
| adk_*.bag      | /flir/adk/image_thermal                   | sensor_msgs/Image                       | Thermal Camera |
|                | /flir/adk/time_reference                  | sensor_msgs/TimeReference               | Thermal Camera |  
| base_*.bag     | /microstrain/imu/data                     | sensor_msgs/Imu                         | IMU            |
|                | /microstrain/mag                          | sensor_msgs/MagneticField               | IMU            |
|                | /piksi/navsatfix_best_fix                 | sensor_msgs/NavSatFix                   | GPS-RTK        |
|                | /piksi/debug/receiver_state               | piksi_rtk_msgs/<br>ReceiverState_V2_4_1 | GPS-RTK        |
|                | /velodyne_points                          | sensor_msgs/PointCloud2                 | LiDAR          |
| blackfly_*.bag | /flir/blackfly/cam0/image_raw             | sensor_msgs/Image                       | Mono Camera    |
|                | /flir/blackfly/cam0/time_reference        | sensor_msgs/TimeReference               | Mono Camera    |
| mapir_*.bag    | /mapir_cam/image_raw                      | sensor_msgs/Image                       | R-G-NIR Camera |
|                | /mapir_cam/time_reference                 | sensor_msgs/TimeReference               | R-G-NIR Camera |
| odom_*.bag     | /jackal_velocity_controller/odom          | nav_msgs/Odometry                       | Wheel Odometry |
| zed_*.bag      | /zed2i/zed_node/confidence/confidence_map | sensor_msgs/Image                       | Zed camera     |
|                | /zed2i/zed_node/depth/camera_info         | sensor_msgs/CameraInfo                  | Zed camera     |
|                | /zed2i/zed_node/depth/depth_registered    | sensor_msgs/Image                       | Zed camera     |
|                | /zed2i/zed_node/imu/data                  | sensor_msgs/Imu                         | Zed camera     |
|                | /zed2i/zed_node/imu/mag                   | sensor_msgs/MagneticField               | Zed camera     |
|                | /zed2i/zed_node/left/camera_info          | sensor_msgs/CameraInfo                  | Zed camera     |
|                | /zed2i/zed_node/left/image_rect_color     | sensor_msgs/Image                       | Zed camera     |
|                | /zed2i/zed_node/pose                      | geometry_msgs/PoseStamped               | Zed camera     |
|                | /zed2i/zed_node/right/camera_info         | sensor_msgs/CameraInfo                  | Zed camera     |
|                | /zed2i/zed_node/right/image_rect_color    | sensor_msgs/Image                       | Zed camera     |
| gt.bag         | /gps/fix/odometry                         | nav_msgs/Odometry                       | GPS-RTK        |

Notes about the three GPS-RTK data types:
- `/piksi/navsatfix_best_fix` is the raw RTK data recorded in the fixed mode;
- `/piksi/debug/receiver_state` is the debugging data to show info such as number of satellites;
- `/gps/fix/odometry` is the post-processed data (via WGS84) that can serve as the **ground-truth trajectories**. (In the meantime, we also provide equivalent CSV files of ground-truth trajectories, in case they are preferred by users.)
- Lastly, we ensured that the GPS-RTK system was always operating in the fixed mode (more accurate than the floating mode) in all experiments, thanks to the high-gain antennas.

Notes about time synchronization:
- `/*/time_reference` recorded the hardware clock time of cameras if available, in case they are useful at some point. In general, you can ignore this topic unless you know what you are doing. 
- In experiments, we have observed that using hardware clock time of each camera can result in larger drift, since these cameras are of different kinds/types (with distinct crystal oscillators, some are running faster while others slower).
- Ideally, for the best performance, we shall have hardware synchronization on professional cameras that provide an interface to connect to an external reference clock. In our case, using software time (ROS time) is also fine.

Please see [Calibration](calibration.html) for more information regarding sensor setup, camera specifications, intrinsic and extrinsic parameters.
