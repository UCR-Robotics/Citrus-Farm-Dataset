# File: bag2files.py
# Authors: Hanzhe Teng et al.
# Date: 2023-10-31
# Description: This script is part of the CitrusFarm Dataset (https://ucr-robotics.github.io/Citrus-Farm-Dataset/),
#   which is released under the Attribution-ShareAlike 4.0 International (CC BY-SA 4.0) license.

"""
This script extracts data from rosbags and saves them to individual files.

Usage: python bag2files.py <src_folder> <output_folder> (e.g. python bag2files.py 01_13B_Jackal /path/to/output)
  <src_folder> is the folder containing rosbags to be processed
  <output_folder> is the folder to save the extracted data

You can also modify the following two variables to select those rosbags and topics that you want to process:
  rosbag_prefixes_of_interest
  known_topic_info
"""

import argparse
import csv
import os
import rosbag
import cv2
from cv_bridge import CvBridge
import sensor_msgs.point_cloud2 as pc2

known_topic_info = {
  # 'adk' bag topics
  '/flir/adk/image_thermal': 'sensor_msgs/Image',
  '/flir/adk/time_reference': 'sensor_msgs/TimeReference',

  # 'base' bag topics
  '/microstrain/imu/data': 'sensor_msgs/Imu',
  '/microstrain/mag': 'sensor_msgs/MagneticField',
  '/piksi/navsatfix_best_fix': 'sensor_msgs/NavSatFix',
  '/piksi/debug/receiver_state': 'piksi_rtk_msgs/ReceiverState_V2_4_1',
  '/velodyne_points': 'sensor_msgs/PointCloud2',

  # 'blackfly' bag topics
  '/flir/blackfly/cam0/image_raw': 'sensor_msgs/Image',
  '/flir/blackfly/cam0/time_reference': 'sensor_msgs/TimeReference',

  # 'mapir' bag topics
  '/mapir_cam/image_raw': 'sensor_msgs/Image',
  '/mapir_cam/time_reference': 'sensor_msgs/TimeReference',

  # 'odom' bag topics
  '/jackal_velocity_controller/odom': 'nav_msgs/Odometry',

  # 'zed' bag topics
  '/zed2i/zed_node/confidence/confidence_map': 'sensor_msgs/Image',
  '/zed2i/zed_node/depth/camera_info': 'sensor_msgs/CameraInfo',
  '/zed2i/zed_node/depth/depth_registered': 'sensor_msgs/Image',
  '/zed2i/zed_node/imu/data': 'sensor_msgs/Imu',
  '/zed2i/zed_node/imu/mag': 'sensor_msgs/MagneticField',
  '/zed2i/zed_node/left/camera_info': 'sensor_msgs/CameraInfo',
  '/zed2i/zed_node/left/image_rect_color': 'sensor_msgs/Image',
  '/zed2i/zed_node/pose': 'geometry_msgs/PoseStamped',
  '/zed2i/zed_node/right/camera_info': 'sensor_msgs/CameraInfo',
  '/zed2i/zed_node/right/image_rect_color': 'sensor_msgs/Image'
}


def file_writer_general_data(msg, output_filepath):
  """Write a general message to a file."""
  with open(f"{output_filepath}.txt", 'w') as data_file:
    data_file.write(str(msg))


def file_writer_image(msg, output_filepath):
  """Write a sensor_msgs/Image to a file."""
  cv_bridge = CvBridge()
  img = cv_bridge.imgmsg_to_cv2(msg, msg.encoding)
  cv2.imwrite(f"{output_filepath}.jpg", img)


def file_writer_point_cloud(msg, output_filepath):
  """Write a sensor_msgs/PointCloud2 to a file."""
  point_cloud = pc2.read_points(msg, field_names=("x", "y", "z", "intensity", "ring"), skip_nans=True)
  point_cloud_list = list(point_cloud)
  with open(f"{output_filepath}.pcd", 'w') as pcd_file:
    pcd_file.write("# .PCD v0.7 - Point Cloud Data file format\n")
    pcd_file.write("VERSION 0.7\n")
    pcd_file.write("FIELDS x y z intensity ring\n")
    pcd_file.write("SIZE 4 4 4 4 2\n")
    pcd_file.write("TYPE F F F F U\n")
    pcd_file.write("COUNT 1 1 1 1 1\n")
    pcd_file.write("WIDTH {}\n".format(len(point_cloud_list)))
    pcd_file.write("HEIGHT 1\n")
    pcd_file.write("VIEWPOINT 0 0 0 1 0 0 0\n")
    pcd_file.write("POINTS {}\n".format(len(point_cloud_list)))
    pcd_file.write("DATA ascii\n")
    for p in point_cloud_list:
      pcd_file.write(f"{float(p[0])} {float(p[1])} {float(p[2])} {int(p[3])} {p[4]}\n")


def csv_row_writer_imu(msg, csv_writer):
  """Convert sensor_msgs/Imu to a row for CSV."""
  csv_writer.writerow([
    msg.header.stamp.to_sec(),
    msg.orientation.x,
    msg.orientation.y,
    msg.orientation.z,
    msg.orientation.w,
    msg.angular_velocity.x,
    msg.angular_velocity.y,
    msg.angular_velocity.z,
    msg.linear_acceleration.x,
    msg.linear_acceleration.y,
    msg.linear_acceleration.z
  ])


def csv_row_writer_magnetic_field(msg, csv_writer):
  """Convert sensor_msgs/MagneticField to a row for CSV."""
  csv_writer.writerow([
    msg.header.stamp.to_sec(),
    msg.magnetic_field.x,
    msg.magnetic_field.y,
    msg.magnetic_field.z
  ])


def csv_row_writer_pose_stamped(msg, csv_writer):
  """Convert geometry_msgs/PoseStamped to a row for CSV."""
  csv_writer.writerow([
    msg.header.stamp.to_sec(),
    msg.pose.position.x,
    msg.pose.position.y,
    msg.pose.position.z,
    msg.pose.orientation.x,
    msg.pose.orientation.y,
    msg.pose.orientation.z,
    msg.pose.orientation.w
  ])


def csv_row_writer_odometry(msg, csv_writer):
  """Convert nav_msgs/Odometry to a row for CSV."""
  csv_writer.writerow([
    msg.header.stamp.to_sec(),
    msg.pose.pose.position.x,
    msg.pose.pose.position.y,
    msg.pose.pose.position.z,
    msg.pose.pose.orientation.x,
    msg.pose.pose.orientation.y,
    msg.pose.pose.orientation.z,
    msg.pose.pose.orientation.w,
    msg.twist.twist.linear.x,
    msg.twist.twist.linear.y,
    msg.twist.twist.linear.z,
    msg.twist.twist.angular.x,
    msg.twist.twist.angular.y,
    msg.twist.twist.angular.z
  ])


def csv_row_writer_time_reference(msg, csv_writer):
  """Convert sensor_msgs/TimeReference to a row for CSV."""
  csv_writer.writerow([
    msg.header.stamp.to_sec(),
    msg.time_ref.to_sec()
  ])


def save_data_to_file_timestamp(bag, topic, output_topic_folder, file_writer):
  """Save all messages of a rosbag topic to files, with the timestamp as the filename."""
  filename_prefix = os.path.basename(bag.filename).replace('.', '_')
  for _, msg, t in bag.read_messages(topics=[topic]):
    timestamp = t.to_nsec()  # nanoseconds
    output_filename = f"{filename_prefix}_{timestamp}"
    file_writer(msg, os.path.join(output_topic_folder, output_filename))


def save_data_to_file_counter(bag, topic, output_topic_folder, file_writer):
  """Save all messages of a rosbag topic to files, with a counter as the filename."""
  filename_prefix = os.path.basename(bag.filename).replace('.', '_')
  count = 0
  for _, msg, _ in bag.read_messages(topics=[topic]):
    output_filename = f"{filename_prefix}_{count}"
    file_writer(msg, os.path.join(output_topic_folder, output_filename))
    count += 1


def save_data_to_file_first_msg(bag, topic, output_topic_folder, file_writer):
  """Save only the first message of a rosbag topic to a file."""
  output_filename = os.path.basename(bag.filename).replace('.', '_')
  _, msg, _ = next(bag.read_messages(topics=[topic]))
  output_filepath = os.path.join(output_topic_folder, f"{output_filename}")
  file_writer(msg, output_filepath)


def save_data_to_csv(bag, topic, output_topic_folder, csv_header, row_writer):
  """Save all messages of a rosbag topic to a csv file, with each message contributing to a row."""
  output_filename = f"{os.path.basename(bag.filename).replace('.', '_')}_{topic.replace('/', '_').strip('_')}.csv"
  with open(os.path.join(output_topic_folder, output_filename), 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(csv_header)
    for _, msg, _ in bag.read_messages(topics=[topic]):
      row_writer(msg, csv_writer)


def process_data_by_msg_type(bag, topic, msg_type, output_folder):
  """Save data from a rosbag topic to output_folder, according to the message type."""
  output_topic_folder = os.path.join(output_folder, topic.replace('/', '_').strip('_'))
  os.makedirs(output_topic_folder, exist_ok=True)

  # Category 1: save all messages into a csv file, each contributing to a row
  if msg_type == "sensor_msgs/Imu":
    csv_header = ["timestamp", "orientation_x", "orientation_y", "orientation_z", "orientation_w",
                  "angular_velocity_x", "angular_velocity_y", "angular_velocity_z",
                  "linear_acceleration_x", "linear_acceleration_y", "linear_acceleration_z"]
    save_data_to_csv(bag, topic, output_topic_folder, csv_header, csv_row_writer_imu)

  elif msg_type == "sensor_msgs/MagneticField":
    csv_header = ["timestamp", "magnetic_field_x", "magnetic_field_y", "magnetic_field_z"]
    save_data_to_csv(bag, topic, output_topic_folder, csv_header, csv_row_writer_magnetic_field)

  elif msg_type == "geometry_msgs/PoseStamped":
    csv_header = ["timestamp", "x", "y", "z", "qx", "qy", "qz", "qw"]
    save_data_to_csv(bag, topic, output_topic_folder, csv_header, csv_row_writer_pose_stamped)

  elif msg_type == "nav_msgs/Odometry":
    csv_header = ["timestamp", "position_x", "position_y", "position_z",
                  "orientation_x", "orientation_y", "orientation_z", "orientation_w",
                  "linear_velocity_x", "linear_velocity_y", "linear_velocity_z",
                  "angular_velocity_x", "angular_velocity_y", "angular_velocity_z"]
    save_data_to_csv(bag, topic, output_topic_folder, csv_header, csv_row_writer_odometry)

  elif msg_type == "sensor_msgs/TimeReference":
    csv_header = ["timestamp", "time_reference"]
    save_data_to_csv(bag, topic, output_topic_folder, csv_header, csv_row_writer_time_reference)

  # Category 2: save every message into a single file
  elif msg_type == "sensor_msgs/Image":
    save_data_to_file_timestamp(bag, topic, output_topic_folder, file_writer_image)

  elif msg_type == "sensor_msgs/PointCloud2":
    save_data_to_file_timestamp(bag, topic, output_topic_folder, file_writer_point_cloud)

  elif msg_type in ["sensor_msgs/NavSatFix", "piksi_rtk_msgs/ReceiverState_V2_4_1"]:
    save_data_to_file_counter(bag, topic, output_topic_folder, file_writer_general_data)

  # Category 3: save only the first message into a file
  elif msg_type == "sensor_msgs/CameraInfo":
    save_data_to_file_first_msg(bag, topic, output_topic_folder, file_writer_general_data)

  # throw a runtime error if the message type is unknown (in fact, this should never happen)
  else:
    raise RuntimeError(f"Message type {msg_type} is unknown and cannot be processed.")


def extract_data_from_bag(bag_path, known_topic_info, output_folder):
  """Extract data from a rosbag and save to output_folder."""
  bag = rosbag.Bag(bag_path, 'r')
  bag_topic_info = bag.get_type_and_topic_info().topics

  # for each topic in the bag, check if it is a known topic and if the message type matches
  for topic, topic_data in bag_topic_info.items():
    if topic not in known_topic_info or topic_data.msg_type != known_topic_info[topic]:
      print(f"Processing rosbag {os.path.basename(bag.filename)}, unknown topic {topic}, skipping")
      continue

    msg_type = known_topic_info[topic]
    print(f"Processing rosbag {os.path.basename(bag.filename)}, topic {topic}, msg_type {msg_type}")
    process_data_by_msg_type(bag, topic, msg_type, output_folder)


def filter_rosbags(src_folder, prefixes_of_interest):
  """Filter rosbags in src_folder by prefixes_of_interest."""
  rosbags_of_interest = []
  for filename in os.listdir(src_folder):
    for prefix in prefixes_of_interest:
      if filename.startswith(prefix):
        rosbags_of_interest.append(filename)
        break
  return rosbags_of_interest


if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Extract data from rosbags.')
  parser.add_argument('src_folder', help='Source folder containing rosbags')
  parser.add_argument('output_folder', help='Output folder to save extracted data')
  args = parser.parse_args()

  # Modify this list as needed, to select those rosbags that you want to process
  rosbag_prefixes_of_interest = ['adk', 'base', 'blackfly', 'mapir', 'odom', 'zed']  
  rosbags_to_process = filter_rosbags(args.src_folder, rosbag_prefixes_of_interest)
  rosbags_to_process.sort()
  print("Reading the following rosbags:")
  for bag in rosbags_to_process:
    print(f"  {bag}")

  # Modify known_topic_info as needed, to include those topics that you want to process

  # Begin processing rosbags
  for bag_name in rosbags_to_process:
    bag_path = os.path.join(args.src_folder, bag_name)
    extract_data_from_bag(bag_path, known_topic_info, args.output_folder)
