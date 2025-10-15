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
gyro_360 = 354

def calibratedAngle(idealAngle):
    return (idealAngle * gyro_360/360)
        
distance = 0


# actions to do when the program starts
brain.screen.clear_screen()

left_tube_spin = 0
right_tube_spin = 0

# Brain and Controllers



# Configure the optical sensor on a specific port (change port number as needed)
potentiometer = Potentiometer(brain.three_wire_port.b) 
distance_sensor = Distance(Ports.PORT10)
inertial_sensor = Inertial(Ports.PORT1)
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
tube_intake_motor = Motor(Ports.PORT3, GearSetting.RATIO_18_1, False)

# Construct a 4-Motor Drivetrain
# Parameters: circumference, distance between wheels on axle, distance between axles, units, gear ratio
#drivetrain = DriveTrain(left_motors, right_motors, 330, 335, 231, MM, 1)
drivetrain = SmartDrive(left_motors, right_motors, inertial_sensor,330, 335, 231, MM, 1)


# Intake/Mechanism motors
first_intake = Motor(Ports.PORT11, GearSetting.RATIO_18_1, True)
basket_intake_motor = Motor(Ports.PORT7, GearSetting.RATIO_18_1, False)
toprack = Motor(Ports.PORT17, GearSetting.RATIO_18_1, False)

#def terminate_Program():
#     while True:
#         if controller_1.buttonDown.pressing():
#             brain.screen.clear_screen()
#             left_motors.stop()
#             right_motors.stop()
#             first_intake.stop()
#             basket_intake_motor.stop()
#             toprack.stop()
#             tube_intake_motor.stop()        

# kill_switch = Thread(terminate_Program)

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

#def turn_until_distance(target_distance_1, target_distance_2, direction):
#     global MAX_SPEED
#     global distance
#     left_motors.set_velocity(MAX_SPEED / 2, PERCENT)
#     right_motors.set_velocity(MAX_SPEED / 2, PERCENT)
    
#     while True:
#         if direction == 'left':

#             if distance >= target_distance_1 and distance <= target_distance_2:
#                 break
#             else:
#                 left_motors.spin(FORWARD)
#                 right_motors.spin(REVERSE)
                

#         elif direction == 'right':

#             if distance >= target_distance_1 and distance <= target_distance_2:
#                 break
#             else:
#                 left_motors.spin(REVERSE)
#                 right_motors.spin(FORWARD)

#     left_motors.stop()
#     right_motors.stop()

# def test_funct():
#     turn_until_distance(1, 70, 'right')

def skills_auton():
    global MAX_SPEED
    vex_brain_slot = 1
    while inertial_sensor.is_calibrating():
        controller_1.screen.set_cursor(2,1)

        controller_1.screen.print("Calibrating Gyro")
        wait(100, MSEC)
    inertial_sensor.reset_rotation()
    inertial_sensor.set_heading(0, DEGREES)
    


    drivetrain.drive_for(FORWARD,23, INCHES, 50, PERCENT )
    drivetrain.turn_to_heading(calibratedAngle(16), DEGREES, wait=True)
    drivetrain.drive_for(FORWARD,8, INCHES, 25, PERCENT )
    first_intake.spin(FORWARD, 100, PERCENT)
    basket_intake_motor.spin(REVERSE, 100, PERCENT)
    drivetrain.drive_for(FORWARD, 13, INCHES, 10, PERCENT)



    wait(2,SECONDS)
    first_intake.stop()
    basket_intake_motor.stop()

#     if vex_brain_slot == 1:
#         drivetrain.turn_to_heading(calibratedAngle(135), DEGREES, wait=True)

#     else:

#         drivetrain.turn_to_heading(calibratedAngle(250), DEGREES, wait=True)
     
#     drivetrain.drive_for(FORWARD, 33, INCHES, 35 , PERCENT)


#     if vex_brain_slot == 1:
#         turn_until_distance(750,'left',5)
#         drivetrain.turn_for(LEFT, 5,DEGREES,5,PERCENT)


#     else: 
#         turn_until_distance(750,'right',5)

     
#     move_until_distance(125,'reverse',20)

#     #  if vex_brain_slot == 1:
    
#     #     drivetrain.turn_for(LEFT, 2,DEGREES,5,PERCENT)

#     #  else:
         
#     #     drivetrain.turn_for(RIGHT, 2,DEGREES,5,PERCENT)
     
#     first_intake.spin(FORWARD, 50, PERCENT)
#     basket_intake_motor.spin(FORWARD, 100, PERCENT)
#     brain.screen.print("we made it")
#     toprack.spin(REVERSE, 50, PERCENT)
#     wait(7, SECONDS)
#     brain.screen.print("we made it 2")
#     basket_intake_motor.stop()
#     first_intake.stop()
#     toprack.stop()
#     drivetrain.drive_for(REVERSE, 2, INCHES, 75 , PERCENT)
#     drivetrain.drive_for(FORWARD, 4, INCHES, 75 , PERCENT)
#     drivetrain.turn_to_heading(calibratedAngle(5), DEGREES, wait=True)
#     move_until_distance(65,'reverse',25)
#     drivetrain.turn_to_heading(calibratedAngle(260), DEGREES, wait=True)
#     first_intake.spin(FORWARD, 100, PERCENT)
#     basket_intake_motor.spin(REVERSE, 100, PERCENT)
#     drivetrain.drive_for(FORWARD, 70, INCHES, 75 , PERCENT)
#     first_intake.stop()
#     basket_intake_motor.stop()


# def auton_funct():
#      global MAX_SPEED
#      if potentiometer.value() < 1250:
#          vex_brain_slot = 1
#          brain.screen.print("right Side Auton")

#      elif potentiometer.value() > 2250:
#          vex_brain_slot = 2

#          brain.screen.print("left Side Auton")
#      SCALE_VALUE = 0.6
    
#      while inertial_sensor.is_calibrating():
#         controller_1.screen.set_cursor(2,1)

#         controller_1.screen.print("Calibrating Gyro")
#         wait(100, MSEC)
#      inertial_sensor.reset_rotation()
#      inertial_sensor.set_heading(0, DEGREES)
    


#      drivetrain.drive_for(FORWARD,12, INCHES, 50, PERCENT )
#      #drivetrain.turn_to_heading(calibratedAngle(35), DEGREES, wait=True)
#      first_intake.spin(FORWARD, 100, PERCENT)
#      basket_intake_motor.spin(REVERSE, 100, PERCENT)
#      drivetrain.drive_for(FORWARD, 9, INCHES, 10, PERCENT)


     
#      wait(0.5,SECONDS)
#      first_intake.stop()
#      basket_intake_motor.stop()

#      if vex_brain_slot == 1:
#         drivetrain.turn_to_heading(calibratedAngle(115), DEGREES, wait=True)

#      else:

#         drivetrain.turn_to_heading(calibratedAngle(245), DEGREES, wait=True)
     
#      drivetrain.drive_for(FORWARD, 32, INCHES, 35 , PERCENT)

#      if vex_brain_slot == 1:
#         turn_until_distance(750,'left',5)

#      else: 
#         turn_until_distance(750,'right',5)

     
#      move_until_distance(150,'reverse',20)

#     #  if vex_brain_slot == 1:
    
#     #     drivetrain.turn_for(LEFT, 2,DEGREES,5,PERCENT)

#     #  else:
         
#     #     drivetrain.turn_for(RIGHT, 2,DEGREES,5,PERCENT)
     
#      first_intake.spin(FORWARD, 50, PERCENT)
#      basket_intake_motor.spin(FORWARD, 100, PERCENT)
#      brain.screen.print("we made it")
#      toprack.spin(REVERSE, 100, PERCENT)
#      wait(5, SECONDS)
#      brain.screen.print("we made it 2")
#      basket_intake_motor.stop()
#      first_intake.stop()
#      toprack.stop()
#      drivetrain.drive_for(REVERSE, 2, INCHES, 75 , PERCENT)
        #  drivetrain.drive_for(FORWARD, 450, MM, 50, PERCENT)
        #  drivetrain.turn_for(LEFT, 30 * SCALE_VALUE, DEGREES, 25, PERCENT)
        #  drivetrain.drive_for(FORWARD, 300, MM, 25, PERCENT)
        #  drivetrain.turn_for(RIGHT, 25 * SCALE_VALUE, DEGREES, 25, PERCENT)
        #  drivetrain.drive_for(FORWARD, 550, MM, 20, PERCENT)
        #  wait(1, SECONDS)
        #  basket_intake_motor.stop()
        #  first_intake.stop()
        #  drivetrain.drive_for(REVERSE, 620, MM, 50, PERCENT)
        #  #drivetrain.turn_for(LEFT, 105 * SCALE_VALUE, DEGREES, 25, PERCENT)
        #  turn_until_distance(500,'left',5)
        #  drivetrain.drive_for(FORWARD, 685, MM, 75, PERCENT)
        #  #where it turns to look at the goal
        #  #drivetrain.turn_for(LEFT, 100 * SCALE_VALUE, DEGREES, 25, PERCENT)
        #  turn_until_distance(1, 70, 'left')

        #  drivetrain.drive_for(REVERSE, 200, MM, 50, PERCENT)

        #  brain.screen.print("we made it3")

def potentiometer_test():
    brain.screen.clear_screen()
    brain.screen.print("Potentiometer Test")
    while True:
        brain.screen.new_line()
        brain.screen.print("Value: " + str(potentiometer.value()))
        wait(100, MSEC)


def drive_task():
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

            tube_intake_motor_control = (controller_1.buttonRight.pressing()) * -100
        else:
            if controller_1.buttonLeft.pressing()   or controller_2.buttonLeft.pressing():
                left_tube_spin = 1
                tube_intake_motor_control = (controller_1.buttonLeft.pressing()) * 100
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
            

        first_intake.spin(FORWARD, first_intake_control * 8, PERCENT)
        basket_intake_motor.spin(FORWARD, basket_intake_control * 10, PERCENT)    
        toprack.spin(REVERSE, toprack_control * 50, PERCENT)
        first_intake.spin(FORWARD, first_intake_control * 8, PERCENT)
        basket_intake_motor.spin(FORWARD, basket_intake_control * MOTOR_MULTIPLIER, PERCENT)    
        toprack.spin(REVERSE, toprack_control * 50, PERCENT)
        tube_intake_motor.spin(FORWARD, tube_intake_motor_control, PERCENT)
       

        #if controller_1.buttonLeft.pressing() or controller_2.buttonLeft.pressing():
        #     brain.screen.clear_screen()
        #     controllerMode = 0  
        #     brain.screen.print("Tank Drive Mode")
        #     wait(200, MSEC)  
        # elif controller_1.buttonRight.pressing() or controller_2.buttonRight.pressing():
        #     brain.screen.clear_screen()
        #     controllerMode = 1  # Arcade mode
        #     brain.screen.print("Arcade Drive Mode")
        #     wait(200, MSEC)  

        if controller_2.buttonUp.pressing():
            first_intake.spin(REVERSE,10,PERCENT)
            basket_intake_motor.spin(FORWARD,10,PERCENT)


        # Autonomous function (X button on either controller)
        #and controller_2.buttonX.pressing()
        if controller_1.buttonX.pressing():
            brain.screen.clear_screen()
            if potentiometer.value() < 2250 and potentiometer.value() > 1250:
                auton = 2
                brain.screen.print("right Side Auton")
            else:
                auton = 1

        if auton == 1:
            auton_funct()
            auton = 0

        if auton == 2:
            skills_auton()
            auton = 0

        # Hopper pickup function (B button on either controller)
        # if controller_1.buttonB.pressing() or controller_2.buttonB.pressing():
        #     tube_intake_motor.spin(FORWARD, 100, PERCENT)
        #     #brain.screen.clear_screen()
        #     #hopper_running = 1

        # else: 
        #     tube_intake_motor.stop()
            #brain.screen.clear_screen()
            #hopper_running = 0
        
        #if hopper_running == 1:
            #hopper_pickup()
            #hopper_running = 0
        #change new_line to new_row
        # Speed adjustment (Up/Down arrows on Controller 2 for intake speed)
        if controller_2.buttonUp.pressing() or controller_1.buttonUp.pressing():
            MAX_SPEED = min(100, MAX_SPEED + 5)
            wait(100, MSEC)
            brain.screen.clear_screen()
        # if True: # controller_2.buttonDown.pressing():
        #     MAX_SPEED = max(10, MAX_SPEED - 5)
        #     wait(100, MSEC)
    
        #     if optical_sensor.is_near_object():
        #         brain.screen.next_row()
        #         brain.screen.clear_screen()
        #         brain.screen.print("Object Detected")
        #         optical_sensor.set_light_power(100, PERCENT)
        #         brightness = optical_sensor.brightness()
        #         hue = optical_sensor.hue()
        #         #brain.screen.clear_screen()
        #         if brightness > 10:
        #             brain.screen.next_row()
        #             brain.screen.print("Brightness > ten: " + str(brightness))
        #             if (hue <= 20) or (hue >= 340):

                        
        #                 #toprack.spin(REVERSE, 1000, PERCENT)
        #                 #wait(0.5, SECONDS)
        #                 toprack.stop()

        #             elif (hue >= 210) and (hue <= 230):

        #                 brain.screen.next_row()
        #                 brain.screen.print("Blue Detected")
                        

        #             else:
        #                 brain.screen.next_row()
        #                 brain.screen.print("No Color Detected")
        #         else:
        #             brain.screen.next_row()
        #             brain.screen.print("Brightness less than ten " + str(brightness))

        #     else:
        #         brain.screen.next_row()
        #         brain.screen.print("No Object Detected")

       # brain.screen.new_line()ain.screen.print("Brightness less than ten")

        sleep(10)
       # brain.screen.new_line()  # Removed typo and malformed code

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
#comp = Competition(user_control, autonomous)
#turn_until_distance(100,'left',20)
drive_task()



#test_funct()