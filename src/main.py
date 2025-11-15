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

from math import atan, degrees, sin, radians, cos
test_function = 0

brain = Brain()
gyro_360 = 354

def calibratedAngle(idealAngle):
    return (idealAngle * gyro_360/360)
        
distance = 0

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
inertial_sensor = Inertial(Ports.PORT1)
optical_sensor = Optical(Ports.PORT2)
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
if left_motor_c.installed():
    right_motors = MotorGroup(right_motor_a, right_motor_b, right_motor_c)
    left_motors = MotorGroup(left_motor_a, left_motor_b, left_motor_c)

else:
    right_motors = MotorGroup(right_motor_a, right_motor_b)
    left_motors = MotorGroup(left_motor_a, left_motor_b)
#FORWARD = REVERSE
#REVERSE = FORWARD
tube_intake_motor = Motor(Ports.PORT3, GearSetting.RATIO_18_1, True)

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

def fix_angle_left(range):
    final_angle = range
    if range <180:
        final_angle = range +360

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



def search_for_objects(direction,range_degrees):
    #global smallest_distance_value
    #global smallest_distance_angle
    global final_object_angle
    print("lucas is cool3")
    #controller_1.rumble('......')
    # while inertial_sensor.is_calibrating():
    #     controller_1.screen.set_cursor(2,1)

    #     controller_1.screen.print("Calibrating Gyro")
    #     wait(100, MSEC)
    #inertial_sensor.reset_rotation()
    range_degrees = convert_relative_to_absolute(range_degrees)
    print("enzo" + str(range_degrees))
    controller_1.screen.clear_screen()
    print("we finished calibrating")
    distance_data = []
    if direction == LEFT:
        print("in the left" + str(inertial_sensor.heading()) + " " + str(range_degrees))
        #inertial_sensor.set_heading(359, DEGREES)  
        print (range_degrees)
        print(inertial_sensor.heading())
        while range_degrees < fix_angle_left(inertial_sensor.heading()):
            print("im in while loop" + "  " +str(inertial_sensor.heading()) + "  " + str(distance_sensor.object_distance(MM))) 
            distance_data.append((inertial_sensor.heading(), distance_sensor.object_distance(MM)))

            left_motors.spin(REVERSE,5,PERCENT)
            right_motors.spin(FORWARD,5,PERCENT)
            wait (100,MSEC)

        print("finished moving motors")    

        right_motors.stop()
        left_motors.stop()
    else:
        print("in the right" + str(inertial_sensor.heading()) + " " + str(range_degrees))
        #inertial_sensor.set_heading(359, DEGREES)        
        while range_degrees > fix_angle_left(inertial_sensor.heading()):
            print("im in while loop" + "  " +str(inertial_sensor.heading()) + "  " + str(distance_sensor.object_distance(MM))) 
            distance_data.append((inertial_sensor.heading(), distance_sensor.object_distance(MM)))

            left_motors.spin(FORWARD,5,PERCENT)
            right_motors.spin(REVERSE,5,PERCENT)
            wait (100,MSEC)

        print("finished moving motors")    

        right_motors.stop()
        left_motors.stop()

    print("done gathering data")
    smallest_distance = 100000
    smallest_distance_angle = 0
    find_objects_in_data(distance_data)
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
        


def one_wheel_turn_to_heading(target_heading, side, direction):
    
    #drivetrain.drive_for(REVERSE,12, INCHES, 50, PERCENT )
    if side == 'left':
        # while angle is not in the target range
        # not ( angle < target + 10 and angle > target - 10 )
        # left
        while not (inertial_sensor.heading() > target_heading - 5 and inertial_sensor.heading() < target_heading + 5):
            left_motors.spin(direction, 25, PERCENT)
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
    
def turn_until_distance(distance,direction,speed):
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

    left_motors.stop()
    right_motors.stop()
    return

def move_until_distance(distance,direction,speed):
    while distance_sensor.object_distance(MM) > distance:
        if direction == 'forward':
            if left_motor_c.installed(): 
                left_motors.spin(REVERSE,speed,PERCENT)
                right_motors.spin(REVERSE,speed,PERCENT)
            else: 
                left_motors.spin(FORWARD,speed,PERCENT)
                right_motors.spin(FORWARD,speed,PERCENT)
        elif direction == 'reverse':
            if left_motor_c.installed():
                left_motors.spin(FORWARD,speed,PERCENT)
                right_motors.spin(FORWARD,speed,PERCENT)
            else: 
                left_motors.spin(REVERSE,speed,PERCENT)
                right_motors.spin(REVERSE,speed,PERCENT)

    left_motors.stop()
    right_motors.stop()
    return


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
    one_wheel_turn_to_heading(ideal_pickup_angle, 'left', REVERSE)
    collect_balls()



def skills_auton():
    global MAX_SPEED
    vex_brain_slot = 1
    kuba = 1
    
    
   
    controller_1.screen.set_cursor(2,1)

    controller_1.rumble("....--.-.- -. -.--- .---.---.---.- ..--.-..")
    wait(100, MSEC)  

    
    #set up to intake balls
    drivetrain.drive_for(FORWARD,23, INCHES, 50, PERCENT)
    drivetrain.turn_to_heading(calibratedAngle(32), DEGREES, wait=True)
    collect_balls()
    #tube_intake_motor.stop()
    drivetrain.turn_to_heading(calibratedAngle(10), DEGREES, wait=True)
    drivetrain.drive_for(FORWARD, 25, INCHES, 25, PERCENT)
    #scanning corner 2
    drivetrain.turn_to_heading(calibratedAngle(45), DEGREES, wait=True)
    (a,d) = search_for_objects(LEFT,-80)
    #going to and intake corner 2
    
    drivetrain.turn_to_heading(a, DEGREES, wait=True) 
    print("caleb is unhappy")




    drivetrain.drive_for(FORWARD, d-35, MM, 25, PERCENT)

    turn_to_balls()
     



    
    basket_intake_motor.stop()
    first_intake.stop()
    drivetrain.drive_for(REVERSE, 10, INCHES, 40, PERCENT)
    #finding center goal
    controller_1.screen.clear_screen()
    controller_1.screen.set_cursor(2,1)
    controller_1.screen.print(inertial_sensor.heading(DEGREES))
    drivetrain.turn_to_heading(calibratedAngle(275), DEGREES, wait=True)
    (a,d) = search_for_objects(LEFT,-80)
    drivetrain.turn_to_heading(a-2, DEGREES, wait=True)    
    #going to and outake center goal
    move_until_distance(310,'forward',20)
    first_intake.spin(FORWARD, 100, PERCENT)
    basket_intake_motor.spin(FORWARD, 100, PERCENT)
    toprack.spin(FORWARD, 20, PERCENT)
    wait(7,SECONDS)
    toprack.stop()
    basket_intake_motor.stop()
    first_intake.stop()
    #Going to corner 3
    drivetrain.drive_for(REVERSE, 11, INCHES, 50, PERCENT)
    
    first_intake.spin(FORWARD, 100, PERCENT)
    basket_intake_motor.spin(REVERSE, 100, PERCENT)
    drivetrain.turn_to_heading(calibratedAngle(300), DEGREES, wait=True) 
    drivetrain.drive_for(FORWARD, 28, INCHES, 60, PERCENT)
    #scanning corner 3
    
    (a,d) = search_for_objects(LEFT,-50)
    #going to and intaking corner 3
    drivetrain.turn_to_heading(a, DEGREES, wait=True)    
    drivetrain.drive_for(FORWARD, d-35, MM, 50, PERCENT)
    turn_to_balls()
    return
    #going to corner 4
    drivetrain.turn_to_heading(calibratedAngle(180), DEGREES, wait=True)
    drivetrain.drive_for(FORWARD, 20, INCHES, 50, PERCENT)
    #scanning corner 4
    drivetrain.turn_to_heading(calibratedAngle(200), DEGREES, wait=True)
    search_for_objects(LEFT,240)
    #going to and intake corner 4
    drivetrain.turn_to_heading(smallest_distance_angle, DEGREES, wait=True)    
    drivetrain.drive_for(FORWARD, smallest_distance_value-35, MM, 50, PERCENT)
    turn_to_balls()
    return

#pick up balls
    #wait(2,SECONDS)
   

#reset tube intake motor position   
    tube_intake_motor.spin_to_position(tube_intake_motor.position() + 360 - tube_intake_motor.position()%360)
    if kuba == 2:


    
        drivetrain.drive_for(REVERSE, 6, INCHES, 10, PERCENT)
        drivetrain.turn_to_heading(calibratedAngle(190), DEGREES, wait=True)
        drivetrain.drive_for(REVERSE, 10, INCHES, 10, PERCENT)

   
    else:


#set up to outtake balls
        drivetrain.turn_to_heading(calibratedAngle(-54), DEGREES, wait=True)
        drivetrain.drive_for(FORWARD, 17, INCHES, 35 , PERCENT)


#outtake balls
        first_intake.spin(REVERSE, 100, PERCENT)


        for i in range(11):
            basket_intake_motor.spin(FORWARD, 100, PERCENT)
            wait(0.5,SECONDS)
            basket_intake_motor.stop()
            wait(0.5,SECONDS)
    
   

#push balls into tube further
        drivetrain.drive_for(FORWARD, 1.5, INCHES, 10 , PERCENT)
        wait (1,SECONDS)
        first_intake.stop()
        basket_intake_motor.stop()


#set up to park
        drivetrain.drive_for(REVERSE, 7, INCHES, 35 , PERCENT)

#start intake backwards to ensure that the balls move out of parking
        first_intake.spin(REVERSE, 100, PERCENT)
        #basket_intake_motor.spin(REVERSE, 100, PERCENT)
    

#continue setting up to park    
        drivetrain.turn_to_heading(calibratedAngle(-45), DEGREES, wait=True)
        wait(0.25, SECONDS)
        drivetrain.drive_for(REVERSE, 2, INCHES, 50 , PERCENT)
        wait(0.25, SECONDS)
        drivetrain.turn_to_heading(calibratedAngle(0), DEGREES, wait=True)
        wait(0.25, SECONDS)
        move_until_distance(360,'reverse',20)
        wait(0.25, SECONDS)
        one_wheel_turn_to_heading(calibratedAngle(266), 'left', REVERSE)


#park robot
        drivetrain.drive_for(FORWARD, 35, INCHES, 100 , PERCENT)
        wait(1, SECONDS)
        drivetrain.drive_for(REVERSE, 12, INCHES, 50 , PERCENT)
        drivetrain.drive_for(FORWARD, 40, INCHES, 100 , PERCENT)
        
        first_intake.stop()
        basket_intake_motor.stop()
#     


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
          brain.screen.print("right Side Auton")

      elif potentiometer.value() > 2250 and potentiometer.value() < 4050:
          vex_brain_slot = 2

      elif potentiometer.value() < 2250 and potentiometer.value() > 1250 :
          skills_auton()
          return
      
      elif potentiometer.value() < 4100 and potentiometer.value() > 4050:
          test_function_before_going()
          return
      

          brain.screen.print("left Side Auton")
      SCALE_VALUE = 0.6
    

    


      drivetrain.drive_for(FORWARD,12, INCHES, 50, PERCENT )
      #drivetrain.turn_to_heading(calibratedAngle(35), DEGREES, wait=True)
      first_intake.spin(FORWARD, 100, PERCENT)
      basket_intake_motor.spin(REVERSE, 100, PERCENT)
      drivetrain.drive_for(FORWARD, 9, INCHES, 10, PERCENT)


     
      wait(0.5,SECONDS)
      first_intake.stop()
      basket_intake_motor.stop()

      if vex_brain_slot == 1:
         drivetrain.turn_to_heading(calibratedAngle(115), DEGREES, wait=True)

      else:

         drivetrain.turn_to_heading(calibratedAngle(245), DEGREES, wait=True)
     
      drivetrain.drive_for(FORWARD, 32, INCHES, 35 , PERCENT)

      if vex_brain_slot == 1:
         turn_until_distance(750,'left',5)

      else: 
         turn_until_distance(750,'right',5)

     

      first_intake.spin(FORWARD, 50, PERCENT)
      basket_intake_motor.spin(FORWARD, 100, PERCENT)
      brain.screen.print("we made it")
      toprack.spin(REVERSE, 100, PERCENT)
      move_until_distance(150,'reverse',20)
      drivetrain.turn_for(LEFT, 8,DEGREES,5,PERCENT)



      wait(3, SECONDS)
      brain.screen.print("we made it 2")
      basket_intake_motor.stop()
      first_intake.stop()
      toprack.stop()
      drivetrain.drive_for(REVERSE, 2, INCHES, 75 , PERCENT)

def potentiometer_test():
    brain.screen.clear_screen()
    brain.screen.print("Potentiometer Test")
    while True:
        brain.screen.new_line()
        brain.screen.print("Value: " + str(potentiometer.value()))
        wait(100, MSEC)


def test_function_before_going():
    print("we are in the test function before going")
    
    brain.screen.clear_screen()
    brain.screen.print("Testing Function Before Going")
    #wait(2, SECONDS)
    drivetrain.turn_to_heading(270,DEGREES,wait=True)
    drivetrain.turn_to_heading(359,DEGREES,wait=True)
    (a,d) = search_for_objects(LEFT,-90)
    drivetrain.turn_to_heading(a, DEGREES, wait=True)

    controller_1.rumble('......')
    wait(1,SECONDS)
    drivetrain.turn_to_heading(0,DEGREES,wait=True)
    drivetrain.turn_to_heading(90,DEGREES,wait=True)
    drivetrain.turn_to_heading(0,DEGREES,wait=True)
    (a,d) = search_for_objects(RIGHT,90)
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
    optical_sensor.set_light_power(25, PERCENT)
    brightness = optical_sensor.brightness()
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
                    left_motor_a.spin(FORWARD, drive_left * 100, PERCENT)
                    left_motor_b.spin(FORWARD, drive_left * 100, PERCENT)
                    left_motor_c.spin(FORWARD, drive_left * 100, PERCENT)
                    right_motor_a.spin(FORWARD, drive_right * 100, PERCENT)
                    right_motor_b.spin(FORWARD, drive_right * 100, PERCENT)
                    right_motor_c.spin(FORWARD, drive_right * 100, PERCENT)
                else:
                    left_motor_a.spin(FORWARD, drive_left * 1, PERCENT)
                    left_motor_b.spin(FORWARD, drive_left * 1, PERCENT)
                    right_motor_a.spin(FORWARD, drive_right * 1, PERCENT)
                    right_motor_b.spin(FORWARD, drive_right * 1, PERCENT)


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
            global bumper_was_pressing
            if bumper_was_pressing == 0:
                bumper_was_pressing = 1
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

#ballsucktest()
#search_for_objects(LEFT,270)
#drivetrain.turn_to_heading(smallest_distance_angle, DEGREES, wait=True)
#drivetrain.drive_for(FORWARD, smallest_distance_value-50, MM, 10, PERCENT)
##drivetrain.turn_to_heading(365, DEGREES, wait=True)
#drivetrain.drive_for(FORWARD, 60, MM, 10, PERCENT)




controller_1.screen.clear_screen()
controller_1.screen.set_cursor(2,1)
controller_1.screen.print("BlahEnzo12")



#search_for_objects(RIGHT,120)
#drivetrain.turn_to_heading(smallest_distance_angle, DEGREES, wait=True)

drive_task()
# create competition instance
#comp = Competition(user_control, autonomous)
#turn_until_distance(100,'left',20)

#This code is Enzo's testing of the vision sensor
#visionTask()

#test_funct()