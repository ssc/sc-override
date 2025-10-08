#https://medium.com/@aleksej.gudkov/python-pid-controller-example-a-complete-guide-5f35589eec86

# >>> prvar = 1000
# prvar = 1000
# >>> curval = 0
# curval = 0
# >>> p = pid.PIDController(Kp=1.0, Ki=0.1, Kd=0.05, setpoint=prvar)
# p = pid.PIDController(Kp=1.0, Ki=0.1, Kd=0.05, setpoint=prvar)
# >>> p.compute(curval, 1)
# p.compute(curval, 1)
# 1150.0
# >>> p.compute(900, 1)
# p.compute(900, 1)
# 165.0
# >>> p.compute(1100, 1)
# p.compute(1100, 1)
# -10.0
# >>> 

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