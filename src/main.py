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


#DO NOT ADD PI KUBA!!!!!!

dont_stop_twice = 0
test_function = 0

EXTREME_RIGHT = 1

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
bumper = Bumper(brain.three_wire_port.a)
potentiometer = Potentiometer(brain.three_wire_port.b) 
distance_sensor = Distance(Ports.PORT9)
distance_sensor_back = Distance(Ports.PORT2)
inertial_sensor = Inertial(Ports.PORT1)
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

brain.screen.print("Hello V5 - Movement/Intake Split Lucas here")

# Create the left Motors and group them under the MotorGroup "left_motors"
left_motor_a = Motor(Ports.PORT2, GearSetting.RATIO_18_1, False)
left_motor_b = Motor(Ports.PORT10, GearSetting.RATIO_18_1, False)

#lift motors
lift_motor_left = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)
lift_motor_right = Motor(Ports.PORT5, GearSetting.RATIO_18_1, True) 

# Create the right Motors and group them under the MotorGroup "right_motors"
right_motor_a = Motor(Ports.PORT3, GearSetting.RATIO_18_1, True)
right_motor_b = Motor(Ports.PORT9, GearSetting.RATIO_18_1, True)

left_motor_b.set_reversed(False)
left_motor_a.set_reversed(False)

right_motor_a.set_reversed(True)
right_motor_b.set_reversed(True)

lift_motor_left.set_reversed(False)
lift_motor_right.set_reversed(True)

lift_motors = MotorGroup(lift_motor_left, lift_motor_right)
right_motors = MotorGroup(right_motor_a, right_motor_b)
left_motors = MotorGroup(left_motor_a, left_motor_b)


#set_position Sets the starting position of the tube intake motor to 0 degrees so that it will not block distance sensor
drivetrain = SmartDrive(left_motors, right_motors, inertial_sensor,330, 335, 231, MM, 1)


# Intake/Mechanism motors
first_intake = Motor(Ports.PORT11, GearSetting.RATIO_18_1, True)
basket_intake_motor = Motor(Ports.PORT7, GearSetting.RATIO_18_1, False)
toprack = Motor(Ports.PORT8, GearSetting.RATIO_18_1, False)

drivetrain.set_stopping(BrakeType.BRAKE)

LEFT = 1
RIGHT = 0



def P_turn(target_heading, max_speed):
    #max_speed = 100
    current_speed = 0
    TOL = 2

    rel_target_heading = convert_absolute_to_relative(target_heading)



    #current_heading = getPatchedHeading(target_heading)
    rel_current_heading = convert_absolute_to_relative(inertial_sensor.heading())
    print("====================================================")
    print("Calebg123", rel_target_heading," ", rel_current_heading)

    
    while not(rel_current_heading > rel_target_heading - TOL and rel_current_heading < rel_target_heading + TOL):
        
        #turning wrong direction when target heading was negative and current heading was positive
        if rel_target_heading < 0 and rel_current_heading > 0:
            rel_current_heading -=360 # according to angle math adding or subtracting 360 doesn't change the angle


        if rel_target_heading > rel_current_heading +180:
            rel_current_heading += 360
        error_degrees = rel_target_heading - rel_current_heading

        # go slower if less than this
        # 
        # using max_speed because faster you go takes longer so slow down
        slowdown_cutoff = max_speed 


        # when far go fast, when close go slow
        current_speed = error_degrees * 0.5        
        if abs(error_degrees) > slowdown_cutoff:
            current_speed= error_degrees


        #max speed is max_speed.. make sure to handle negative
        if current_speed > max_speed:
            current_speed = max_speed
        else:
            if current_speed < (0 - max_speed):
                current_speed = (0 - max_speed)

        #print("rel_current_heading", rel_current_heading)
       # print("current_speed", current_speed)
       
        left_motors.spin(FORWARD, current_speed, PERCENT)
        right_motors.spin(REVERSE, current_speed, PERCENT)    
        

       
        

        rel_current_heading = convert_absolute_to_relative(inertial_sensor.heading())
        #wait(10)
    drivetrain.stop_motors()
    return


def ramp_up(input_percent):
    if (input_percent < 25):
        return input_percent * 0.25
    
    elif (input_percent < 50):
        return input_percent * 0.5
    
    
    elif (input_percent < 75):
        return input_percent * 0.75
    else:
        return input_percent
    




def jiggle_angle(goal_angle, jspeed):
    drivetrain.drive_for(FORWARD,1.5,INCHES, jspeed, PERCENT)
    drivetrain.drive_for(REVERSE,1.8,INCHES, jspeed, PERCENT)
    # P_turn(goal_angle, 40)

    
    


        


    





def find_objects_in_data(data_set):

    global final_object_angle
    
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

    return relative_angle





  
    
def search_for_objects(range_degrees,sensor="BACK"):
    print("lucas is cool3")




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




def search_for_objects_back(range_degrees):

    print("lucas is cool3")


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


def back_until_yaw(left_or_right,amount,speed):
    if left_or_right == "left":
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
        



def one_wheel_turn_to_heading(target_heading, side, direction,speed):
    

    if side == 'left':


        while not (inertial_sensor.heading() > target_heading - 7 and inertial_sensor.heading() < target_heading + 7):
            left_motors.spin(direction, speed, PERCENT)
            controller_1.screen.clear_screen()
            controller_1.screen.set_cursor(1,1)
            controller_1.screen.print(inertial_sensor.heading())

            
    if side == 'right':
        while not (inertial_sensor.heading() > target_heading - 7 and inertial_sensor.heading() < target_heading + 7):
            right_motors.spin(direction, 25, PERCENT)
    left_motors.stop()
    right_motors.stop()
    return()


def P_drive_dist(maxs, targ_dist, directionA):
    thespeed = 0
    

  

    if directionA == "forward":

        curdistance = distance_sensor.object_distance(MM)
        travel_dist = curdistance - targ_dist
        travel_steps = travel_dist / 2
        cons_acc = 0.5
      

        while (distance_sensor.object_distance(MM) > travel_steps):
            if thespeed == maxs:
                thespeed = maxs - 1
            else:
                thespeed += cons_acc
            left_motors.set_velocity(thespeed, PERCENT)
            right_motors.set_velocity(thespeed, PERCENT)
        print("1st done")


        while (distance_sensor.object_distance(MM) > 0):
            if thespeed == maxs:
                thespeed = maxs - 1
            else:
                thespeed -= cons_acc
            left_motors.set_velocity(thespeed, PERCENT)
            right_motors.set_velocity(thespeed, PERCENT)
        print("3rd done")

    if directionA == "back":
        curdistance = distance_sensor_back.object_distance(MM)
        travel_dist = curdistance - targ_dist
        travel_steps = travel_dist / 3

        # increase the speed to max
        while (distance_sensor_back.object_distance(MM) > travel_steps * 2):
            if thespeed == maxs:
                thespeed = maxs - 1
            else:
                thespeed += 1
            left_motors.set_velocity(-thespeed, PERCENT)
            right_motors.set_velocity(-thespeed, PERCENT)
        print("1st done")

        while (distance_sensor_back.object_distance(MM) > travel_steps):
            left_motors.set_velocity(-maxs, PERCENT)
            right_motors.set_velocity(-maxs, PERCENT)
        print("2nd done")

        while (distance_sensor_back.object_distance(MM) > travel_steps * 0):
            if thespeed == maxs:
                thespeed = maxs - 1
            else:
                thespeed -= 1
            left_motors.set_velocity(-thespeed, PERCENT)
            right_motors.set_velocity(-thespeed, PERCENT)
        print("3rd done")
        

    # drive some time
   
    
    left_motors.stop()
    right_motors.stop()





def P_drive_max_done(maxs, targ_dist):
    thespeed = 5
    curdistance = distance_sensor.object_distance(MM)
    myerror = curdistance - targ_dist

    

    # start motors

    left_motors.spin(FORWARD,thespeed, PERCENT)    
    right_motors.spin(FORWARD, thespeed, PERCENT)    
    # increase the speed to max
    while (thespeed < maxs):
        thespeed += 1
        left_motors.set_velocity(thespeed, PERCENT)
        right_motors.set_velocity(thespeed, PERCENT)
        wait(10)

    # drive some time
   
    curdistance = distance_sensor.object_distance(MM)
    while (thespeed > 5):
        
        myerror = curdistance - targ_dist
        if (myerror > maxs):
            myerror = maxs
        thespeed = myerror / 1.2
        left_motors.set_velocity(thespeed, PERCENT)
        right_motors.set_velocity(thespeed, PERCENT)
        wait(0.01, SECONDS)
        curdistance = distance_sensor.object_distance(MM)

    # stop motors
    left_motors.stop()
    right_motors.stop()






            
        
        
            
        

    
def turn_until_distance(distance,direction,speed, sensor_location):
    if sensor_location == "FRONT":
        while distance_sensor.object_distance(MM) > distance:
            if direction == 'left':
                    left_motors.spin(REVERSE,speed,PERCENT)
                    right_motors.spin(FORWARD,speed,PERCENT)
            elif direction == 'right':
                    left_motors.spin(FORWARD,speed,PERCENT)
                    right_motors.spin(REVERSE,speed,PERCENT)
    else:
         while distance_sensor_back.object_distance(MM) > distance:
            if direction == 'left':
                    left_motors.spin(FORWARD,speed,PERCENT)
                    right_motors.spin(REVERSE,speed,PERCENT)
            elif direction == 'right':
                    left_motors.spin(REVERSE,speed,PERCENT)
                    right_motors.spin(FORWARD,speed,PERCENT)

#lucas is the best 
    left_motors.stop()
    right_motors.stop()
    return

def move_until_distance(distance,direction,speed, sensor_location):
    sensed_once = 0
    if sensor_location == "FRONT":
        if direction == 'forward':
        
            while sensed_once < 1:
                left_motors.spin(FORWARD,speed,PERCENT)
                right_motors.spin(FORWARD,speed,PERCENT)
                if distance_sensor.object_distance() < distance:
                    sensed_once += 1
                else:
                    sensed_once = 0
        elif direction == 'reverse':
            while distance_sensor.object_distance(MM)< distance:

                left_motors.spin(REVERSE,speed,PERCENT)
                right_motors.spin(REVERSE, speed,PERCENT)

    elif sensor_location == "BACK":
        if direction == 'forward':
            while distance_sensor_back.object_distance(MM) < distance:

                left_motors.spin(FORWARD,speed,PERCENT)
                right_motors.spin(FORWARD,speed,PERCENT)
        elif direction == 'reverse':
            while distance_sensor_back.object_distance(MM) > distance:
                left_motors.spin(REVERSE,speed,PERCENT)
                right_motors.spin(REVERSE, speed,PERCENT)
    left_motors.stop()
    right_motors.stop()
    return




class PIDController:
    def __init__(self, Kp, Ki, Kd, setpoint):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.setpoint = setpoint
        self.previous_error = 0
        self.integral = 0

    def compute(self, process_variable, dt):
        # Calculate error
        error = self.setpoint - process_variable
        
        # Proportional term
        P_out = self.Kp * error
        
        # Integral term
        self.integral += error * dt
        I_out = self.Ki * self.integral
        
        # Derivative term
        derivative = (error - self.previous_error) / dt
        D_out = self.Kd * derivative
        
        # Compute total output
        output = P_out + I_out + D_out
        
        # Update previous error
        self.previous_error = error
        
        return output
    

def PID():
    return
def stop_motors_on_collision():
    controller_1.screen.clear_screen
    controller_1.screen.set_cursor(2,1)
    controller_1.screen.print("dsafasdf enzo today")
    left_motors.stop()
    right_motors.stop()
    
    controller_1.screen.set_cursor(3,1)

    global dont_stop_twice
    wait ( 1, SECONDS)
    dont_stop_twice += 1
    if dont_stop_twice < 2:
        drivetrain.drive_for(REVERSE, 10, INCHES, 50, PERCENT)
        one_wheel_turn_to_heading(270,"left",REVERSE,30) #normal 355
        print("we are done turning") 
        if distance_sensor.object_distance(DistanceUnits.MM) < 415:
            print("we are in the if statement") 
            move_until_distance(415,"reverse",20,"FRONT")
            
      
        else:
            print("we are in the else statement") 
            move_until_distance(415,"forward",20,"FRONT")
        one_wheel_turn_to_heading(0,"left",FORWARD,30) # normal 85
        print("we are done with the if statement") 
        #DigOutMatch.set(True)
    

        controller_1.screen.set_cursor(2,1)
        controller_1.screen.print("In")
        wait(5,SECONDS)
        first_intake.stop()
        basket_intake_motor.stop()
        toprack.stop()
        
        
        



def stop_all_motors():
    drivetrain.stop()
    first_intake.stop()
    basket_intake_motor.stop()
    toprack.stop()




"""
example usage of P_turn (cut and paste into your code)

when turning a full 180 from current direction and you want to control which direction
clockwise or counter clockwise try this:

P_turn(calibratedAngle(175),90) # slighly off from 180 enough so we know what direction to go
P_turn(calibratedAngle(180),90)
wait(1000)
P_turn(calibratedAngle(355),90)
P_turn(calibratedAngle(0),90)
"""








def isZero(heading):
    if (heading < 0.2 and heading > -0.2):
        return True
    else:
        return False

def getPatchedHeading(target_heading):
    current_heading = inertial_sensor.heading()
    
    if isZero(current_heading):

        # if we are turning to the left we want to make sure our heading is 360 not 0
        if (target_heading>180 and target_heading < 360):
            current_heading +=360
            print("in patched heading")
        else:
            # this handles situations where it is reading 359.9 we want have the heading be 0
            current_heading = 0.0
    return current_heading
      




def potentiometer_test():
    brain.screen.clear_screen()
    brain.screen.print("Potentiometer Test")
    while True:
        brain.screen.new_line()
        brain.screen.print("Value: " + str(potentiometer.value()))
        wait(100, MSEC)



def auton_funct():
    drivetrain.drive_for(FORWARD,10,INCHES,50,PERCENT)


def drive_task():
    controller_1.rumble('.')
    global test_function
    drive_left = 0
    drive_right = 0
    global MAX_SPEED, hopper_running, auton, controllerMode
    #brightness = optical_sensor.brightness()
    #hue = optical_sensor.hue()
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
                right_motor_a.set_velocity(30, PERCENT)
                right_motor_b.set_velocity(30, PERCENT)
                left_motor_a.spin(FORWARD)
                right_motor_a.spin(FORWARD)
                left_motor_b.spin(FORWARD)
                right_motor_b.spin(FORWARD)

                brain.screen.print("Button Up Pressed")
            elif controller_1.buttonDown.pressing(): #or controller_2.buttonDown.pressing():
                left_motor_a.set_velocity(60, PERCENT)
                left_motor_b.set_velocity(60, PERCENT)
                right_motor_a.set_velocity(60, PERCENT)
                right_motor_b.set_velocity(60, PERCENT)
                left_motor_a.spin(REVERSE)
                right_motor_a.spin(REVERSE)
                left_motor_b.spin(REVERSE)
                right_motor_b.spin(REVERSE)
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

                # Apply tank drive withGroups



                #if the left stick is postive
                if drive_left > 0:
                    #make the left wheels go fast forward
                    left_motors.spin(FORWARD, ramp_up(drive_left), PERCENT)
                else:
                    #make the left wheels go fast backwards
                    left_motors.spin(REVERSE, ramp_up(0 - drive_left), PERCENT)

                if drive_right > 0:
                    #make th right wheels go fast forward
                    right_motors.spin(FORWARD, ramp_up(drive_right), PERCENT)
                else:
                    #make the right wheels go fast backwards
                    right_motors.spin(REVERSE, ramp_up(0 - drive_right), PERCENT)


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
            right_motor_a.set_velocity(right_power * 2, PERCENT)
            right_motor_b.set_velocity(right_power * 2, PERCENT)

            left_motor_a.spin(FORWARD)
            left_motor_b.spin(FORWARD)
            right_motor_a.spin(FORWARD)
            right_motor_b.spin(FORWARD)

     

        first_intake_control = (controller_1.buttonL1.pressing()) * 100

        lift_motors.spin(FORWARD,first_intake_control,PERCENT)

        if controller_2.buttonUp.pressing():
            first_intake.spin(FORWARD,80,PERCENT)
            basket_intake_motor.spin(FORWARD,80,PERCENT)
            toprack.spin(FORWARD,40,PERCENT)


        if bumper.pressing():
            global bumper_was_pressing
            if bumper_was_pressing == 0:
                bumper_was_pressing = 1
                print('Caleb2')
                #auton_funct()

     
        sleep(10)


 


def autonomous():
    brain.screen.clear_screen()
    brain.screen.print("autonomous code")
    # place automonous code here

def user_control():
    brain.screen.clear_screen()
    brain.screen.print("driver control")
    # place driver control in this while loop
    drive_task()








controller_1.screen.clear_screen()
controller_1.screen.set_cursor(2,1)
controller_1.screen.print("Running")


while inertial_sensor.is_calibrating():
        controller_1.screen.set_cursor(2,1)

        controller_1.screen.print("Calibrating Gyro")
        wait(100, MSEC)
inertial_sensor.reset_rotation()
inertial_sensor.set_heading(0, DEGREES)

global keeprunning
keeprunning = True
def temp_detect():
    dark_red = Color(139, 0, 0)

    print("detecting temp")
    while True:
        if Motor.temperature(right_motor_b) > 50 or Motor.temperature(left_motor_b) > 50 or Motor.temperature(left_motor_a) > 50 or Motor.temperature(right_motor_a) > 50:
            while True:

                brain.screen.clear_screen(Color.ORANGE)
                brain.screen.set_pen_color(Color.GREEN)
        elif Motor.temperature(right_motor_b) > 55 or Motor.temperature(left_motor_b) > 55 or Motor.temperature(left_motor_a) > 55 or Motor.temperature(right_motor_a) > 55:
            brain.screen.clear_screen(Color.RED)
            brain.screen.set_pen_color(Color.GREEN)
        elif Motor.temperature(right_motor_b) > 60 or Motor.temperature(left_motor_b) > 60 or Motor.temperature(left_motor_a) > 60 or Motor.temperature(right_motor_a) > 60:
            brain.screen.set_fill_color(Color(139, 0, 0))
            brain.screen.draw_rectangle(0, 0, 480, 240)

Thread(temp_detect)
#comp = Competition(drive_task())
auton_funct()
drive_task()
