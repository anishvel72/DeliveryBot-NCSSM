import Jetson.GPIO as GPIO
import time

# Pin assignments
GND_PIN = 39      # Ground (just for reference)
VCC_PIN = 4       # 5V (just for reference)

R_EN = 38         # Right enable
L_EN = 37         # Left enable
RPWM = 33         # Right PWM
LPWM = 15         # Left PWM

# GPIO setup
GPIO.setmode(GPIO.BOARD)  # Use physical pin numbers

# Set up EN pins as output
GPIO.setup(R_EN, GPIO.OUT)
GPIO.setup(L_EN, GPIO.OUT)

# Set up PWM pins as output
GPIO.setup(RPWM, GPIO.OUT)
GPIO.setup(LPWM, GPIO.OUT)

# Initialize PWM
pwm_freq = 1000  # 1 kHz is typical for DC motors
rpwm_pwm = GPIO.PWM(RPWM, pwm_freq)
lpwm_pwm = GPIO.PWM(LPWM, pwm_freq)

# Start PWM at 0 duty cycle
rpwm_pwm.start(0)
lpwm_pwm.start(0)

# Function to move motor forward
def forward(speed=50):
    GPIO.output(L_EN, GPIO.HIGH)
    GPIO.output(R_EN, GPIO.LOW)
    lpwm_pwm.ChangeDutyCycle(speed)
    rpwm_pwm.ChangeDutyCycle(0)

# Function to move motor backward
def backward(speed=50):
    GPIO.output(L_EN, GPIO.LOW)
    GPIO.output(R_EN, GPIO.HIGH)
    lpwm_pwm.ChangeDutyCycle(0)
    rpwm_pwm.ChangeDutyCycle(speed)

# Function to stop motor
def stop():
    GPIO.output(L_EN, GPIO.LOW)
    GPIO.output(R_EN, GPIO.LOW)
    lpwm_pwm.ChangeDutyCycle(0)
    rpwm_pwm.ChangeDutyCycle(0)

# Example usage
try:
    print("Motor forward")
    forward(70)  # 70% speed
    time.sleep(2)
    
    print("Motor backward")
    backward(50)  # 50% speed
    time.sleep(2)
    
    print("Stop motor")
    stop()
    
finally:
    rpwm_pwm.stop()
    lpwm_pwm.stop()
    GPIO.cleanup()