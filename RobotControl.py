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

# 
time = 0
target_angle = 90
start_time = 0

algorithm = "find_corner"
state = "turn"
state_next = "forward"
turn_dir = ""

def radToDegree(rad):
    return rad * 180 / PI

def setWheelVelocities(left_velocity, right_velocity):
    left_velocity = left_velocity / 10 * 6.28
    right_velocity = right_velocity / 10 * 6.28

    wheel_left.setVelocity(left_velocity)
    wheel_right.setVelocity(right_velocity)

#=============== Alignment Functions ===============#

last_error, I = 0, 0

def setOrientation(target_angle):
    global last_error, I
    error = yaw - target_angle
    
    if error > 180:
        error -= 360
    elif error < -180:
        error += 360

    P = 0.2 * error

    if abs(error) < 30: I += error * 0.001
    else: I = 0

    D = 0.05 * (error - last_error)    
    last_error = error
    
    speed = P + I + D
    speed = min(max(speed, -10), 10)

    if abs(error) <= 0.1:
        speed = 0
        I = 0

    setWheelVelocities(-speed, speed)

#=============== Alignment Functions ===============#

def alignToClosestWall():
    error = (front_left - front_right) + (right_front - right_back) + (left_front - left_back) + (back_left - back_right)

    if abs(error) > 2: 
        if error > 0:
            setWheelVelocities(3, -3)
        else:
            setWheelVelocities(-3, 3)
    else:
        setWheelVelocities(0, 0)

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

#=============== Utility Functions ===============#

def changeTargetAngle(increase):
    global target_angle

    target_angle = yaw + increase

    if target_angle < -180: target_angle += 360
    elif target_angle > 180: target_angle -= 360

def angleReached(angle):
    if abs(yaw - angle) <= 0.1 or abs(yaw - angle) >= 359.9:
        return True

#=============== Main Loop ===============#

while robot.step(timestep) != -1:
    print(state, time, yaw, target_angle)

    readAllSensors()
    time += 1

    if algorithm == "find_corner":
        if state == "turn": 
            setOrientation(target_angle)

            if angleReached(target_angle):
                if target_angle == -180:
                    algorithm = "snake_sweep"
                
                state = state_next
                time = 0
        
        elif state == "forward":
            setWheelVelocities(10, 10)

            if min(front_left, front_right) < 20:
                if yaw > 45 and yaw < 135:
                    state = "turn"
                    target_angle = 0
                    state_next = "forward"
                
                elif yaw > -45 and yaw < 45:
                    state = "turn"
                    target_angle = -180
                    state_next = "forward"

    elif algorithm == "snake_sweep":
        if state == "forward":
            setWheelVelocities(10, 10)

            if min(front_left, front_right) < 20:
                state = "turn"
                state_next = "forward_time"

                if yaw > -45 and yaw < 45: 
                    changeTargetAngle(-90)
                    turn_dir = -90
                
                elif yaw < -135 or yaw > 135:
                    changeTargetAngle(90)
                    turn_dir = 90

        elif state == "turn": 
            setOrientation(target_angle)

            if angleReached(target_angle):
                state = state_next
                time = 0

        elif state == "forward_time":
            setWheelVelocities(10, 10)

            if time >= 15 or min(front_left, front_right) < 20: 
                state = "turn"
                state_next = "forward"

                changeTargetAngle(turn_dir)
