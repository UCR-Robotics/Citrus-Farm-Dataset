#!/usr/bin/env python3

import rospy
import numpy as np
from sensor_msgs.msg import Imu

def kalman_filter(x, P, measurement, dt):
  # Process noise covariance
  Q = 0.000001
  # Measurement noise covariance (std is 0.003, so variance is 0.003^2)
  R = 0.003 ** 2

  # Time Update (Prediction)
  x_pred = x + dt
  P_pred = P + Q

  # Measurement Update (Correction)
  K = P_pred / (P_pred + R)
  x_update = x_pred + K * (measurement - x_pred)
  P_update = (1 - K) * P_pred

  return x_update, P_update

class KalmanFilterNode:
  def __init__(self):
    rospy.init_node('kalman_filter_imu_node', anonymous=True)
    self.subscriber = rospy.Subscriber('/microstrain/imu/data', Imu, self.callback)
    self.publisher = rospy.Publisher('/microstrain/imu/data_filtered', Imu, queue_size=10)

    # Initial state and covariance
    self.x = 0.0
    self.P = 1.0

  def callback(self, data):
    # Extract timestamp and convert to seconds
    timestamp = data.header.stamp.to_sec()
    
    # Assuming the time increment is fixed (0.005 seconds)
    dt = 0.005

    # Apply Kalman filter
    self.x, self.P = kalman_filter(self.x, self.P, timestamp, dt)

    # Replace timestamp in the original IMU message
    filtered_stamp = rospy.Time.from_sec(self.x)
    data.header.stamp = filtered_stamp

    # Publish the updated IMU message
    self.publisher.publish(data)

if __name__ == '__main__':
  try:
    node = KalmanFilterNode()
    rospy.spin()
  except rospy.ROSInterruptException:
    pass