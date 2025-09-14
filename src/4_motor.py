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

brain = Brain()

        
distance = 0


# actions to do when the program starts
brain.screen.clear_screen()

# Brain and Controllers



# Configure the optical sensor on a specific port (change port number as needed)
distance_sensor = Distance(Ports.PORT10)
optical_sensor = Optical(Ports.PORT2)
controller_1 = Controller(ControllerType.PRIMARY)    # MOVEMENT CONTROLLER
controller_2 = Controller(ControllerType.PARTNER)    # INTAKE CONTROLLER

# Global variables
MAX_SPEED = 40
MOTOR_MULTIPLIER = 10  # Multiplier for motor control speeds
controllerMode = 0
auton = 0
hopper_running = 0
b_was_pressed = 0
vex_brain_slot = 1 # 1 = left, 2 = right Auton

brain.screen.print("Hello V10 - Movement/Intake Split")
brain.screen.new_line()

# Create the left Motors and group them under the MotorGroup "left_motors"
left_motor_a = Motor(Ports.PORT19, GearSetting.RATIO_18_1, False)
left_motor_b = Motor(Ports.PORT12, GearSetting.RATIO_18_1, False)
left_motors = MotorGroup(left_motor_a, left_motor_b)

# Create the right Motors and group them under the MotorGroup "right_motors"
right_motor_a = Motor(Ports.PORT14, GearSetting.RATIO_18_1, True)
right_motor_b = Motor(Ports.PORT16, GearSetting.RATIO_18_1, True)
right_motors = MotorGroup(right_motor_a, right_motor_b)

# Construct a 4-Motor Drivetrain
# Parameters: circumference, distance between wheels on axle, distance between axles, units, gear ratio
drivetrain = DriveTrain(left_motors, right_motors, 330, 335, 231, MM, 1)

# Intake/Mechanism motors
first_intake = Motor(Ports.PORT11, GearSetting.RATIO_18_1, False)
basket_intake_motor = Motor(Ports.PORT9, GearSetting.RATIO_18_1, False)
toprack = Motor(Ports.PORT17, GearSetting.RATIO_18_1, False)

def hopper_pickup():
    SCALE_VALUE = 0.6
    global MAX_SPEED
    
    drivetrain.turn_for(RIGHT, 20 * SCALE_VALUE, DEGREES, 25, PERCENT)
    drivetrain.turn_for(LEFT, 20 * SCALE_VALUE, DEGREES, 25, PERCENT)
    drivetrain.drive_for(FORWARD, 10, MM, 50, PERCENT)

def turn_until_distance(target_distance_1, target_distance_2, direction):
    return
    global MAX_SPEED
    global distance
    left_motor_a.set_velocity(MAX_SPEED / 2, PERCENT)
    left_motor_b.set_velocity(MAX_SPEED / 2, PERCENT)
    right_motor_a.set_velocity(MAX_SPEED / 2, PERCENT)
    right_motor_b.set_velocity(MAX_SPEED / 2, PERCENT)
    while True:
        if direction == 'left':

            if distance >= target_distance_1 and distance <= target_distance_2:
                break
            else:
                left_motor_a.spin(FORWARD)
                right_motor_a.spin(REVERSE)
                left_motor_b.spin(FORWARD)
                right_motor_b.spin(REVERSE)

        elif direction == 'right':

            if distance >= target_distance_1 and distance <= target_distance_2:
                break
            else:
                left_motor_a.spin(REVERSE)
                right_motor_a.spin(FORWARD)
                left_motor_b.spin(REVERSE)
                right_motor_b.spin(FORWARD)       
      
    left_motor_a.stop()
    left_motor_b.stop()
    right_motor_a.stop()
    right_motor_b.stop()

def test_funct():
    turn_until_distance(1, 70, 'right')

def auton_funct():
    global MAX_SPEED
    
    SCALE_VALUE = 0.6
    
    if vex_brain_slot == 2:  # right side auton
        first_intake.spin(FORWARD, 100, PERCENT)
        basket_intake_motor.spin(REVERSE, 100, PERCENT)
        drivetrain.drive_for(FORWARD, 450, MM, 50, PERCENT)
        drivetrain.turn_for(RIGHT, 30 * SCALE_VALUE, DEGREES, 25, PERCENT)
        drivetrain.drive_for(FORWARD, 300, MM, 25, PERCENT)
        drivetrain.turn_for(LEFT, 25 * SCALE_VALUE, DEGREES, 25, PERCENT)
        drivetrain.drive_for(FORWARD, 550, MM, 20, PERCENT)
        wait(1, SECONDS)
        basket_intake_motor.stop()
        first_intake.stop()
        drivetrain.drive_for(REVERSE, 620, MM, 50, PERCENT)
        drivetrain.turn_for(RIGHT, 105 * SCALE_VALUE, DEGREES, 25, PERCENT)
        drivetrain.drive_for(FORWARD, 685, MM, 75, PERCENT)
        #where it turns to look at the goal
        #drivetrain.turn_for(RIGHT, 100 * SCALE_VALUE, DEGREES, 25, PERCENT)
        turn_until_distance(1, 70, 'right')

        drivetrain.drive_for(REVERSE, 200, MM, 50, PERCENT)
        first_intake.spin(FORWARD, 50, PERCENT)
        basket_intake_motor.spin(FORWARD, 100, PERCENT)
        brain.screen.print("we made it")
        toprack.spin(REVERSE, 100, PERCENT)
        wait(5, SECONDS)
        brain.screen.print("we made it 2")
        basket_intake_motor.stop()
        first_intake.stop()
        toprack.stop()
        brain.screen.print("we made it3")

    elif vex_brain_slot == 1:  # left side auton
        first_intake.spin(FORWARD, 100, PERCENT)
        basket_intake_motor.spin(REVERSE, 100, PERCENT)
        drivetrain.drive_for(FORWARD, 450, MM, 50, PERCENT)
        drivetrain.turn_for(LEFT, 30 * SCALE_VALUE, DEGREES, 25, PERCENT)
        drivetrain.drive_for(FORWARD, 300, MM, 25, PERCENT)
        drivetrain.turn_for(RIGHT, 25 * SCALE_VALUE, DEGREES, 25, PERCENT)
        drivetrain.drive_for(FORWARD, 550, MM, 20, PERCENT)
        wait(1, SECONDS)
        basket_intake_motor.stop()
        first_intake.stop()
        drivetrain.drive_for(REVERSE, 620, MM, 50, PERCENT)
        drivetrain.turn_for(LEFT, 105 * SCALE_VALUE, DEGREES, 25, PERCENT)
        drivetrain.drive_for(FORWARD, 685, MM, 75, PERCENT)
        #where it turns to look at the goal
        #drivetrain.turn_for(LEFT, 100 * SCALE_VALUE, DEGREES, 25, PERCENT)
        turn_until_distance(1, 70, 'left')

        drivetrain.drive_for(REVERSE, 200, MM, 50, PERCENT)
        first_intake.spin(FORWARD, 50, PERCENT)
        basket_intake_motor.spin(FORWARD, 100, PERCENT)
        brain.screen.print("we made it")
        toprack.spin(REVERSE, 100, PERCENT)
        wait(5, SECONDS)
        brain.screen.print("we made it 2")
        basket_intake_motor.stop()
        first_intake.stop()
        toprack.stop()
        brain.screen.print("we made it3")





def drive_task_2():
    #optical_sensor.set_light_power(25, PERCENT)
    brightness = optical_sensor.brightness()
    hue = optical_sensor.hue()
    drive_left = 0
    drive_right = 0
    global MAX_SPEED, hopper_running, auton, controllerMode
    brightness = optical_sensor.brightness()
    hue = optical_sensor.hue()
    
    while True:
        brain.screen.print("Lucas")
        if distance_sensor.object_distance(MM) < 100:
            #brain.screen.clear_screen()
            brain.screen.clear_screen()
            left_motor_a.stop()
        else:
            #brain.screen.clear_screen()
            left_motor_a.spin(FORWARD, 20, PERCENT)
            brain.screen.print("Hello")
            brain.screen.new_line()


def drive_task():
    #optical_sensor.set_light_power(25, PERCENT)
    brightness = optical_sensor.brightness()
    hue = optical_sensor.hue()
    drive_left = 0
    drive_right = 0
    global MAX_SPEED, hopper_running, auton, controllerMode
    brightness = optical_sensor.brightness()
    hue = optical_sensor.hue()
    
    while True:
        brain.screen.print("Lucas")
        if distance_sensor.object_distance(MM) < 100:
            #brain.screen.clear_screen()
            brain.screen.clear_screen()
            left_motor_a.stop()
        else:
            #brain.screen.clear_screen()
            left_motor_a.spin(FORWARD, 20, PERCENT)
            brain.screen.print("Hello")
            brain.screen.new_line()

    


        #brain.screen.print(distance)
        #distance = distance_sensor.object_distance(MM)
       
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

                # Apply tank drive
                left_motor_a.spin(FORWARD, drive_left * 0.7, PERCENT)
                left_motor_b.spin(FORWARD, drive_left * 0.7, PERCENT)
                right_motor_a.spin(FORWARD, drive_right * 0.7, PERCENT)
                right_motor_b.spin(FORWARD, drive_right * 0.7, PERCENT)
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
            
            left_motor_a.set_velocity(left_power * 0.7, PERCENT)
            left_motor_b.set_velocity(left_power * 0.7, PERCENT)
            right_motor_a.set_velocity(right_power * 0.7, PERCENT)
            right_motor_b.set_velocity(right_power * 0.7,PERCENT)

            left_motor_a.spin(FORWARD)
            left_motor_b.spin(FORWARD)
            right_motor_a.spin(FORWARD)
            right_motor_b.spin(FORWARD)

        #brain.screen.clear_screen()



        first_intake_control = (controller_2.buttonL1.pressing() - controller_2.buttonL2.pressing()) * 30
        basket_intake_control = (controller_2.buttonR1.pressing() - controller_2.buttonR2.pressing()) * MAX_SPEED
        toprack_control = (controller_2.buttonA.pressing() - controller_2.buttonY.pressing()) * 110

        if first_intake_control == 0:
            first_intake_control = (controller_1.buttonL1.pressing() - controller_1.buttonL2.pressing()) * 30
        if basket_intake_control == 0:
            basket_intake_control = (controller_1.buttonR1.pressing() - controller_1.buttonR2.pressing()) * MAX_SPEED
        if toprack_control == 0:
            toprack_control = (controller_1.buttonA.pressing() - controller_1.buttonY.pressing()) * 70

        first_intake.spin(FORWARD, first_intake_control * 8, PERCENT)
        basket_intake_motor.spin(FORWARD, basket_intake_control * 10, PERCENT)    
        toprack.spin(REVERSE, toprack_control * 50, PERCENT)
        first_intake.spin(FORWARD, first_intake_control * 8, PERCENT)
        basket_intake_motor.spin(FORWARD, basket_intake_control * MOTOR_MULTIPLIER, PERCENT)    
        toprack.spin(REVERSE, toprack_control * 50, PERCENT)
       

        if controller_1.buttonLeft.pressing() or controller_2.buttonLeft.pressing():
            brain.screen.clear_screen()
            controllerMode = 0  
            brain.screen.print("Tank Drive Mode")
            wait(200, MSEC)  
        elif controller_1.buttonRight.pressing() or controller_2.buttonRight.pressing():
            brain.screen.clear_screen()
            controllerMode = 1  # Arcade mode
            brain.screen.print("Arcade Drive Mode")
            wait(200, MSEC)  

        if controller_2.buttonUp.pressing():
            first_intake.spin(REVERSE,10,PERCENT)
            basket_intake_motor.spin(FORWARD,10,PERCENT)


        # Autonomous function (X button on either controller)
        #and controller_2.buttonX.pressing()
        if controller_1.buttonX.pressing():
            brain.screen.clear_screen()
            auton = 1

        if auton == 1:
            auton_funct()
            auton = 0

        # Hopper pickup function (B button on either controller)
        if controller_1.buttonB.pressing() or controller_2.buttonB.pressing():
            brain.screen.clear_screen()
            hopper_running = 1
        
        if hopper_running == 1:
            hopper_pickup()
            hopper_running = 0
        #change new_line to new_row
        # Speed adjustment (Up/Down arrows on Controller 2 for intake speed)
        if controller_2.buttonUp.pressing() or controller_1.buttonUp.pressing():
            MAX_SPEED = min(100, MAX_SPEED + 5)
            wait(100, MSEC)
            brain.screen.clear_screen()
        if controller_2.buttonDown.pressing():
            MAX_SPEED = max(10, MAX_SPEED - 5)
            wait(100, MSEC)
    
            if optical_sensor.is_near_object():
                brain.screen.next_row()
                brain.screen.clear_screen()
                brain.screen.print("Object Detected")
                optical_sensor.set_light_power(100, PERCENT)
                brightness = optical_sensor.brightness()
                hue = optical_sensor.hue()
                #brain.screen.clear_screen()
                if brightness > 10:
                    brain.screen.next_row()
                    brain.screen.print("Brightness > ten: " + str(brightness))
                    if (hue <= 20) or (hue >= 340):

                        
                        toprack.spin(REVERSE, 1000, PERCENT)
                        wait(0.5, SECONDS)
                        toprack.stop()

                    elif (hue >= 210) and (hue <= 230):

                        brain.screen.next_row()
                        brain.screen.print("Blue Detected")
                        

                    else:
                        brain.screen.next_row()
                        brain.screen.print("No Color Detected")
                else:
                    brain.screen.next_row()
                    brain.screen.print("Brightness less than ten " + str(brightness))

            #else:
             #   brain.screen.next_row()
              #  brain.screen.print("No Object Detected")

       # brain.screen.new_line()ain.screen.print("Brightness less than ten")

        sleep(10)
   
   
   
   
       # brain.screen.new_line()  # Removed typo and malformed code


        brain.screen.print("Lucas")
        if distance_sensor.object_distance(MM) < 100:
            #brain.screen.clear_screen()
            brain.screen.new_line()

            brain.screen.print("Distance: " + str(distance_sensor.object_distance(MM)) + " mm")
        else:
            #brain.screen.clear_screen()
            brain.screen.print("Hello")
            brain.screen.new_line()


brain.screen.print("Hello little function - Movement/Intake Split")
brain.screen.new_line()
drive_task_2()
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
        
#drive_task()
# create competition instance
comp = Competition(user_control, autonomous)


test_funct()
