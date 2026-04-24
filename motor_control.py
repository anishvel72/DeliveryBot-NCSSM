import Jetson.GPIO as GPIO
import time
import os

# Pin assignments
R_EN = 38
L_EN = 37
RPWM = 33
LPWM = 15

# Suppress "channel already in use" warnings from dirty previous runs
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(R_EN, GPIO.OUT)
GPIO.setup(L_EN, GPIO.OUT)
GPIO.setup(RPWM, GPIO.OUT)
GPIO.setup(LPWM, GPIO.OUT)

pwm_freq = 1000
rpwm_pwm = GPIO.PWM(RPWM, pwm_freq)
lpwm_pwm = GPIO.PWM(LPWM, pwm_freq)

rpwm_pwm.start(0)
lpwm_pwm.start(0)

def forward(speed=50):
    GPIO.output(L_EN, GPIO.HIGH)
    GPIO.output(R_EN, GPIO.LOW)
    lpwm_pwm.ChangeDutyCycle(speed)
    rpwm_pwm.ChangeDutyCycle(0)

def backward(speed=50):
    GPIO.output(L_EN, GPIO.LOW)
    GPIO.output(R_EN, GPIO.HIGH)
    lpwm_pwm.ChangeDutyCycle(0)
    rpwm_pwm.ChangeDutyCycle(speed)

def stop():
    GPIO.output(L_EN, GPIO.LOW)
    GPIO.output(R_EN, GPIO.LOW)
    lpwm_pwm.ChangeDutyCycle(0)
    rpwm_pwm.ChangeDutyCycle(0)

def safe_cleanup():
    """Stop PWM and clean up GPIO, tolerating bad file descriptors."""
    stop()
    time.sleep(0.1)  # Let PWM settle before closing

    for pwm_obj in [rpwm_pwm, lpwm_pwm]:
        try:
            pwm_obj.stop()
        except OSError as e:
            print(f"Warning: PWM stop error (ignored): {e}")

    try:
        GPIO.cleanup()
    except OSError as e:
        print(f"Warning: GPIO cleanup error (ignored): {e}")

try:
    print("Motor forward")
    forward(70)
    time.sleep(2)

    print("Motor backward")
    backward(50)
    time.sleep(2)

    print("Stop motor")
    stop()

finally:
    safe_cleanup()