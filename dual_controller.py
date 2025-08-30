from vex import *

brain = Brain()
controller_1 = Controller(PRIMARY)    
controller_2 = Controller(PARTNER)    


def dual_controller_test():
   
    
    while True:
        
        left_speed = controller_1.axis3.position()   
        right_speed = controller_1.axis2.position()  
        
        
        arm_speed = controller_2.axis3.position()    
        intake_button = controller_2.buttonR1.pressing()  
        
       
        
        wait(20, MSEC)  

if __name__ == "__main__":
    dual_controller_test()