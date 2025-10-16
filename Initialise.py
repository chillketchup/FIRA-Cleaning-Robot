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