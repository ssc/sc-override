# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       magicgear                                                    #
# 	Created:      8/16/2025, 6:09:00 PM                                        #
# 	Created:      8/16/2025, 6:09:00 PM                                        #
# 	Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #

MAX_SPEED = 0
# Library imports
from vex import *
from vex import *

brain = Brain()
controller_1 = Controller(PRIMARY)    
controller_2 = Controller(PARTNER)    


# Brain should be defined by defaultF
brain=Brain()
brain=Brain()
controller = Controller(ControllerType.PRIMARY)
controller2 = Controller(ControllerType.PARTNER)
controllerMode = 0
auton = 0
hopper_running = 0
b_was_pressed = 0
brain.screen.print("Hello V5")
# Create the left Motors and group them under the
# MotorGroup "left_motors".
left_motor_a = Motor(Ports.PORT19, GearSetting.RATIO_18_1, False)
left_motor_b = Motor(Ports.PORT12, GearSetting.RATIO_18_1, False)
left_motors = MotorGroup(left_motor_a, left_motor_b)

# Create the right Motors and group them under the
# MotorGroup "right_motors".
right_motor_a = Motor(Ports.PORT14, GearSetting.RATIO_18_1, True)
right_motor_b = Motor(Ports.PORT16, GearSetting.RATIO_18_1, True)
right_motors = MotorGroup(right_motor_a, right_motor_b)
# Construct a 4-Motor Drivetrain "drivetrain" with the
# 1 is the circumference, 2 is the distance on a single axle between two wheels, 3 is the distance between the two axles, 4 is the unit of measurement
# DriveTrain class.
drivetrain = DriveTrain(left_motors, right_motors, 330, 335, 231, MM, 1)
def hopper_pickup():
    SCALE_VALUE = 0.6
    global MAX_SPEED



    drivetrain.turn_for(RIGHT, 20 * SCALE_VALUE, DEGREES, 25, PERCENT)
    
    drivetrain.turn_for(LEFT, 20 * SCALE_VALUE, DEGREES, 25, PERCENT)

    drivetrain.drive_for(FORWARD, 10, MM, 50, PERCENT)


    
    
def auton_funct():
    #was getting annoying by accadntily hitting the wrong button
    
    global MAX_SPEED
    
    # Move the Drivetrain forward 1000 mm at 50% speed.
    #drivetrain.drive_for(FORWARD, 500, MM, 25, PERCENT)
    # Turn the Drivetrain left 90 degrees at 50% speed.

    SCALE_VALUE = 0.6
    first_intake = Motor(Ports.PORT11, GearSetting.RATIO_18_1, False)
    basket_intake_motor = Motor(Ports.PORT15, GearSetting.RATIO_18_1, False)
    toprack = Motor(Ports.PORT17, GearSetting.RATIO_18_1, False)

    #drivetrain.turn_for(LEFT, 90 * SCALE_VALUE, DEGREES, 25, PERCENT)
    # Move the Drivetrain backward 500 mm at 50% speed.
    #drive in a square
    # for _ in range(4):      
    #     drivetrain.drive_for(FORWARD, 200, MM, 25, PERCENT)
    #     drivetrain.turn_for(LEFT, 90 * SCALE_VALUE, DEGREES, 25, PERCENT)
    # start of 15 second auton section
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
    # drivetrain.turn_for(LEFT, 90 * SCALE_VALUE, DEGREES, 25, PERCENT)
    # drivetrain.drive_for(FORWARD, 200, MM, 25, PERCENT)
    # drivetrain.turn_for(RIGHT, 10 * SCALE_VALUE, DEGREES, 25, PERCENT)
    # drivetrain.drive_for(FORWARD, 2000, MM, 25, PERCENT)
    # drivetrain.turn_for(LEFT, 100 * SCALE_VALUE, DEGREES, 25, PERCENT)

    
def drive_task():
    drive_left = 0
    drive_right = 0
    global MAX_SPEED
    global hopper_running
    
    #global b_was_pressed
    MAX_SPEED= 40
    first_intake = Motor(Ports.PORT11, GearSetting.RATIO_18_1, False)
    basket_intake_motor = Motor(Ports.PORT15, GearSetting.RATIO_18_1, False)


    # Auxilary motors
    #motor_aux_1 = Motor(Ports.PORT5, GearSetting.RATIO_18_1, False)
    #motor_aux_2 = Motor(Ports.PORT7, GearSetting.RATIO_18_1, False)
    toprack = Motor(Ports.PORT17, GearSetting.RATIO_18_1, False)



    # setup the claw motor
    #claw_motor.set_max_torque(25, PERCENT)
    #claw_motor.set_stopping(HOLD)

    # setup the arm motor
    #arm_motor.set_stopping(HOLD)

    # loop forever

    global auton
    global auton
    global controllerMode



    #Autonomous
    #Forward(720)
    #controller.buttonY.pressed(auto)
    auton = 0
    auton = 0

    while True:
        # buttons
        # Three values, max, 0 and -max.
        brain.screen.print(MAX_SPEED)
        if controllerMode == 0:
   
            control_A  = (controller.buttonA.pressing() - controller.buttonY.pressing()) * MAX_SPEED
            control_l1  = (controller.buttonL1.pressing() - controller.buttonL2.pressing()) * MAX_SPEED
            control_r1  = (controller.buttonR1.pressing() - controller.buttonR2.pressing()) * MAX_SPEED
            #control_r2  = (controller.buttonR2.pressing()) * MAX_SPEED
            #control_Y  = (controller.buttonY.pressing() - controller.buttonA.pressing()) * MAX_SPEED
            #control_l2  = (controller.buttonL2.pressing() - controller.buttonL1.pressing()) * MAX_SPEED
            #control_r2  = (controller.buttonA.pressing() - controller.buttonB.pressing()) * MAX_SPEED
        else:
            # Arcade control
            left_motor_a.set_velocity((controller.axis3.position() + controller.axis1.position()), PERCENT)
            left_motor_b.set_velocity((controller.axis3.position() + controller.axis1.position()), PERCENT)
            right_motor_a.set_velocity((controller.axis3.position() - controller.axis1.position()), PERCENT)
            right_motor_b.set_velocity((controller.axis3.position() - controller.axis1.position()), PERCENT)
            left_motor_a.set_velocity((controller.axis3.position() + controller.axis1.position()), PERCENT)
            left_motor_b.set_velocity((controller.axis3.position() + controller.axis1.position()), PERCENT)
            right_motor_a.set_velocity((controller.axis3.position() - controller.axis1.position()), PERCENT)
            right_motor_b.set_velocity((controller.axis3.position() - controller.axis1.position()), PERCENT)





     
        #if controller.buttonB.pressing():
            # Toggle controller mode
            # brain.screen.clear_screen()
            # controllerMode = (controllerMode + 1) % 2
            # if controllerMode == 0:
            #     brain.screen.print("drive")
            # else:
            #     brain.screen.print("arm")


        if controller.buttonX.pressing():
            # Toggle controller mode
            brain.screen.clear_screen()
            auton = 1


        if auton == 1:
            auton_funct()
            auton = 0
            pass    


        if controller.buttonB.pressing():
            # Toggle controller mode
            brain.screen.clear_screen()

            hopper_running = 1


        if hopper_running == 1:
            hopper_pickup()
            hopper_running = 0

  



        if controller.buttonX.pressing():
            # Toggle controller mode
            brain.screen.clear_screen()
            auton = 1


        if auton == 1:
            auton_funct()
            auton = 0
            pass    

        # joystick tank control
        drive_left = controller.axis3.position()
        drive_right = controller.axis2.position()

        # threshold the variable channels so the drive does not
        # move if the joystick axis does not return exactly to 0
        deadband = 15
        if abs(drive_left) < deadband:
            drive_left = 0
        if abs(drive_right) < deadband:
            drive_right = 0

        # Now send all drive values to motors
        
        


        
        



        # The drivetrain

        if controllerMode == 0:
            if controller.buttonUp.pressing():
                left_motor_a.set_velocity(50, PERCENT)
                left_motor_b.set_velocity(50, PERCENT)
                right_motor_a.set_velocity(50, PERCENT)
                right_motor_b.set_velocity(50, PERCENT)
                left_motor_a.spin(FORWARD)
                right_motor_a.spin(FORWARD)
                left_motor_b.spin(FORWARD)
                right_motor_b.spin(FORWARD)

            else:
                if controller.buttonDown.pressing():
                    left_motor_a.set_velocity(50, PERCENT)
                    left_motor_b.set_velocity(50, PERCENT)
                    right_motor_a.set_velocity(50, PERCENT)
                    right_motor_b.set_velocity(50, PERCENT)
                    left_motor_a.spin(REVERSE)
                    right_motor_a.spin(REVERSE)
                    left_motor_b.spin(REVERSE)
                    right_motor_b.spin(REVERSE)
                else:
                    left_motor_a.spin(FORWARD, drive_left, PERCENT)
                    left_motor_b.spin(FORWARD, drive_left, PERCENT)
                    right_motor_a.spin(FORWARD, drive_right, PERCENT)
                    right_motor_b.spin(FORWARD, drive_right, PERCENT)
        else:
            left_motor_a.spin(FORWARD)
            left_motor_b.spin(FORWARD)
            right_motor_a.spin(FORWARD)
            right_motor_b.spin(FORWARD)
            left_motor_a.spin(FORWARD)
            left_motor_b.spin(FORWARD)
            right_motor_a.spin(FORWARD)
            right_motor_b.spin(FORWARD)
        # Claw and Arm motors
        
        


        first_intake.spin(FORWARD, control_l1 * 10, PERCENT)
        basket_intake_motor.spin(FORWARD, control_r1 * 10, PERCENT)    
        toprack.spin(REVERSE, control_A * 10, PERCENT)

        # No need to run too fast
        sleep(10)    
        sleep(10)    


drive_task()
        

drive_task()
        
