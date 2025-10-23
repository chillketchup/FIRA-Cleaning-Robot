import sys
sys.path.append("/Applications/Webots.app/Contents/lib/controller/python")

from controller import Robot, DistanceSensor, Motor, PositionSensor

PI = 3.14159265

robot = Robot()
timestep = int(robot.getBasicTimeStep())

# motor setup
wheel_left = robot.getDevice('wheel1 motor')
wheel_left.setPosition(float('inf'))
wheel_right = robot.getDevice('wheel2 motor')
wheel_right.setPosition(float('inf'))

# wheel position sensors
wheel_left_sensor = robot.getDevice('wheel1 sensor')
wheel_left_sensor.enable(timestep)
wheel_right_sensor = robot.getDevice('wheel2 sensor')
wheel_right_sensor.enable(timestep)

# distance sensors
distance_sensor1 = robot.getDevice('D1')
distance_sensor1.enable(timestep)
distance_sensor2 = robot.getDevice('D2')
distance_sensor2.enable(timestep)
distance_sensor3 = robot.getDevice('D3')
distance_sensor3.enable(timestep)
distance_sensor4 = robot.getDevice('D4')
distance_sensor4.enable(timestep)
distance_sensor5 = robot.getDevice('D5')
distance_sensor5.enable(timestep)
distance_sensor6 = robot.getDevice('D6')
distance_sensor6.enable(timestep)
distance_sensor7 = robot.getDevice('D7')
distance_sensor7.enable(timestep)
distance_sensor8 = robot.getDevice('D8')
distance_sensor8.enable(timestep)

# GPS and orientation sensors
gps_sensor = robot.getDevice('gps')
gps_sensor.enable(timestep)

compass_sensor = robot.getDevice('inertial_unit')
compass_sensor.enable(timestep)

emitter = robot.getDevice('emitter')
emitter.setChannel(1)
emitter.send('john'.encode('utf-8'))

# globals for sensor data
x, y, z = 0, 0, 0
front_left, front_right, right_front, right_back, back_left, back_right, left_back, left_front = 0, 0, 0, 0, 0, 0, 0, 0
roll, pitch, yaw = 0, 0, 0
left_wheel_pos, right_wheel_pos = 0, 0

def radToDegree(rad):
    return rad * 180 / PI

def setWheelVelocities(left_velocity, right_velocity):
    left_velocity = left_velocity / 10 * 6.28
    right_velocity = right_velocity / 10 * 6.28

    wheel_left.setVelocity(left_velocity)
    wheel_right.setVelocity(right_velocity)

#=============== Alighment Functions ===============#

def setOrientation(target_angle):
    error = target_angle - yaw
    if error > 180:
        error -= 360
    elif error < -180:
        error += 360
    
    speed = 0.2 * error
    speed = min(max(speed, -10), 10)

    setWheelVelocities(speed, -speed)
    if abs(error) < 2: setWheelVelocities(0, 0)

def alignToClosestWall():
    error = (front_left - front_right) + (right_front - right_back) + (left_front - left_back) + (back_left - back_right)

    if abs(error) > 2: 
        if error > 0:
            setWheelVelocities(3, -3)
        else:
            setWheelVelocities(-3, 3)
    else:
        setWheelVelocities(0, 0)

# def alignToWall(sensor1, sensor2):
#         error = sensor1 - sensor2
        
#         if abs(error) > 2: 
#             if error > 0:
#                 setWheelVelocities(3, -3)
#             else:
#                 setWheelVelocities(-3, 3)
#         else:
#             setWheelVelocities(0, 0)

# def findClosestWall():
#     distances = {
#         'front': front_left + front_right,
#         'right': right_front + right_back,
#         'left': left_front + left_back,
#         'back': back_left + back_right,
#     }
    
#     closest_wall = min(distances, key=distances.get)
    
#     if closest_wall == 'front':
#         alignToWall(front_left, front_right)
#     elif closest_wall == 'right':
#         alignToWall(right_front, right_back)
#     elif closest_wall == 'left':
#         alignToWall(left_front, left_back)
#     else:
#         alignToWall(back_left, back_right)

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
    readAllSensors()
    printAllSensors()
    setOrientation(90)
