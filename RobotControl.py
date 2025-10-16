import sys
from Initalise import *
sys.path.append("/Applications/Webots.app/Contents/lib/controller/python")

from controller import Robot, DistanceSensor, Motor, PositionSensor

def radToDegree(rad):
    return rad * 180 / PI

def setWheelVelocities(left_velocity, right_velocity):
    left_velocity = left_velocity / 10 * 6.28
    right_velocity = right_velocity / 10 * 6.28

    wheel_left.setVelocity(left_velocity)
    wheel_right.setVelocity(right_velocity)

# globals for sensor data
x, y, z = 0, 0, 0
front_left, front_right, right_front, right_back, back_left, back_right, left_back, left_front = 0, 0, 0, 0, 0, 0, 0, 0
roll, pitch, yaw = 0, 0, 0
left_wheel_pos, right_wheel_pos = 0, 0

def readAllSensors():
    global x, y, z, front_left, front_right, right_front, right_back, back_left, back_right, left_back, left_front
    global roll, pitch, yaw, left_wheel_pos, right_wheel_pos

    # GPS data
    gps_values = gps_sensor.getValues()
    x = gps_values[0] * 100 
    y = gps_values[1] * 100
    z = gps_values[2] * 100

    # intertial unit data
    compass_values = compass_sensor.getRollPitchYaw()
    roll = radToDegree(compass_values[0])
    pitch = radToDegree(compass_values[1])
    yaw = radToDegree(compass_values[2])

    # distance sensors
    front_left = distance_sensor1.getValue() * 320
    front_right = distance_sensor8.getValue() * 320
    right_front = distance_sensor7.getValue() * 320
    right_back = distance_sensor6.getValue() * 320
    back_left = distance_sensor3.getValue() * 320
    back_right = distance_sensor5.getValue() * 320
    left_back = distance_sensor4.getValue() * 320
    left_front = distance_sensor2.getValue() * 320

    # wheel position sensors
    left_wheel_pos = radToDegree(wheel_left_sensor.getValue())
    right_wheel_pos = radToDegree(wheel_right_sensor.getValue())

def printAllSensors():
    print('=== POSITION & ORIENTATION ===')
    print(f'Position - X: {x:.2f} cm, Y: {y:.2f} cm, Z: {z:.2f} cm')
    print(f'Orientation - Roll: {roll:.2f}°, Pitch: {pitch:.2f}°, Yaw: {yaw:.2f}°')
    
    print('\n=== DISTANCE SENSORS ===')
    print(f'Front left: {front_left:.2f}')
    print(f'Front right: {front_right:.2f}')
    print(f'Right front: {right_front:.2f}')
    print(f'Right back: {right_back:.2f}')
    print(f'Back left: {back_left:.2f}')
    print(f'Back right: {back_right:.2f}')
    print(f'Left back: {left_back:.2f}')
    print(f'Left front: {left_front:.2f}')
    
    print('\n=== WHEEL POSITIONS ===')
    print(f'Left wheel: {left_wheel_pos:.2f}°')
    print(f'Right wheel: {right_wheel_pos:.2f}°')
    print('-' * 50)

while robot.step(timestep) != -1:
    setWheelVelocities(-10, -10)
    readAllSensors()
    printAllSensors()
