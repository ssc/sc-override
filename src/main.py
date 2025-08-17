# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       magicgear                                                    #
# 	Created:      8/6/2025, 9:54:00 PM                                         #
# 	Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #

from vex import *

# Brain should be defined by default
brain = Brain()

# 
#

# The controller
controller = Controller()

# Drive motors
left_drive_1 = Motor(Ports.PORT20, GearSetting.RATIO_18_1, False)
left_drive_2 = Motor(Ports.PORT12, GearSetting.RATIO_18_1, False)
right_drive_1 = Motor(Ports.PORT14, GearSetting.RATIO_18_1, True)
right_drive_2 = Motor(Ports.PORT15, GearSetting.RATIO_18_1, True)

# Arm and claw motors will have brake mode set to hold
# Claw motor will have max torque limited
#claw_motor = Motor(Ports.PORT3, GearSetting.RATIO_18_1, False)
arm_motor = Motor(Ports.PORT11, GearSetting.RATIO_18_1, False)

# Auxilary motors
motor_aux_1 = Motor(Ports.PORT5, GearSetting.RATIO_18_1, False)
motor_aux_2 = Motor(Ports.PORT7, GearSetting.RATIO_18_1, False)
toprack = Motor(Ports.PORT10, GearSetting.RATIO_18_1, False)

# Max motor speed (percent) for motors controlled by buttons
MAX_SPEED = 40

controllerMode = 0
def auto():
    Forward(1)

def Forward(degrees):
  left_drive_1.spin_to_position(degrees)
  left_drive_2.spin_to_position(degrees)
  right_drive_1.spin_to_position(degrees)
  right_drive_2.spin_to_position(degrees)


def Backward(degrees):
  left_drive_1.spin_to_position(-degrees)
  left_drive_2.spin_to_position(-degrees)
  right_drive_1.spin_to_position(-degrees)
  right_drive_2.spin_to_position(-degrees)


def Left(degrees):
  left_drive_1.spin_to_position(-degrees)
  left_drive_2.spin_to_position(-degrees)
  right_drive_1.spin_to_position(degrees)
  right_drive_2.spin_to_position(degrees)


def Right(degrees):
  left_drive_1.spin_to_position(degrees)
  left_drive_2.spin_to_position(degrees)
  right_drive_1.spin_to_position(-degrees)
  right_drive_2.spin_to_position(-degrees)


def add_MAXSPEED():
    global MAX_SPEED
    MAX_SPEED += 10
    if MAX_SPEED > 100:
        MAX_SPEED = 100

def remove_MAXSPEED():
    global MAX_SPEED
    MAX_SPEED -= 10
    if MAX_SPEED < 0:
        MAX_SPEED = 0

#
# All motors are controlled from this function which is run as a separate thread
#
def drive_task():
    drive_left = 0
    drive_right = 0

    # setup the claw motor
    #claw_motor.set_max_torque(25, PERCENT)
    #claw_motor.set_stopping(HOLD)

    # setup the arm motor
    #arm_motor.set_stopping(HOLD)

    # loop forever

    controller.buttonR2.pressed(add_MAXSPEED)
    controller.buttonR1.pressed(remove_MAXSPEED)
    global controllerMode

    #Autonomous
    #Forward(720)
    #controller.buttonY.pressed(auto)






    while True:
        # buttons
        # Three values, max, 0 and -max.
        brain.screen.print(MAX_SPEED)
        if controllerMode == 0:
            control_l1  = (controller.buttonL1.pressing() - controller.buttonL2.pressing()) * MAX_SPEED
            control_r1  = (controller.buttonR1.pressing() - controller.buttonR2.pressing()) * MAX_SPEED
            control_l2  = (controller.buttonUp.pressing() - controller.buttonDown.pressing()) * MAX_SPEED
            control_r2  = (controller.buttonA.pressing() - controller.buttonB.pressing()) * MAX_SPEED
        else:
            left_drive_1.set_velocity((controller.axis3.position() + controller.axis1.position()), PERCENT)
            left_drive_2.set_velocity((controller.axis3.position() + controller.axis1.position()), PERCENT)
            right_drive_1.set_velocity((controller.axis3.position() - controller.axis1.position()), PERCENT)
            right_drive_2.set_velocity((controller.axis3.position() - controller.axis1.position()), PERCENT)




        if controller.buttonB.pressing():
            # Toggle controller mode
            brain.screen.clear_screen()
            controllerMode = (controllerMode + 1) % 2
            if controllerMode == 0:
                brain.screen.print("drive")
            else:
                brain.screen.print("arm")

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
            left_drive_1.spin(FORWARD, drive_left, PERCENT)
            left_drive_2.spin(FORWARD, drive_left, PERCENT)
            right_drive_1.spin(FORWARD, drive_right, PERCENT)
            right_drive_2.spin(FORWARD, drive_right, PERCENT)
        else:
            left_drive_1.spin(FORWARD)
            left_drive_2.spin(FORWARD)
            right_drive_1.spin(FORWARD)
            right_drive_2.spin(FORWARD)
        # Claw and Arm motors
        arm_motor.spin(REVERSE, control_l1, PERCENT)
        #claw_motor.spin(FORWARD, control_r1, PERCENT)
 
        # and the auxilary motors
        motor_aux_1.spin(FORWARD, control_l2, PERCENT)
        motor_aux_2.spin(FORWARD, control_r2, PERCENT)
        toprack.spin(FORWARD, control_r1, PERCENT)

        # No need to run too fast
        sleep(10)

# Run the drive code
drive = Thread(drive_task)

# Python now drops into REPL
