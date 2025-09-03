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

from vex import *

# Brain and Controllers
brain = Brain()


# Configure the optical sensor on a specific port (change port number as needed)
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

brain.screen.print("Hello V5 - Movement/Intake Split")

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
basket_intake_motor = Motor(Ports.PORT15, GearSetting.RATIO_18_1, False)
toprack = Motor(Ports.PORT17, GearSetting.RATIO_18_1, False)

def hopper_pickup():
    SCALE_VALUE = 0.6
    global MAX_SPEED
    
    drivetrain.turn_for(RIGHT, 20 * SCALE_VALUE, DEGREES, 25, PERCENT)
    drivetrain.turn_for(LEFT, 20 * SCALE_VALUE, DEGREES, 25, PERCENT)
    drivetrain.drive_for(FORWARD, 10, MM, 50, PERCENT)

def auton_funct():
    global MAX_SPEED
    
    SCALE_VALUE = 0.6
    
    # Start of 15 second auton section
    first_intake.spin(FORWARD, 75, PERCENT)
    basket_intake_motor.spin(REVERSE, 100, PERCENT)
    drivetrain.drive_for(FORWARD, 450, MM, 25, PERCENT)
    drivetrain.turn_for(RIGHT, 30 * SCALE_VALUE, DEGREES, 25, PERCENT)
    drivetrain.drive_for(FORWARD, 300, MM, 25, PERCENT)
    drivetrain.turn_for(LEFT, 30 * SCALE_VALUE, DEGREES, 25, PERCENT)
    drivetrain.drive_for(FORWARD, 550, MM, 20, PERCENT)
    wait(2, SECONDS)
    basket_intake_motor.stop()
    first_intake.stop()
    drivetrain.drive_for(REVERSE, 620, MM, 25, PERCENT)
    drivetrain.turn_for(RIGHT, 90 * SCALE_VALUE, DEGREES, 25, PERCENT)
    drivetrain.drive_for(FORWARD, 700, MM, 25, PERCENT)
    drivetrain.turn_for(RIGHT, 95 * SCALE_VALUE, DEGREES, 25, PERCENT)
    drivetrain.drive_for(REVERSE, 90, MM, 25, PERCENT)
    first_intake.spin(FORWARD, 75, PERCENT)
    basket_intake_motor.spin(FORWARD, 100, PERCENT)
    brain.screen.print("we made it")
    toprack.spin(REVERSE, 100, PERCENT)
    wait(10, SECONDS)
    brain.screen.print("we made it 2")
    basket_intake_motor.stop()
    first_intake.stop()
    toprack.stop()
    brain.screen.print("we made it3")

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

        brain.screen.print(optical_sensor.hue())
        brain.screen.print(MAX_SPEED)
        
       
        if controllerMode == 0:
     
            if controller_1.buttonUp.pressing():
                left_motor_a.set_velocity(50, PERCENT)
                left_motor_b.set_velocity(50, PERCENT)
                right_motor_a.set_velocity(50, PERCENT)
                right_motor_b.set_velocity(50, PERCENT)
                left_motor_a.spin(FORWARD)
                right_motor_a.spin(FORWARD)
                left_motor_b.spin(FORWARD)
                right_motor_b.spin(FORWARD)
            elif controller_1.buttonDown.pressing():
                left_motor_a.set_velocity(50, PERCENT)
                left_motor_b.set_velocity(50, PERCENT)
                right_motor_a.set_velocity(50, PERCENT)
                right_motor_b.set_velocity(50, PERCENT)
                left_motor_a.spin(REVERSE)
                right_motor_a.spin(REVERSE)
                left_motor_b.spin(REVERSE)
                right_motor_b.spin(REVERSE)
            else:
                # Joystick tank control (Controller 1)
                drive_left = controller_1.axis3.position()   # Left stick Y
                drive_right = controller_1.axis2.position()  # Right stick Y

                # Deadband threshold
                deadband = 15
                if abs(drive_left) < deadband:
                    drive_left = 0
                if abs(drive_right) < deadband:
                    drive_right = 0

                # Apply tank drive
                left_motor_a.spin(FORWARD, drive_left, PERCENT)
                left_motor_b.spin(FORWARD, drive_left, PERCENT)
                right_motor_a.spin(FORWARD, drive_right, PERCENT)
                right_motor_b.spin(FORWARD, drive_right, PERCENT)
        else:
            # Arcade control mode (Controller 1)
            forward_power = controller_1.axis3.position()  # Left stick Y
            turn_power = controller_1.axis1.position()     # Left stick X
            
            left_power = forward_power + turn_power
            right_power = forward_power - turn_power
            
            left_motor_a.set_velocity(left_power, PERCENT)
            left_motor_b.set_velocity(left_power, PERCENT)
            right_motor_a.set_velocity(right_power, PERCENT)
            right_motor_b.set_velocity(right_power, PERCENT)
            
            left_motor_a.spin(FORWARD)
            left_motor_b.spin(FORWARD)
            right_motor_a.spin(FORWARD)
            right_motor_b.spin(FORWARD)

       

        first_intake_control = (controller_2.buttonL1.pressing() - controller_2.buttonL2.pressing()) * MAX_SPEED
        basket_intake_control = (controller_2.buttonR1.pressing() - controller_2.buttonR2.pressing()) * MAX_SPEED
        toprack_control = (controller_2.buttonA.pressing() - controller_2.buttonY.pressing()) * 60


        first_intake.spin(FORWARD, first_intake_control * 10, PERCENT)
        basket_intake_motor.spin(FORWARD, basket_intake_control * 10, PERCENT)    
        toprack.spin(REVERSE, toprack_control * 10, PERCENT)
        first_intake.spin(FORWARD, first_intake_control * MOTOR_MULTIPLIER, PERCENT)
        basket_intake_motor.spin(FORWARD, basket_intake_control * MOTOR_MULTIPLIER, PERCENT)    
        toprack.spin(REVERSE, toprack_control * MOTOR_MULTIPLIER, PERCENT)
       

        if controller_1.buttonLeft.pressing():
            brain.screen.clear_screen()
            controllerMode = 0  
            brain.screen.print("Tank Drive Mode")
            wait(200, MSEC)  
        elif controller_1.buttonRight.pressing():
            brain.screen.clear_screen()
            controllerMode = 1  # Arcade mode
            brain.screen.print("Arcade Drive Mode")
            wait(200, MSEC)  

        # Autonomous function (X button on either controller)
        if controller_1.buttonX.pressing() or controller_2.buttonX.pressing():
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
        if controller_2.buttonUp.pressing():
            MAX_SPEED = min(100, MAX_SPEED + 5)
            wait(100, MSEC)
            brain.screen.clear_screen()
        if True: # controller_2.buttonDown.pressing():
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

                        brain.screen.next_row()
                        brain.screen.print("Red Detected")
                        toprack.spin(REVERSE, 100, PERCENT)
                    #wait(1, SECONDS)
                    #toprack.stop()

                    elif (hue >= 210) and (hue <= 230):

                        brain.screen.next_row()
                        brain.screen.print("Blue Detected")
                        toprack.spin(FORWARD, 100, PERCENT)


                    else:
                        brain.screen.next_row()
                        brain.screen.print("No Color Detected")
                else:
                    brain.screen.next_row()
                    brain.screen.print("Brightness less than ten " + str(brightness))

            else:
                brain.screen.next_row()
                brain.screen.print("No Object Detected")

       # brain.screen.new_line()ain.screen.print("Brightness less than ten")

        sleep(10)
       # brain.screen.new_line()  # Removed typo and malformed code


drive_task()


