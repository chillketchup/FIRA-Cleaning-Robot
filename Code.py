import sys
sys.path.append("/Applications/Webots.app/Contents/lib/controller/python")

from controller import Robot,DistanceSensor
from controller import Motor
from controller import PositionSensor

PI = 3.14159265

robot = Robot()
timestep = int(robot.getBasicTimeStep())

def radToDegree(rad):
    return rad * 180 / PI

def setWheelVelocities(left_velocity, right_velocity):
    left_velocity = left_velocity / 10 * 6.28
    right_velocity = right_velocity / 10 * 6.28

    wheel_left.setVelocity(left_velocity)
    wheel_right.setVelocity(right_velocity)

x, y = 0, 0
front_left, front_right, right_front, right_back, back_left, back_right, left_back, left_front = 0, 0, 0, 0, 0, 0, 0, 0

def readAllSensors():
    global x, y, front_left, front_right, right_front, right_back, back_left, back_right, left_back, left_front

    x = gps_sensor.getValues()[0]*100 
    y = gps_sensor.getValues()[2]*100 

    front_left = distance_sensor1.getValue() * 320
    front_right = distance_sensor8.getValue() * 320
    right_front = distance_sensor7.getValue() * 320
    right_back = distance_sensor6.getValue() * 320
    back_left = distance_sensor3.getValue() * 320
    back_right = distance_sensor5.getValue() * 320
    left_back = distance_sensor4.getValue() * 320
    left_front = distance_sensor2.getValue() * 320

def printAllSensors():
    print('x:', x, 'y:', y)
    print('Front left:', front_left)
    print('Front right:', front_right)
    print('Right front:', right_front)
    print('Right back:', right_back)
    print('Back left', back_left)
    print('Back_right', back_right)
    print('Left_back', left_back)
    print('Left front', left_front)

wheel_left = robot.getDevice('wheel1 motor')
wheel_left.setPosition(float('inf'))
wheel_right = robot.getDevice('wheel2 motor')
wheel_right.setPosition(float('inf'))

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

gps_sensor = robot.getDevice('gps')
gps_sensor.enable(timestep)

compass_sensor = robot.getDevice('inertial_unit')
compass_sensor.enable(timestep)

emitter = robot.getDevice('emitter')
emitter.setChannel(1)
emitter.send('john'.encode('utf-8'))


while robot.step(timestep) != -1:
    setWheelVelocities(-10, -10)
    readAllSensors()
    printAllSensors()
