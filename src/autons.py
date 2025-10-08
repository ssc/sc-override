
gyro_360 = 354
from vex import *
inertial_sensor = Inertial(Ports.PORT2)
def calibratedAngle(idealAngle):
    return (idealAngle * gyro_360/360)


left_motor_a = Motor(Ports.PORT19, GearSetting.RATIO_18_1, False)
left_motor_b = Motor(Ports.PORT12, GearSetting.RATIO_18_1, False)




# Create the right Motors and group them under the MotorGroup "right_motors"
right_motor_a = Motor(Ports.PORT14, GearSetting.RATIO_18_1, True)
right_motor_b = Motor(Ports.PORT16, GearSetting.RATIO_18_1, True)

right_motors = MotorGroup(right_motor_a, right_motor_b)
left_motors = MotorGroup(left_motor_a, left_motor_b)

drivetrain = DriveTrain(left_motors, right_motors, 330, 335, 231, MM, 1)

def turnTestingAuton():
    # reset the gyro sensor to 0 degrees
    #change all Gyro to inertial

    inertial_sensor.reset_rotation()
    
    # turn to 90 degrees
    drivetrain.turn_to_heading(calibratedAngle(90), DEGREES, wait=True)
    
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