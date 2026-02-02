# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       solved.py                                                     #
# 	Author:       magicgear                                                    #
# 	Created:      8/16/2025, 6:09:00 PM                                        #
# 	Description:  V5 project with dual controller support                     #
#               Controller 1: Movement (drivetrain)                           #
#               Controller 2: Intake systems                                  #
#                                                                              #
# ---------------------------------------------------------------------------- #

# Library imports
from vex import *
from math import atan, degrees, sin, radians, cos, ceil, floor,sqrt, tan, asin

#DO NOT ADD PI KUBA!!!!!!

dont_stop_twice = 0
test_function = 0

brain = Brain()
gyro_360 = 360

def calibratedAngle(idealAngle):
    return (idealAngle * gyro_360/360)
        
distance = 0
collision_funct_stopper = 0
final_object_angle = []
# actions to do when the program starts
brain.screen.clear_screen()

left_tube_spin = 0
right_tube_spin = 0

# Brain and Controllers

#smallest_distance_value = 100000
#smallest_distance_angle = 0

# Configure the optical sensor on a specific port (change port number as needed)
DigInMatch = DigitalIn(brain.three_wire_port.g)
DigOutMatch = DigitalOut(brain.three_wire_port.g)
Digin = DigitalIn(brain.three_wire_port.h)
Digout = DigitalOut(brain.three_wire_port.h)
bumper = Bumper(brain.three_wire_port.a)
potentiometer = Potentiometer(brain.three_wire_port.b) 
distance_sensor = Distance(Ports.PORT9)
distance_sensor_back = Distance(Ports.PORT2)
inertial_sensor = Inertial(Ports.PORT1)
optical = Optical(Ports.PORT5)
controller_1 = Controller(ControllerType.PRIMARY)    # MOVEMENT CONTROLLER
controller_2 = Controller(ControllerType.PARTNER)    # INTAKE CONTROLLER
bumper_was_pressing = 0

# Global variables
MAX_SPEED = 40
MOTOR_MULTIPLIER = 10  # Multiplier for motor control speeds
controllerMode = 0
auton = 0
hopper_running = 0
b_was_pressed = 0
vex_brain_slot = 2 # 1 = left, 2 = right Auton

brain.screen.print("Hello V5 - Movement/Intake Split")

# Create the left Motors and group them under the MotorGroup "left_motors"
left_motor_a = Motor(Ports.PORT19, GearSetting.RATIO_18_1, False)
left_motor_b = Motor(Ports.PORT12, GearSetting.RATIO_18_1, False)
left_motor_c = Motor(Ports.PORT20, GearSetting.RATIO_18_1, False)



# Create the right Motors and group them under the MotorGroup "right_motors"
right_motor_a = Motor(Ports.PORT14, GearSetting.RATIO_18_1, True)
right_motor_b = Motor(Ports.PORT16, GearSetting.RATIO_18_1, True)
right_motor_c = Motor(Ports.PORT8, GearSetting.RATIO_18_1, True)
left_motor_b.set_reversed(False)
left_motor_a.set_reversed(False)
right_motor_a.set_reversed(True)
if left_motor_c.installed():
    right_motors = MotorGroup(right_motor_a, right_motor_b, right_motor_c)
    left_motors = MotorGroup(left_motor_a, left_motor_b, left_motor_c)

else:
    right_motors = MotorGroup(right_motor_a, right_motor_b)
    left_motors = MotorGroup(left_motor_a, left_motor_b)
#FORWARD = REVERSE
#REVERSE = FORWARD
tube_intake_motor = Motor(Ports.PORT3, GearSetting.RATIO_18_1, True)


#set_position Sets the starting position of the tube intake motor to 0 degrees so that it will not block distance sensor
tube_intake_motor.set_position(0, DEGREES)


# Construct a 4-Motor Drivetrain
# Parameters: circumference, distance between wheels on axle, distance between axles, units, gear ratio
#drivetrain = DriveTrain(left_motors, right_motors, 330, 335, 231, MM, 1)
drivetrain = SmartDrive(left_motors, right_motors, inertial_sensor,330, 335, 231, MM, 1)


# Intake/Mechanism motors
first_intake = Motor(Ports.PORT11, GearSetting.RATIO_18_1, True)
basket_intake_motor = Motor(Ports.PORT6, GearSetting.RATIO_18_1, False)
toprack = Motor(Ports.PORT8, GearSetting.RATIO_18_1, False)


LEFT = 1
RIGHT = 0


def ramp_up(input_percent):
    if (input_percent < 50):
        return input_percent * 0.5
    elif (input_percent < 75):
        return input_percent * 0.75
    else:
        return input_percent
    


def outake_empty():
    empty_timer = 0
    first_time = brain.timer.time(SECONDS)
    first_intake.spin(FORWARD, 50, PERCENT)
    basket_intake_motor.spin(FORWARD, 50, PERCENT)
    toprack.spin(FORWARD, 50, PERCENT)
    print(brain.timer.time(SECONDS))
    while empty_timer < 16 and brain.timer.time(SECONDS) - first_time < 10: 
     if basket_intake_motor.current() < 0.5:
        wait(0.1, SECONDS)
        empty_timer +=1 
     else:
        empty_timer = 0
        print(brain.timer.time(SECONDS) - first_time)

    basket_intake_motor.stop()
    first_intake.stop()
    toprack.stop()
    

        


    





def find_objects_in_data(data_set):

    global final_object_angle
    data = [((359.0),(753.0)),
        ((359.0087),(741.0)),
        ((359.0102),(746.0)),
        ((358.4795),(728.0)),
        ((355.2454),(135.0)),
        ((350.8036),(123.0)),
        ((347.172),(132.0)),
        ((344.0994),(145.0)),
        ((340.5105),(171.0)),
        ((336.7918),(980.9999)),
        ((333.8525),(969.0)),
        ((329.9612),(930.0)),
        ((326.2497),(892.0)),
        ((323.4548),(199.0)),
        ((319.0367),(194.0)),
        ((315.6708),(192.0)),
        ((312.3238),(196.0)),
        ((308.3157),(208.0)),
        ((305.453),(224.0)),
        ((301.2501),(786.0)),
        ((297.505),(797.0)),
        ((294.6898),(808.0)),
        ((290.2702),(811.0)),
        ((286.8119),(826.0)),
        ((283.6574),(841.0)),
        ((279.266),(866.0)),
        ((276.4171),(905.9999)),
        ((272.8502),(934.9999)),((359.0),(753.0)),
        ((359.0087),(741.0)),
        ((359.0102),(746.0)),
        ((358.4795),(728.0)),
        ((355.2454),(135.0)),
        ((350.8036),(123.0)),
        ((347.172),(132.0)),
        ((344.0994),(145.0)),
        ((340.5105),(171.0)),
        ((336.7918),(980.9999)),
        ((333.8525),(969.0)),
        ((329.9612),(930.0)),
        ((326.2497),(892.0)),
        ((323.4548),(199.0)),
        ((319.0367),(194.0)),
        ((315.6708),(192.0)),
        ((312.3238),(196.0)),
        ((308.3157),(208.0)),
        ((305.453),(224.0)),
        ((301.2501),(786.0)),
        ((297.505),(797.0)),
        ((294.6898),(808.0)),
        ((290.2702),(811.0)),
        ((286.8119),(826.0)),
        ((283.6574),(841.0)),
        ((279.266),(866.0)),
        ((276.4171),(905.9999)),
            ((272.8502),(934.9999)),((359.0),(753.0)),
        ((359.0087),(741.0)),
        ((359.0102),(746.0)),
        ((358.4795),(728.0)),
        ((355.2454),(135.0)),
        ((350.8036),(123.0)),
        ((347.172),(132.0)),
        ((344.0994),(145.0)),
        ((340.5105),(171.0)),
        ((336.7918),(980.9999)),
        ((333.8525),(969.0)),
        ((329.9612),(930.0)),
        ((326.2497),(892.0))]

    Num_of_objects = 0
    shift_down_in_range = 0
    previous_distance = 0
    widths_of_objects = []
    #object_item_on_list = []
    Number_of_cycles = 0
    current_object = []
    final_object_angle = []


    for i in data_set:
        print ("data set not empty" + str(len(data_set)))
        Number_of_cycles += 1
        if i[1] < previous_distance/1.5:
            shift_down_in_range = 1
            current_object = []
        elif shift_down_in_range > 0:
            shift_down_in_range += 1
            current_object.append((i[0], i[1]))
        if i[1] > previous_distance + 100 and shift_down_in_range > 0:
            print ("i am appending  " + str(Num_of_objects))
            Num_of_objects = Num_of_objects + 1 
            
            widths_of_objects.append(current_object)
            shift_down_in_range = 0
        previous_distance = i[1]

    print (data_set)


        
    for i_smalllist in widths_of_objects:
       # print ("found an object" + str(len(i_smalllist)))
        print ("lucas is awesome 23")
        target_index = math.floor(len(i_smalllist)/2)
        target_item = i_smalllist[target_index]
        final_object_angle.append(target_item)
       # print(target_item)
        

    print(final_object_angle)    
    return (final_object_angle)

def fix_angle_left(range,difference):
    #if range - difference > 0:
    #    final_angle = range - difference - 360
    #else:
    final_angle = range - difference

    if final_angle > 5:
        final_angle = final_angle - 360
    return final_angle
    #current_gyro_angle = range
    #if current_gyro_angle < 10 and current_gyro_angle > 0:
    #    current_gyro_angle += 360
    #return current_gyro_angle

def convert_relative_to_absolute(relative_angle):

    absolute_angle = relative_angle + inertial_sensor.heading()
    if absolute_angle < 0:
        absolute_angle += 360


    #if relative_angle < 0:
    #    absolute_angle = inertial_sensor.heading() + relative_angle + 360
    #else:
    #    absolute_angle = inertial_sensor.heading() + relative_angle

    return absolute_angle


def convert_absolute_to_relative(absolute_angle):

    relative_angle = absolute_angle
    if relative_angle > 180:
        relative_angle = relative_angle - 360


    #if relative_angle < 0:
    #    absolute_angle = inertial_sensor.heading() + relative_angle + 360
    #else:
    #    absolute_angle = inertial_sensor.heading() + relative_angle

    return relative_angle
# def turn_until_dist_drop(speed, direction, threshold = 150):
    
#     initial_dist = distance_sensor.object_distance(MM)
#     if direction == "left":
#         while initial_dist 
#             left_motors.spin(FORWARD, speed, PERCENT)
def intake_from_tube():
    global collision_funct_stopper
    print("collision")
    if collision_funct_stopper == 1:
        drivetrain.stop()
        print("action!")
        collision_funct_stopper +=1
        drivetrain.drive_for(REVERSE,0.5,INCHES)
        first_intake.spin(FORWARD, 100, PERCENT)
        basket_intake_motor.spin(FORWARD, 100, PERCENT)
        wait(10000, MSEC)
        first_intake.stop()
        basket_intake_motor.stop()



def color_sort(color, ball_count):
    run_basket = 0
    saw_ball=0
    empty_timer = 0
    optical.set_light_power(100)
    optical.set_light(LedStateType.ON)
    balls_sorted = 0
    first_intake.spin(FORWARD, 35, PERCENT)
    basket_intake_motor.spin(FORWARD, 50, PERCENT)
    while ball_count > balls_sorted:
        if run_basket < 100:
                basket_intake_motor.spin(FORWARD, 50, PERCENT)
                run_basket += 1
        elif run_basket < 150:
                basket_intake_motor.stop()
                run_basket += 1
        else:
                run_basket = 0
        if color == "blue":
                if optical.hue() < 250 and optical.hue() > 200:
                    if saw_ball < 10:
                        saw_ball += 1
                    else:
                        print(optical.hue())
                        wait(0.2,SECONDS)
                        toprack.spin(REVERSE, 75, PERCENT)
                        wait(0.65,SECONDS)
                        toprack.stop()
                        balls_sorted += 1
                else: 
                    saw_ball = 0
                wait (0.01,SECONDS)
        elif color == "red":
            if optical.hue() < 11 and optical.hue() > 5:
                if saw_ball < 10:
                    saw_ball += 1
                else:
                    controller_1.rumble('.-.')    
                    print(optical.hue())
                    wait(0.2,SECONDS)
                    toprack.spin(REVERSE, 75, PERCENT)
                    wait(0.65,SECONDS)
                    toprack.stop()
                    balls_sorted += 1
            else: 
                saw_ball = 0
            wait (0.01,SECONDS)
    first_intake.stop()
    basket_intake_motor.stop()
        



def search_for_objects(range_degrees,sensor="BACK"):
    #global smallest_distance_value
    #global smallest_distance_angle
    #global final_object_angle
    print("lucas is cool3")
    #controller_1.rumble('......')
    # while inertial_sensor.is_calibrating():
    #     controller_1.screen.set_cursor(2,1)

    #     controller_1.screen.print("Calibrating Gyro")
    #     wait(100, MSEC)
    #inertial_sensor.reset_rotation()



    if range_degrees < 0:
        direction = LEFT
    else:
        direction = RIGHT

    
    print("enzo" + str(range_degrees))
    controller_1.screen.clear_screen()
    print("we finished calibrating")
    distance_data = []

    if sensor == "FRONT":

        if direction == LEFT:
            difference = inertial_sensor.heading()
            #print("in the left" + str(inertial_sensor.heading()) + " " + str(range_degrees))
            #inertial_sensor.set_heading(359, DEGREES)  
            #print (range_degrees)
            print(inertial_sensor.heading())
            while range_degrees < fix_angle_left(inertial_sensor.heading(), difference):
                print("im in while loop" + "  " +str(fix_angle_left(inertial_sensor.heading(), difference)) + "  " + str(distance_sensor.object_distance(MM))+ str(range_degrees)) 
                distance_data.append((inertial_sensor.heading(), distance_sensor.object_distance(MM)))

                left_motors.spin(REVERSE,5,PERCENT)
                right_motors.spin(FORWARD,5,PERCENT)
                wait (100,MSEC)

            print("finished moving motors" + str(fix_angle_left(inertial_sensor.heading(), difference)))    

            right_motors.stop()
            left_motors.stop()
        else:
            difference = inertial_sensor.heading()
            print("in the right" + str(inertial_sensor.heading()) + " " + str(range_degrees))
            #inertial_sensor.set_heading(359, DEGREES)        
            while range_degrees > (inertial_sensor.heading() - difference):
                print("im in while loop" + "  " +str(inertial_sensor.heading()) + "  " + str(distance_sensor.object_distance(MM))) 
                distance_data.append((inertial_sensor.heading(), distance_sensor.object_distance(MM)))

                left_motors.spin(FORWARD,5,PERCENT)
                right_motors.spin(REVERSE,5,PERCENT)
                wait (100,MSEC)

            print("finished moving motors")    

            right_motors.stop()
            left_motors.stop()
    else:
        if direction == LEFT:
            difference = inertial_sensor.heading()
            #print("in the left" + str(inertial_sensor.heading()) + " " + str(range_degrees))
            #inertial_sensor.set_heading(359, DEGREES)  
            #print (range_degrees)
            print(inertial_sensor.heading())
            while range_degrees < fix_angle_left(inertial_sensor.heading(), difference):
                print("im in while loop" + "  " +str(fix_angle_left(inertial_sensor.heading(), difference)) + "  " + str(distance_sensor_back.object_distance(MM))+ str(range_degrees)) 
                distance_data.append((inertial_sensor.heading(), distance_sensor_back.object_distance(MM)))

                left_motors.spin(REVERSE,5,PERCENT)
                right_motors.spin(FORWARD,5,PERCENT)
                wait (100,MSEC)

            print("finished moving motors" + str(fix_angle_left(inertial_sensor.heading(), difference)))    

            right_motors.stop()
            left_motors.stop()
        else:
            difference = inertial_sensor.heading()
            print("in the right" + str(inertial_sensor.heading()) + " " + str(range_degrees))
            #inertial_sensor.set_heading(359, DEGREES)        
            while range_degrees > (inertial_sensor.heading() - difference):
                print("im in while loop" + "  " +str(inertial_sensor.heading()) + "  " + str(distance_sensor_back.object_distance(MM))) 
                distance_data.append((inertial_sensor.heading(), distance_sensor_back.object_distance(MM)))

                left_motors.spin(FORWARD,5,PERCENT)
                right_motors.spin(REVERSE,5,PERCENT)
                wait (100,MSEC)

            print("finished moving motors")    

            right_motors.stop()
            left_motors.stop()

    print("done gathering data")
    smallest_distance = 100000
    smallest_distance_angle = 0
    final_object_angle = find_objects_in_data(distance_data)
    # for i in distance_data:
    #     if i[1] < smallest_distance:
    #         smallest_distance = i[1]
    #         smallest_distance_angle = i[0]
    #     print("((" + str(i[0]) + "),(" + str(i[1]) + ")),")
    # print("exiting")
    print("smallest v   distance " + str(smallest_distance) + " at angle " + str(smallest_distance_angle))

    smallest_distance_value = 100000
    smallest_distance_angle = 0
    for i in final_object_angle:
        if i[1] < smallest_distance_value:
            smallest_distance_value = i[1]
            smallest_distance_angle = i[0]

    print(smallest_distance_angle)
    if smallest_distance_value == 100000:
        smallest_distance_value = -1
    return (smallest_distance_angle, smallest_distance_value)
    #drivetrain.turn_to_heading(smallest_distance_angle, DEGREES, wait=True)



def search_for_objects_back(range_degrees):
    #global smallest_distance_value
    #global smallest_distance_angle
    #global final_object_angle
    print("lucas is cool3")
    #controller_1.rumble('......')
    # while inertial_sensor.is_calibrating():
    #     controller_1.screen.set_cursor(2,1)

    #     controller_1.screen.print("Calibrating Gyro")
    #     wait(100, MSEC)
    #inertial_sensor.reset_rotation()



    if range_degrees < 0:
        direction = LEFT
    else:
        direction = RIGHT

    
    print("enzo" + str(range_degrees))
    controller_1.screen.clear_screen()
    print("we finished calibrating")
    distance_data = []

    if direction == LEFT:
        difference = inertial_sensor.heading()
        #print("in the left" + str(inertial_sensor.heading()) + " " + str(range_degrees))
        #inertial_sensor.set_heading(359, DEGREES)  
        #print (range_degrees)
        print(inertial_sensor.heading())
        while range_degrees < fix_angle_left(inertial_sensor.heading(), difference):
            print("im in while loop" + "  " +str(fix_angle_left(inertial_sensor.heading(), difference)) + "  " + str(distance_sensor_back.object_distance(MM))+ str(range_degrees)) 
            distance_data.append((inertial_sensor.heading(), distance_sensor_back.object_distance(MM)))

            left_motors.spin(REVERSE,5,PERCENT)
            right_motors.spin(FORWARD,5,PERCENT)
            wait (100,MSEC)

        print("finished moving motors" + str(fix_angle_left(inertial_sensor.heading(), difference)))    

        right_motors.stop()
        left_motors.stop()
    else:
        difference = inertial_sensor.heading()
        print("in the right" + str(inertial_sensor.heading()) + " " + str(range_degrees))
        #inertial_sensor.set_heading(359, DEGREES)        
        while range_degrees > (inertial_sensor.heading() - difference):
            print("im in while loop" + "  " +str(inertial_sensor.heading()) + "  " + str(distance_sensor_back.object_distance(MM))) 
            distance_data.append((inertial_sensor.heading(), distance_sensor_back.object_distance(MM)))

            left_motors.spin(FORWARD,5,PERCENT)
            right_motors.spin(REVERSE,5,PERCENT)
            wait (100,MSEC)

        print("finished moving motors")    

        right_motors.stop()
        left_motors.stop()

    print("done gathering data")
    smallest_distance = 100000
    smallest_distance_angle = 0
    final_object_angle = find_objects_in_data(distance_data)
    # for i in distance_data:
    #     if i[1] < smallest_distance:
    #         smallest_distance = i[1]
    #         smallest_distance_angle = i[0]
    #     print("((" + str(i[0]) + "),(" + str(i[1]) + ")),")
    # print("exiting")
    print("smallest v   distance " + str(smallest_distance) + " at angle " + str(smallest_distance_angle))

    smallest_distance_value = 100000
    smallest_distance_angle = 0
    for i in final_object_angle:
        if i[1] < smallest_distance_value:
            smallest_distance_value = i[1]
            smallest_distance_angle = i[0]

    print(smallest_distance_angle)
    if smallest_distance_value == 100000:
        smallest_distance_value = -1
    return (smallest_distance_angle, smallest_distance_value)
    #drivetrain.turn_to_heading(smallest_distance_angle, DEGREES, wait=True)


def back_until_yaw(left_or_right,amount,speed):
    if left_or_right == "left":
        # inertial_sensor.reset_heading()
        while convert_absolute_to_relative(inertial_sensor.heading()) > convert_absolute_to_relative(amount):
            wait(50)
            controller_1.screen.clear_screen()
            controller_1.screen.set_cursor(3,1)
            controller_1.screen.print("Enzo")
            controller_1.screen.print(inertial_sensor.heading())
            left_motors.spin(REVERSE,speed,PERCENT)
            right_motors.spin(REVERSE,speed,PERCENT)
        right_motors.stop()
        left_motors.stop()
        controller_1.screen.clear_screen()
        controller_1.screen.set_cursor(3,1)
        controller_1.screen.print("Finished")
        controller_1.screen.print(convert_absolute_to_relative(amount))
        

def ball_sucker(direction, top_range, bottom_range):
    #forward_dist = distance_sensor.object_distance(MM)
    if direction == 'left':
        while distance_sensor.object_distance(MM) > top_range or distance_sensor.object_distance(MM) < bottom_range:
            left_motors.spin(REVERSE,10,PERCENT)
            right_motors.spin(FORWARD,10,PERCENT)
            #drivetrain.turn_to_heading(calibratedAngle(inertial_sensor.heading() - 2), DEGREES, wait=True)
        left_motors.stop()
        right_motors.stop()
            
        forward_dist = distance_sensor.object_distance(MM)

        target_angle = inertial_sensor.heading() - degrees(atan(120/forward_dist)) 
        controller_1.screen.clear_screen()
        controller_1.screen.print(target_angle)
        controller_1.screen.set_cursor(3,1)
        controller_1.screen.print(inertial_sensor.heading())


        drivetrain.turn_to_heading(target_angle, DEGREES, wait=True)
        actual_distance = forward_dist / cos(atan(114 / forward_dist))
        
      
        drivetrain.drive_for(FORWARD, actual_distance + 20, MM, 10, PERCENT)
    elif direction == 'right':
        while distance_sensor.object_distance(MM) > top_range or distance_sensor.object_distance(MM) < bottom_range:
            left_motors.spin(FORWARD,10,PERCENT)
            right_motors.spin(REVERSE,10,PERCENT)
            #drivetrain.turn_to_heading(calibratedAngle(inertial_sensor.heading() - 2), DEGREES, wait=True)
        left_motors.stop()
        right_motors.stop()
            
        forward_dist = distance_sensor.object_distance(MM)

        target_angle = inertial_sensor.heading() - degrees(atan(120/forward_dist)) 
        controller_1.screen.clear_screen()
        controller_1.screen.print(target_angle)
        controller_1.screen.set_cursor(3,1)
        controller_1.screen.print(inertial_sensor.heading())
        if target_angle < 0:
            target_angle = target_angle + 360


        drivetrain.turn_to_heading(target_angle, DEGREES, wait=True)
        actual_distance = forward_dist / cos(atan(114 / forward_dist))
        
        
        drivetrain.drive_for(FORWARD, actual_distance + 20, MM, 10, PERCENT)
        


def one_wheel_turn_to_heading(target_heading, side, direction,speed):
    
    #drivetrain.drive_for(REVERSE,12, INCHES, 50, PERCENT )
    if side == 'left':
        # while angle is not in the target range
        # not ( angle < target + 10 and angle > target - 10 )
        # left


        while not (inertial_sensor.heading() > target_heading - 5 and inertial_sensor.heading() < target_heading + 5):
            left_motors.spin(direction, speed, PERCENT)
            controller_1.screen.clear_screen()
            controller_1.screen.set_cursor(1,1)
            controller_1.screen.print(inertial_sensor.heading())

            
    if side == 'right':
        while not (inertial_sensor.heading() > target_heading - 5 and inertial_sensor.heading() < target_heading + 5):
            right_motors.spin(direction, 25, PERCENT)
    left_motors.stop()
    right_motors.stop()
    return()





def hopper_pickup():
    SCALE_VALUE = 0.6
    global MAX_SPEED
    
    drivetrain.turn_for(RIGHT, 20 * SCALE_VALUE, DEGREES, 25, PERCENT)
    drivetrain.turn_for(LEFT, 20 * SCALE_VALUE, DEGREES, 25, PERCENT)
    drivetrain.drive_for(FORWARD, 10, MM, 50, PERCENT)
    
def turn_until_distance(distance,direction,speed, sensor_location):
    if sensor_location == "FRONT":
        while distance_sensor.object_distance(MM) > distance:
            if direction == 'left':
                if left_motor_c.installed():
                    left_motors.spin(REVERSE,speed,PERCENT)
                    right_motors.spin(FORWARD,speed,PERCENT)
                else: 
                    left_motors.spin(FORWARD,speed,PERCENT)
                    right_motors.spin(REVERSE,speed,PERCENT)
            elif direction == 'right':
                if left_motor_c.installed():
                    left_motors.spin(FORWARD,speed,PERCENT)
                    right_motors.spin(REVERSE,speed,PERCENT)
                else: 
                    left_motors.spin(REVERSE,speed,PERCENT)
                    right_motors.spin(FORWARD,speed,PERCENT)
    else:
         while distance_sensor_back.object_distance(MM) > distance:
            if direction == 'left':
                if left_motor_c.installed():
                    left_motors.spin(REVERSE,speed,PERCENT)
                    right_motors.spin(FORWARD,speed,PERCENT)
                else: 
                    left_motors.spin(FORWARD,speed,PERCENT)
                    right_motors.spin(REVERSE,speed,PERCENT)
            elif direction == 'right':
                if left_motor_c.installed():
                    left_motors.spin(FORWARD,speed,PERCENT)
                    right_motors.spin(REVERSE,speed,PERCENT)
                else: 
                    left_motors.spin(REVERSE,speed,PERCENT)
                    right_motors.spin(FORWARD,speed,PERCENT)


    left_motors.stop()
    right_motors.stop()
    return

def move_until_distance(distance,direction,speed, sensor_location):
    sensed_once = 0
    if sensor_location == "FRONT":
        if direction == 'forward':
        
            while sensed_once < 1:
                if left_motor_c.installed(): 
                    left_motors.spin(REVERSE,speed,PERCENT)
                    right_motors.spin(REVERSE,speed,PERCENT)
                else: 
                    left_motors.spin(FORWARD,speed,PERCENT)
                    right_motors.spin(FORWARD,speed,PERCENT)
                if distance_sensor.object_distance() < distance:
                    sensed_once += 1
                else:
                    sensed_once = 0
        elif direction == 'reverse':
            while distance_sensor.object_distance(MM)< distance:

                if left_motor_c.installed(): 
                    left_motors.spin(FORWARD,speed,PERCENT)
                    right_motors.spin(FORWARD,speed,PERCENT)
                else: 
                    left_motors.spin(REVERSE,speed,PERCENT)
                    right_motors.spin(REVERSE, speed,PERCENT)

    elif sensor_location == "BACK":
        if direction == 'forward':
            while distance_sensor_back.object_distance(MM) < distance:

                if left_motor_c.installed(): 
                    left_motors.spin(REVERSE,speed,PERCENT)
                    right_motors.spin(REVERSE,speed,PERCENT)
                else: 
                    left_motors.spin(FORWARD,speed,PERCENT)
                    right_motors.spin(FORWARD,speed,PERCENT)
        elif direction == 'reverse':
            while distance_sensor_back.object_distance(MM) > distance:

                if left_motor_c.installed(): 
                    left_motors.spin(FORWARD,speed,PERCENT)
                    right_motors.spin(FORWARD,speed,PERCENT)
                else: 
                    left_motors.spin(REVERSE,speed,PERCENT)
                    right_motors.spin(REVERSE, speed,PERCENT)

        
    left_motors.stop()
    right_motors.stop()
    return


def outake_four_balls():
    controller_1.screen.clear_screen()
    controller_1.screen.set_cursor(1,1)
    controller_1.screen.print("Outtake4")
    first_intake.spin(REVERSE,100,PERCENT)
    basket_intake_motor.spin(FORWARD,100,PERCENT)
    toprack.spin(REVERSE, 100, PERCENT)
    wait(10)
    toprack.stop()
    first_intake.stop()
    basket_intake_motor.stop()
    move_until_distance(40,'forward',30,"BACK")
    drivetrain.turn_to_heading(45,DEGREES,20,PERCENT)


def turnTestingAuton():
    # reset the gyro sensor to 0 degrees
    #change all Gyro to inertial
    inertial_sensor.calibrate()
    controller_1.screen.clear_screen()
    controller_1.screen.set_cursor(1,1)
    controller_1.screen.print("turnTestingAuton 1.1")

    while inertial_sensor.is_calibrating():
        controller_1.screen.set_cursor(2,1)

        controller_1.screen.print("Calibrating Gyro")
        wait(100, MSEC)
    inertial_sensor.reset_rotation()
    inertial_sensor.set_heading(0, DEGREES)
    
    # turn to 90 degrees
    drivetrain.turn_to_heading(calibratedAngle(90), DEGREES, wait=True)
    controller_1.screen.set_cursor(3,1)    
    controller_1.screen.print("[90=]")
    controller_1.screen.print(inertial_sensor.heading(DEGREES))
    # wait for a moment
    wait(1, SECONDS)
    
    # turn to 180 degrees
    drivetrain.turn_to_heading(calibratedAngle(180), DEGREES, wait=True)
    
    # wait for a moment
    wait(1, SECONDS)
    
    # turn to 270 degrees
    drivetrain.turn_to_heading(calibratedAngle(270), DEGREES, wait=True)
    
    # wait for a moment
    wait(1, SECONDS)
    
    # turn to 0 degrees
    drivetrain.turn_to_heading(calibratedAngle(0), DEGREES, wait=True)
    
    # wait for a moment
    wait(1, SECONDS)
    
    # end of auton
    drivetrain.stop()


def collect_balls():
    first_intake.spin(FORWARD, 100, PERCENT)
    basket_intake_motor.spin(REVERSE, 100, PERCENT)
    drivetrain.drive_for(FORWARD,8, INCHES, 25, PERCENT )
    drivetrain.drive_for(FORWARD, 16, INCHES, 10, PERCENT)
def turn_to_balls():
    ideal_pickup_angle = inertial_sensor.heading(DEGREES) - 18
    if ideal_pickup_angle < 0:
        ideal_pickup_angle += 360
    one_wheel_turn_to_heading(ideal_pickup_angle, 'left', REVERSE,10)
    collect_balls()


def twenty_point_skills():

    first_intake.spin(FORWARD,100,PERCENT)
    basket_intake_motor.spin(REVERSE,100,PERCENT)
    tube_intake_motor.spin(REVERSE,100,PERCENT)
    wait(5,SECONDS)

    drivetrain.drive_for(FORWARD, 22, INCHES) 

    wait(10,SECONDS)
    first_intake.stop()
    basket_intake_motor.stop()
    tube_intake_motor.stop()



def stop_motors():
    left_motors.stop()
    right_motors.stop()


def skills_auton():
    newauton_mainfunc()
    return
    # global MAX_SPEED
    # vex_brain_slot = 1
    # kuba = 0
    # caleb = 1
    # lucas = 0
    
    
   
    # controller_1.screen.set_cursor(2,1)

    # #controller_1.rumble("....--.-.- -. -.--- .---.---.---.- ..--.-..-..-.-..-.----.-.-.-..-.-----.-...-.-...-.-...-.--.-..-.-.-..-.-...")
    # wait(100, MSEC)  
    # if lucas == 1:
    #     Digout.set(False)
    #     tube_intake_motor.spin(FORWARD,100,PERCENT)
    #     wait(2000,MSEC)
    #     tube_intake_motor.stop()
    #     one_wheel_turn_to_heading(270,'left',REVERSE)
    #     drivetrain.drive_for(REVERSE, 6, INCHES)
    #     drivetrain.turn_to_heading(180,DEGREES,wait=True)
    #     move_until_distance(500,'forward',30,"FRONT")
    #     controller_1.rumble("...--")
    #     drivetrain.turn_to_heading(270,DEGREES,20,PERCENT)
    #     Digout.set(False)
    #     first_intake.spin(REVERSE,100,PERCENT)
    #     basket_intake_motor.spin(REVERSE,100,PERCENT)
    #     left_motors.spin(FORWARD,100,PERCENT)
    #     right_motors.spin(FORWARD,100,PERCENT)
    #     #nertial_sensor.collision(stop_motors)
    #     wait(3,SECONDS)
    #     stop_motors()

    #     #move_until_distance(100,'forward',40,"FRONT")
    #     Digout.set(True)


    # if caleb == 1:
    #     DigOutMatch.set(False)
    #     tube_intake_motor.spin(FORWARD,100,PERCENT)
    #     wait(2000,MSEC)
    #     tube_intake_motor.stop()
    #     drivetrain.drive_for(REVERSE, 7, INCHES)
    #     one_wheel_turn_to_heading(270, 'left',REVERSE)
    #     drivetrain.turn_to_heading(180, DEGREES, wait=True)
    #     move_until_distance(540, 'forward', 30, "FRONT")
    #     drivetrain.turn_to_heading(calibratedAngle(270),DEGREES, wait=True)
    #     move_until_distance(370,"forward",30,"FRONT")
    #     DigOutMatch.set(True)
    #     inertial_sensor.collision(intake_from_tube)
    #     drivetrain.drive_for(FORWARD,10,INCHES)
    #     controller_1.rumble("....--.-.- -. -.--- .---.---.---.- ..--.-..-..-.-..-.----.-.-.-..-.-----.-...-.-...-.-...-.--.-..-.-.-..-.-...")



    # if kuba == 1:
    # #set up to intake balls
    # #hellof

    #     #twenty_point_skills(1)
    #     tube_intake_motor.spin(REVERSE,100,PERCENT)
    #     wait (2, SECONDS)
    #     tube_intake_motor.stop()
    #     drivetrain.drive_for(REVERSE,10,INCHES)
    #     drivetrain.turn_to_heading(calibratedAngle(90))
    #     drivetrain.drive_for(FORWARD,18,INCHES)
    #     drivetrain.turn_to_heading(convert_relative_to_absolute(55))
    #     (a,d) = search_for_objects(-70)
    #     drivetrain.turn_to_heading(a)
    #     drivetrain.drive_for(FORWARD,d-30,MM)
    #     turn_to_balls()
        
    #     drivetrain.turn_to_heading(calibratedAngle(92), DEGREES, wait=True)
    #     drivetrain.drive_for(FORWARD, 23, INCHES, 25, PERCENT)
    #     #scanning corner 2
    #     drivetrain.turn_to_heading(convert_relative_to_absolute(65), DEGREES, wait=True)
    #     (a,d) = search_for_objects(-70)
    #     #going to and intake corner 2
        
    #     drivetrain.turn_to_heading(a, DEGREES, wait=True) 
    #     print("caleb is unhappy")
    #     drivetrain.drive_for(FORWARD,d-30,MM)
    #     turn_to_balls()
    
    #     basket_intake_motor.stop()
    #     first_intake.stop()
      
    #     #finding center goal
    #     drivetrain.turn_to_heading(calibratedAngle(0), DEGREES, wait=True)
    #     (a,d) = search_for_objects(-90)
    #     drivetrain.turn_to_heading(a - 7, DEGREES, wait=True)    
    #     #going to and outake center goal
    #     move_until_distance(400,'forward',50,"FRONT")
    #     outake_empty()
    #     move_until_distance(550, 'reverse', 50, "FRONT")
    #     wait(0.25, SECONDS)
    #     drivetrain.turn_to_heading(calibratedAngle(92), DEGREES, wait=True)
    #     wait(0.25, SECONDS)
    #     move_until_distance(580, 'reverse', 50, "BACK")
    #     one_wheel_turn_to_heading(355, 'left', REVERSE)
    #     park_after_bump()
        # color_sort("blue", 3)
        
        # #Going to corner 3
        # drivetrain.drive_for(REVERSE, 11, INCHES, 50, PERCENT)
        
        # first_intake.spin(FORWARD, 100, PERCENT)
        # basket_intake_motor.spin(REVERSE, 100, PERCENT)
        # drivetrain.turn_to_heading(calibratedAngle(300), DEGREES, wait=True) 
        # drivetrain.drive_for(FORWARD, 28, INCHES, 60, PERCENT)
        # #scanning corner 3
        
        # (a,d) = search_for_objects(-75)
        # #going to and intaking corner 3
        # drivetrain.turn_to_heading(a, DEGREES, wait=True)    
        # drivetrain.drive_for(FORWARD, d-30, MM, 50, PERCENT)
        # turn_to_balls()
        # #going to corner 4
        # drivetrain.turn_to_heading(180, DEGREES, wait=True)
        # drivetrain.drive_for(FORWARD, 35, INCHES, 50, PERCENT)
        # drivetrain.turn_to_heading(90, DEGREES, wait=True)
        # #going to and outake center goal
        # (a,d) = search_for_objects(-85)
        # drivetrain.turn_to_heading(a-2, DEGREES, wait=True)
        # move_until_distance(310, 'forward', 25, "FRONT")
        

        # #delivering corner 3 balls
        # drivetrain.turn_to_heading(135, DEGREES, wait=True)
        # drivetrain.drive_for(FORWARD, 12, INCHES, 50, PERCENT)
        # drivetrain.turn_to_heading(155, DEGREES, wait=True)
        # (a,d) = search_for_objects(-80)
        # drivetrain.turn_to_heading(a, DEGREES, wait=True)
        # drivetrain.drive_for(FORWARD, d, MM, 50, PERCENT)
def PID():
    return
def stop_motors_on_collision():
    controller_1.screen.clear_screen
    controller_1.screen.set_cursor(2,1)
    controller_1.screen.print("dsafasdf enzo today")
    left_motors.stop()
    right_motors.stop()
    first_intake.spin(FORWARD, 100, PERCENT)
    basket_intake_motor.spin(FORWARD,100,PERCENT)
    toprack.spin(FORWARD,100,PERCENT)
    tube_intake_motor.spin(REVERSE,100,PERCENT)


    global dont_stop_twice
    dont_stop_twice += 1
    if dont_stop_twice < 2:
        drivetrain.drive_for(REVERSE, 6, INCHES, 50, PERCENT)
        one_wheel_turn_to_heading(270,"left",REVERSE,10) #normal 355
        if distance_sensor.object_distance(MM) < 400:
            move_until_distance(425,"reverse",20,"FRONT")
            move_until_distance(425,"forward",20,"FRONT")
        else:
            move_until_distance(425,"forward",20,"FRONT")
        one_wheel_turn_to_heading(0,"left",FORWARD,20) # normal 85
        #DigOutMatch.set(True)
        drivetrain.drive_for(FORWARD, 22, INCHES, 50, PERCENT) 



def stop_all_motors():
    left_motors.stop()
    right_motors.stop()


def collision_and_park():


    
    #controller_1.rumble('...')
    left_motors.spin(FORWARD,70,PERCENT)
    right_motors.spin(FORWARD,70,PERCENT)
    controller_1.screen.clear_screen
    controller_1.screen.set_cursor(2,1)
    controller_1.screen.print("Before collision")
    inertial_sensor.collision(stop_motors_on_collision)
    controller_1.rumble('--')

    wait(10,SECONDS)
    controller_1.rumble('--')


def newauton_drive_and_alignwithtower():
    controller_1.screen.set_cursor(2,1)
    controller_1.screen.print("7777 Hello! Im controller and this code ran.")
    DigOutMatch.set(False)
    tube_intake_motor.spin(REVERSE,100,PERCENT)
    wait(2000,MSEC)
    tube_intake_motor.stop()
    tube_intake_motor.spin_to_position(-2520,DEGREES)
    drivetrain.drive_for(REVERSE, 7, INCHES)
    one_wheel_turn_to_heading(270, 'left',REVERSE,20)
    one_wheel_turn_to_heading(180, 'left', REVERSE,20)
    print(calibratedAngle)
    move_until_distance(500, 'forward', 30, "FRONT")
    drivetrain.turn_to_heading(calibratedAngle(270),DEGREES, wait=True)
    DigOutMatch.set(True)
    move_until_distance(360,"forward",30,"FRONT")

    left_motors.spin(FORWARD,55,PERCENT)
    right_motors.spin(FORWARD,55,PERCENT)
    #inertial_sensor.collision(stop_all_motors)
    wait(0.5,SECONDS)
    left_motors.stop()
    right_motors.stop()
   # drivetrain.drive_for(FORWARD,10,INCHES)
   # controller_1.rumble("....--.-.- -. -.--- .---.---.---.- ..--.-..-..-.-..-.----.-.-.-..-.-----.-...-.-...-.-...-.--.-..-.-.-..-.-...")
    #wait(20000)


def newauton_back_n_align_auton():
   
    
    # first_intake.spin(REVERSE,100,PERCENT)
    # basket_intake_motor.spin(FORWARD,100,PERCENT)
    # toprack.spin(REVERSE,100,PERCENT)
    # #left_motors.spin(FORWARD,5,PERCENT)
    # #right_motors.spin(FORWARD,5,PERCENT)
    # for i in range (1,2):
    #     wait(3,SECONDS)
    #     DigOutMatch.set(False)
    #     wait(0.5,SECONDS)
    #     DigOutMatch.set(True)

    # left_motors.stop()
    # toprack.stop()
    # right_motors.stop()
    # first_intake.stop()
    # basket_intake_motor.stop()
    #left_motors.stop()
    #right_motors.stop()
    left_motors.spin(REVERSE,20,PERCENT)
    right_motors.spin(REVERSE,20,PERCENT)
    wait (1.5,SECONDS)
    DigOutMatch.set(False)
    left_motors.stop()
    right_motors.stop()
    drivetrain.turn_to_heading(300,DEGREES)
    (a,b)=search_for_objects(-50)
    drivetrain.turn_to_heading(a,DEGREES)
    move_until_distance(120,"reverse",20,"BACK")
    
    #wait(20000)

def newauton_load_n_descore_auton():

    if True:        
        global MAX_SPEED

        first_intake.spin(FORWARD,100,PERCENT)
        basket_intake_motor.spin(FORWARD,100,PERCENT)
        toprack.spin(REVERSE,100,PERCENT)
        wait (8,SECONDS)
        first_intake.stop()
        basket_intake_motor.stop()
        toprack.stop()
        move_until_distance(180,'forward',20,"BACK")
        drivetrain.turn_to_heading(0, DEGREES)
        Digout.set(True)
        move_until_distance(170,'reverse',20,"BACK")
        drivetrain.turn_to_heading(282, DEGREES)
    
    Digout.set(True)


    back_until_yaw("left",260,60)



    controller_1.rumble("-..-.-..-.-.-")
    #wait(200000)


def newauton_extractballsfromtower():

    left_motors.spin(FORWARD, 40, PERCENT)
    right_motors.spin(FORWARD, 40, PERCENT)
    first_intake.spin(FORWARD, 100, PERCENT)
    basket_intake_motor.spin(REVERSE,100,PERCENT)
    wait(1,SECONDS)
    for i in range (1,13):
     wait(0.7,SECONDS)
     left_motors.spin(REVERSE, 40, PERCENT)
     right_motors.spin(REVERSE, 40, PERCENT)
     wait(0.2, SECONDS)
     left_motors.spin(FORWARD, 40, PERCENT)
     right_motors.spin(FORWARD, 40, PERCENT)

    wait(0.9, SECONDS)
    first_intake.stop()
    basket_intake_motor.stop()
    left_motors.stop()
    right_motors.stop()
    drivetrain.drive_for(REVERSE, 8, INCHES)
    drivetrain.turn_to_heading(290,DEGREES)
    #drivetrain.turn_to_heading(240,DEGREES)
    (a,b)=search_for_objects(-50)
    drivetrain.turn_to_heading(a,DEGREES)
   # drivetrain.turn_to_heading(a,DEGREES)

def newauton_drive_back_to_park():
    Digout.set(False)
    one_wheel_turn_to_heading(270,'left',FORWARD,10)
    move_until_distance(310,"forward",20,"FRONT")
    drivetrain.turn_to_heading(350,DEGREES,20,PERCENT)
    collision_and_park()

def on_collision_1():
    print("collided 1")

def on_collision_2():
    print("collided 2")


def newauton_mainfunc():
    #newauton_sweepballs() # notstarted
    newauton_drive_and_alignwithtower() # notstarted
    newauton_extractballsfromtower() # notstarted
    newauton_back_n_align_auton()   # inprogress
    newauton_load_n_descore_auton() # done and working
    newauton_drive_back_to_park() # notstarted    
    



    



def auton_funct():

      

      while inertial_sensor.is_calibrating():
         controller_1.screen.set_cursor(2,1)
         controller_1.screen.print("Calibrating Gyro")
         wait(100, MSEC)
      inertial_sensor.reset_rotation()
      inertial_sensor.set_heading(0, DEGREES)
      global MAX_SPEED
      if potentiometer.value() < 1250:
          vex_brain_slot = 1
          

      elif potentiometer.value() > 2250 and potentiometer.value() < 4050:
          vex_brain_slot = 2

      elif potentiometer.value() < 2250 and potentiometer.value() > 1250 :
          #skills_auton()
          #skills_auton()
          ##load_n_descore_auton()

          controller_1.screen.set_cursor(2,1)
          controller_1.screen.print("cccc333 Hello! Im controller and this code ran.")
    
          newauton_mainfunc()

          #lucas_auton
          return
      
      elif potentiometer.value() < 4100 and potentiometer.value() > 4050:
          test_function_before_going()
          return
      

          brain.screen.print("left Side Auton")
      SCALE_VALUE = 0.6
    

    

    #going toward balls
      first_intake.spin(FORWARD, 100, PERCENT)
      basket_intake_motor.spin(REVERSE, 100, PERCENT)

      drivetrain.drive_for(FORWARD,12, INCHES, 35, PERCENT )
      #drivetrain.drive_for(FORWARD,5, INCHES, 25, PERCENT )
      move_until_distance(25, "forward",20,"FRONT")
      DigOutMatch.set(True)
      drivetrain.drive_for(FORWARD,5, INCHES, 20, PERCENT )

      wait(1,SECONDS)
      first_intake.stop()
      basket_intake_motor.stop()

      if vex_brain_slot == 1:
         drivetrain.turn_to_heading(calibratedAngle(115), DEGREES, wait=True)

      else:

         drivetrain.turn_to_heading(calibratedAngle(245), DEGREES, wait=True)
     
      drivetrain.drive_for(FORWARD, 24, INCHES, 50 , PERCENT)

    #turning toward goal
      if vex_brain_slot == 1:
         turn_until_distance(400,'left',5, "BACK")

      else: 
         turn_until_distance(400,'right',5, "BACK")
     
    #moving toward goal
      first_intake.spin(FORWARD, 50, PERCENT)
      basket_intake_motor.spin(FORWARD, 100, PERCENT)
      
      toprack.spin(REVERSE, 100, PERCENT)
      if vex_brain_slot == 2:
          right_motors.spin(FORWARD, 50, PERCENT)
          wait(0.1, SECONDS)
          right_motors.stop()
      move_until_distance(100,'reverse',20,"BACK")

      if vex_brain_slot == 1:
          right_motors.spin(REVERSE, 50, PERCENT)
          wait(0.1, SECONDS)
          right_motors.stop()
          

      #drivetrain.turn_to_heading(convert_relative_to_absolute(-5), DEGREES, wait=True)



      wait(3.5, SECONDS)
      
      basket_intake_motor.stop()
      first_intake.stop()
      toprack.stop()
      drivetrain.drive_for(REVERSE, 1, INCHES, 75 , PERCENT)

def potentiometer_test():
    brain.screen.clear_screen()
    brain.screen.print("Potentiometer Test")
    while True:
        brain.screen.new_line()
        brain.screen.print("Value: " + str(potentiometer.value()))
        wait(100, MSEC)


def test_function_before_going():
    while inertial_sensor.is_calibrating():
        controller_1.screen.set_cursor(2,1)

        controller_1.screen.print("Calibrating Gyro")
        wait(100, MSEC)
    inertial_sensor.reset_rotation()
    inertial_sensor.set_heading(0, DEGREES)
    print("we are in the test function before going")
    
    
    #move_until_distance (100,'forward',30,"FRONT")
    #move_until_distance(100,'reverse',30,"BACK")
    
    
    drivetrain.drive_for(FORWARD, 5,INCHES)

    
    brain.screen.clear_screen()
    brain.screen.print("Testing Function Before Going")
    #wait(2, SECONDS)
    move_until_distance(50, REVERSE, 30, "BACK")
    drivetrain.turn_to_heading(270,DEGREES,wait=True)
    drivetrain.turn_to_heading(359,DEGREES,wait=True)
    (a,d) = search_for_objects(-90)
    drivetrain.turn_to_heading(a, DEGREES, wait=True)

    controller_1.rumble('......')
    wait(1,SECONDS)
    drivetrain.turn_to_heading(0,DEGREES,wait=True)
    drivetrain.turn_to_heading(90,DEGREES,wait=True)
    drivetrain.turn_to_heading(0,DEGREES,wait=True)
    (a,d) = search_for_objects(90)
    drivetrain.turn_to_heading(d, DEGREES, wait=True)
    
    controller_1.rumble('......')
    wait(1,SECONDS)
    drivetrain.turn_to_heading(0,DEGREES,wait=True)
    first_intake.spin(FORWARD,100,PERCENT)
    wait (1,SECONDS)
    first_intake.stop()
    first_intake.spin(REVERSE,100,PERCENT)
    wait(1,SECONDS)
    first_intake.stop()
    basket_intake_motor.spin(FORWARD,100,PERCENT)
    wait(1,SECONDS)
    basket_intake_motor.stop()
    basket_intake_motor.spin(REVERSE,100,PERCENT)
    wait(1,SECONDS)
    basket_intake_motor.stop()
    toprack.spin(REVERSE,100,PERCENT)
    wait(1,SECONDS)
    toprack.stop()
    toprack.spin(FORWARD,100,PERCENT)
    wait(1,SECONDS)
    toprack.stop()
    left_motor_a.spin(FORWARD,100,PERCENT)
    wait(1,SECONDS)
    left_motor_a.stop()
    wait(1,SECONDS)
    left_motor_a.spin(REVERSE,100,PERCENT)
    wait(1,SECONDS)
    left_motor_a.stop()
    wait(1,SECONDS)
    left_motor_b.spin(FORWARD,100,PERCENT)
    wait(1,SECONDS)
    left_motor_b.stop()
    wait(1,SECONDS)
    left_motor_b.spin(REVERSE,100,PERCENT)
    wait(1,SECONDS)
    left_motor_b.stop()
    wait(1,SECONDS)
    right_motor_a.spin(FORWARD,100,PERCENT)
    wait(1,SECONDS)
    right_motor_a.stop()
    wait(1,SECONDS)
    right_motor_a.spin(REVERSE,100,PERCENT)
    wait(1,SECONDS)
    right_motor_a.stop()
    wait(1,SECONDS)
    right_motor_b.spin(FORWARD,100,PERCENT)
    wait(1,SECONDS)
    right_motor_b.stop()
    wait(1,SECONDS)
    right_motor_b.spin(REVERSE,100,PERCENT)
    wait(1,SECONDS)
    right_motor_b.stop()


def drive_task():
    global test_function
    descorer_out = 0
    descorer_out2 = 0
    matchloader_out = 0
    descorer = 0
    descorer2 = 0
    matchloader = 0
    #hue = optical_sensor.hue()
    drive_left = 0
    drive_right = 0
    global MAX_SPEED, hopper_running, auton, controllerMode
    #brightness = optical_sensor.brightness()
    #hue = optical_sensor.hue()
    tube_intake_motor.set_position(0,DEGREES)
    brain.screen.clear_screen()
    brain.screen.print(potentiometer.value())
    global left_tube_spin
    global right_tube_spin
    print("very unique")
    while True:

        global distance
        #brain.screen.print(optical_sensor.hue())
        brain.screen.print(distance)
        distance = distance_sensor.object_distance(MM)
       
        if controllerMode == 0:
     
            if controller_1.buttonUp.pressing(): #or controller_2.buttonUp.pressing():
                left_motor_a.set_velocity(30, PERCENT)
                left_motor_b.set_velocity(30, PERCENT)
                left_motor_c.set_velocity(30, PERCENT)
                right_motor_a.set_velocity(30, PERCENT)
                right_motor_b.set_velocity(30, PERCENT)
                right_motor_c.set_velocity(30, PERCENT)
                left_motor_a.spin(FORWARD)
                left_motor_c.spin(FORWARD)
                right_motor_a.spin(FORWARD)
                left_motor_b.spin(FORWARD)
                right_motor_b.spin(FORWARD)
                right_motor_c.spin(FORWARD)

                brain.screen.print("Button Up Pressed")
            elif controller_1.buttonDown.pressing(): #or controller_2.buttonDown.pressing():
                left_motor_a.set_velocity(60, PERCENT)
                left_motor_c.set_velocity(60, PERCENT)
                left_motor_b.set_velocity(60, PERCENT)
                right_motor_a.set_velocity(60, PERCENT)
                right_motor_c.set_velocity(60, PERCENT)
                right_motor_b.set_velocity(60, PERCENT)
                left_motor_a.spin(REVERSE)
                left_motor_c.spin(REVERSE)
                right_motor_a.spin(REVERSE)
                left_motor_b.spin(REVERSE)
                right_motor_b.spin(REVERSE)
                right_motor_c.spin(REVERSE)
            else:
                # Joystick tank control (Controller 1)
                drive_left = controller_1.axis3.position()    # Left stick Y
                drive_right = controller_1.axis2.position()  # Right stick Y
                if drive_left == 0:
                    drive_left = controller_2.axis3.position()  # Left stick Y
                if drive_right == 0:
                    drive_right = controller_2.axis2.position()  # Right stick Y

                # Deadband threshold
                deadband = 15
                if abs(drive_left) < deadband:
                    drive_left = 0
                if abs(drive_right) < deadband:
                    drive_right = 0

                # Apply tank drive
                if left_motor_c.installed():
                    left_motor_a.spin(FORWARD, ramp_up(drive_left), PERCENT)
                    left_motor_b.spin(FORWARD, ramp_up(drive_left), PERCENT)
                    left_motor_c.spin(FORWARD, ramp_up(drive_left), PERCENT)
                    right_motor_a.spin(FORWARD, ramp_up(drive_right), PERCENT)
                    right_motor_b.spin(FORWARD, ramp_up(drive_right), PERCENT)
                    right_motor_c.spin(FORWARD, ramp_up(drive_right), PERCENT)
                else:
                    left_motor_a.spin(FORWARD, ramp_up(drive_left), PERCENT)
                    left_motor_b.spin(FORWARD, ramp_up(drive_left), PERCENT)
                    right_motor_a.spin(FORWARD, ramp_up(drive_right), PERCENT)
                    right_motor_b.spin(FORWARD, ramp_up(drive_right), PERCENT)


        else:
            # Arcade control mode (Controller 1)
            forward_power = controller_1.axis3.position()  # Left stick Y
            turn_power = controller_1.axis1.position()     # Left stick X
            if forward_power == 0:
                forward_power = controller_2.axis3.position()  # Left stick Y
            if turn_power == 0:
                turn_power = controller_2.axis1.position()     # Left stick X

            left_power = forward_power + turn_power
            right_power = forward_power - turn_power

            left_motor_a.set_velocity(left_power * 2, PERCENT)
            left_motor_b.set_velocity(left_power * 2, PERCENT)
            left_motor_c.set_velocity(left_power * 2, PERCENT)
            right_motor_a.set_velocity(right_power * 2, PERCENT)
            right_motor_b.set_velocity(right_power * 2, PERCENT)
            right_motor_c.set_velocity(right_power * 2, PERCENT)

            left_motor_a.spin(FORWARD)
            left_motor_b.spin(FORWARD)
            left_motor_c.spin(FORWARD)
            right_motor_a.spin(FORWARD)
            right_motor_b.spin(FORWARD)
            right_motor_c.spin(FORWARD)

     

        first_intake_control = (controller_2.buttonL1.pressing() - controller_2.buttonL2.pressing()) * 30
        basket_intake_control = (controller_2.buttonR1.pressing() - controller_2.buttonR2.pressing()) * MAX_SPEED
        toprack_control = (controller_2.buttonA.pressing() - controller_2.buttonY.pressing()) * 110





        if controller_1.buttonRight.pressing()   or controller_2.buttonRight.pressing():
            right_tube_spin = 1
            if controller_1.buttonRight.pressing() :
                tube_intake_motor_control = (controller_1.buttonRight.pressing()) * -100
            else:
                tube_intake_motor_control = (controller_2.buttonRight.pressing()) * -100
        else:
            if controller_1.buttonLeft.pressing()   or controller_2.buttonLeft.pressing():
                left_tube_spin = 1
                if controller_1.buttonLeft.pressing() :
                    tube_intake_motor_control = (controller_1.buttonLeft.pressing()) * 100
                else:
                    tube_intake_motor_control = (controller_2.buttonLeft.pressing()) * 100
            else:
                tube_intake_motor_control = 0


        if first_intake_control == 0:
            first_intake_control = (controller_1.buttonL1.pressing() - controller_1.buttonL2.pressing()) * 30
        if basket_intake_control == 0:
            basket_intake_control = (controller_1.buttonR1.pressing() - controller_1.buttonR2.pressing()) * MAX_SPEED
        if toprack_control == 0:
            toprack_control = (controller_1.buttonA.pressing() - controller_1.buttonY.pressing()) * 70

        if controller_1.buttonX.pressing():
            if descorer == 0:
                descorer = 1
                if descorer_out == 0:
                    Digout.set(True)
                    descorer_out = 1
                else:
                    Digout.set(False)
                    descorer_out = 0

        else:
            descorer = 0

            #controller_1.rumble('......')
        
  

        if controller_1.buttonB.pressing():
            if descorer2 == 0:
                descorer2 = 1
                if descorer_out2 == 0:
                    DigOutMatch.set(True)
                    descorer_out2 = 1
                else:
                    DigOutMatch.set(False)
                    descorer_out2 = 0

        else:
            descorer2 = 0
                        # if matchloader == 0:
            #     matchloader = 1
            #     if matchloader_out == 0:
            
            #         matchloader_out = 1
            #     else:
            #         DigOutMatch.set(False)
            #         matchloader_out = 0

        #else:
        #    matchloader = 0
            #Digout.set(False)
            #controller_1.rumble('-----')
            

        if right_tube_spin == 1 and tube_intake_motor_control == 0:
            controller_1.screen.clear_screen()
            controller_1.screen.set_cursor(1,1)
            controller_1.screen.print("Right Spin")
            controller_1.screen.print(tube_intake_motor.position())      
            #tube_intake_motor.spin_to_position(tube_intake_motor.position() + 360 - tube_intake_motor.position()%360)
            right_tube_spin = 0
      

        if left_tube_spin == 1 and tube_intake_motor_control == 0:

            controller_1.screen.clear_screen()
            controller_1.screen.set_cursor(1,1)
            controller_1.screen.print("Left Spin")
            controller_1.screen.print(tube_intake_motor.position())      
            #tube_intake_motor.spin_to_position(tube_intake_motor.position() - 360 - tube_intake_motor.position()%360)
            left_tube_spin = 0
            

        first_intake.spin(FORWARD, first_intake_control * 10, PERCENT)
        basket_intake_motor.spin(FORWARD, basket_intake_control * 10, PERCENT)    
        toprack.spin(REVERSE, toprack_control * 100, PERCENT)
        first_intake.spin(FORWARD, first_intake_control * 10, PERCENT)
        basket_intake_motor.spin(FORWARD, basket_intake_control * MOTOR_MULTIPLIER, PERCENT)    
        toprack.spin(REVERSE, toprack_control * 100, PERCENT)
        tube_intake_motor.spin(FORWARD, tube_intake_motor_control, PERCENT)
   

        if controller_2.buttonUp.pressing():
            first_intake.spin(REVERSE,10,PERCENT)
            basket_intake_motor.spin(FORWARD,10,PERCENT)


        # Autonomous function (X button on either controller)
        #and controller_2.buttonX.pressing()
        if bumper.pressing():
            print('Caleb1')
            global bumper_was_pressing
            if bumper_was_pressing == 0:
                bumper_was_pressing = 1
                print('Caleb2')
                auton_funct()

        if controller_2.buttonUp.pressing() or controller_1.buttonUp.pressing():
            MAX_SPEED = min(100, MAX_SPEED + 5)
            wait(100, MSEC)
            brain.screen.clear_screen()
     
        sleep(10)




#def vision_scan():

    #print("func_scan")
    controller_1.screen.print("BlahEnzo5")
    # Create a new Signature "RED_BOX" with the Colordesc class
    RED_BOX = Signature(0, 9269, 11397,10333, -1695, -523, -1109,7878448, 0)
    # Create a new Vision Sensor "vision_1" with the Vision
    # class, with the "RED_BOX" Signature.
    vision_1 = Vision(Ports.PORT17, 100, RED_BOX)
    wilenum = 0
    # Move forward if a red object is detected
    while True:
        
        controller_1.screen.set_cursor(1,1)
        controller_1.screen.clear_screen()
        wilenum += 1
        controller_1.screen.print("hia")
        red_object = vision_1.take_snapshot(RED_BOX)
        controller_1.screen.print(red_object)
        if red_object:
            #drivetrain.drive_for(FORWARD, 10, MM)
            controller_1.rumble(".....-")
        wait(5, MSEC)
def visionTask():
    while True:
        SIG_1 = Signature(0, 9269, 11397,10333, -1695, -523, -1109,7878448, 0)
        vision = Vision(Ports.PORT17, 100)
        objects = vision.take_snapshot(SIG_1)
        if objects is not None:
            for obj in objects:
                wait(50,MSEC)
                if obj.width > 120:
                    print("e8 x:" + str(obj.centerX) + " y:" + str(obj.centerY))
                






def autonomous():
    brain.screen.clear_screen()
    brain.screen.print("autonomous code")
    auton_funct()
    # place automonous code here

def user_control():
    brain.screen.clear_screen()
    brain.screen.print("driver control")
    # place driver control in this while loop
    drive_task()
def ballsucktest():
    
    while inertial_sensor.is_calibrating():
        controller_1.screen.set_cursor(2,1)

        controller_1.screen.print("Calibrating Gyro")
        wait(100, MSEC)
    inertial_sensor.reset_rotation()
    inertial_sensor.set_heading(0, DEGREES)
    ball_sucker('left',700, 0)




#dontdoit = False

def park_after_bump():

    
    #global dontdoit
    
    #if (dontdoit == False):
        right_motors.stop()
        left_motors.stop()
        wait(1, SECONDS)
        drivetrain.drive_for(FORWARD, 20, INCHES, 100, PERCENT) 
        first_intake.spin(FORWARD, 100, PERCENT)
        basket_intake_motor.spin(REVERSE, 100, PERCENT)
        tube_intake_motor.spin(REVERSE, 100, PERCENT)
        drivetrain.drive_for(FORWARD, 30, INCHES) 
        wait(5, SECONDS)
        first_intake.stop()
        basket_intake_motor.stop()
        tube_intake_motor.stop()
        # dontdoit = True
    


# def go_to_bump():
    
    
#     right_motors.spin(FORWARD, 75, PERCENT)
#     left_motors.spin(FORWARD, 75, PERCENT)
#     wait(0.5, SECONDS)
#     inertial_sensor.collision() 
    
    

#ballsucktest()
#search_for_objects(LEFT,270)
#drivetrain.turn_to_heading(smallest_distance_angle, DEGREES, wait=True)
#drivetrain.drive_for(FORWARD, smallest_distance_value-50, MM, 10, PERCENT)
##drivetrain.turn_to_heading(365, DEGREES, wait=True)
#drivetrain.drive_for(FORWARD, 60, MM, 10, PERCENT)




controller_1.screen.clear_screen()
controller_1.screen.set_cursor(2,1)
controller_1.screen.print("Running")


#test_function_before_going()


#search_for_objects(RIGHT,120)
#drivetrain.turn_to_heading(smallest_distance_angle, DEGREES, wait=True)
#color_sort("red", 6)
#go_to_bump()
while inertial_sensor.is_calibrating():
        controller_1.screen.set_cursor(2,1)

        controller_1.screen.print("Calibrating Gyro")
        wait(100, MSEC)
inertial_sensor.reset_rotation()
inertial_sensor.set_heading(0, DEGREES)

def PointWhackerArm():
    controller_1.screen.clear_screen()
    controller_1.screen.set_cursor(2,1)
    controller_1.screen.print("Point Whacker Test")
    tube_intake_motor.spin_to_position(200, DEGREES)
    wait(1, SECONDS)
    tube_intake_motor.spin_to_position(300, DEGREES)
    wait(1, SECONDS)
    tube_intake_motor.spin_to_position(10, DEGREES)
#ball_sucker('left',700, 0)
#PointWhackerArm()
drive_task()
# (a,d) = search_for_objects(-120)
# drivetrain.turn_to_heading(a, DEGREES, wait=True) 
#outake_empty()
# create competition instance
#one_wheel_turn_to_heading(180,'left',REVERSE,20)
print("i am before")
#auton_funct()
#drive_task()#twenty_point_skills(0)
print('hello my name is caleb')
#collision_and_park()
#skills_auton()
#comp = Competition(user_control, autonomous)
#turn_until_distance(100,'left',20)
#newauton_load_n_descore_auton()
