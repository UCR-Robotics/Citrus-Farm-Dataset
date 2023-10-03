---
# Feel free to add content and custom Front Matter to this file.
# To modify the layout, see https://jekyllrb.com/docs/themes/#overriding-theme-defaults

layouts: default
title: CitrusFarm Dataset
---

## Introduction
CitrusFarm is a multimodal agricultural robotics dataset that provides both **multispectral images** and **navigational sensor data** for localization, mapping and crop monitoring tasks.
- It was collected by a wheeled mobile robot in the [Agricultural Experimental Station](https://cnas.ucr.edu/resources/agricultural-experiment-station) at the [University of California Riverside](https://www.ucr.edu/) in the summer of 2023.
- It offers a total of **nine** sensing modalities, including stereo RGB, depth, monochrome, near-infrared and thermal images, as well as wheel odometry, LiDAR, IMU and GPS-RTK data.
- It comprises seven sequences collected from three citrus tree fields, featuring various tree species at different growth stages, distinctive planting patterns, as well as varying daylight conditions.
- It spans a total operation time of 1.7 hours, covers a total distance of 7.5 km, and constitutes 1.3 TB of data.

**Authors:** Hanzhe Teng, Yipeng Wang, Xiaoao Song and Konstantinos Karydis from [ARCS Lab](https://sites.google.com/view/arcs-lab/) at [UC Riverside](https://www.ucr.edu/).

**Videos:** Will be posted once available.

**Related Publications:**
H. Teng, Y. Wang, X. Song and K. Karydis, "Multimodal Dataset for Localization, Mapping and Crop Monitoring in Citrus Tree Farms", in the 18th International Symposium on Visual Computing (ISVC 2023). ([preprint](https://arxiv.org/abs/2309.15332))

## License
CitrusFarm dataset is released under the [Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0). You are allowed to **share** and **adapt** under the condition that you **give appropriate credit**, **indicate if changes were made**, and distribute your contributions under the **same license**.

## Acknowledgement
This work is supported in part by NSF, USDA-NIFA, ONR and the University of California UC-MRPI.
Furthermore, we thank Dr. Peggy Mauk and the staff team at UCR’s Agricultural Experimental Station for their support in our work.

## Mobile Robot Platform
We employ the Clearpath Jackal wheeled mobile robot to collect multi-sensor data in the agricultural fields.
The sensor setup on the robot is illustrated in the figure below (left).
The corresponding reference frames are highlighted in the figure below (right).
Red, green and blue bars denote x, y and z axes respectively. They are generated in RViz using real calibrated extrinsic parameters.

![Robot Sensor Setup](./figures/robot.png)

## Sample Data
### Sample Multispectral Images
![Sample Multispectral Images](./figures/image.png)

### Sample Trajectories
![Sample Trajectories](./figures/trajectory.png)

### Sample Field Views
![Sample Field Views](./figures/field.png)

## Sequence Info
![Sequence Info](./figures/sequence.png)

## Data Format and Download
The primary data format we used in data collection is [ROS bags](http://wiki.ros.org/rosbag). To simplify data storage and transfer, we split recorded data into blocks of 4GB, and categorized them based on their respective modalities.

You may download only those ROS bags that are of your interest. After download, simply place these ROS bags in the same folder and run `rosbag play *.bag`. ROS will automatically arrange the data across all bags and sequence the playback according to their timestamps.

Click [this link](https://drive.google.com/drive/folders/12h5CAagVVtz1Od9bK_O6hDMyG8Xh_DLG?usp=sharing) to download all sequences of data.

