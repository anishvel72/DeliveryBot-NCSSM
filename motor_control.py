import Jetson.GPIO as GPIO
import time

# Pin assignments
RPWM = 2
LPWM = 1
R_EN = 38
L_EN = 37

# Setup
GPIO.setmode(GPIO.BOARD)
GPIO.setup(RPWM, GPIO.OUT)
GPIO.setup(LPWM, GPIO.OUT)
GPIO.setup(R_EN, GPIO.OUT)
GPIO.setup(L_EN, GPIO.OUT)

# Create PWM instances (frequency in Hz)
rpwm_pwm = GPIO.PWM(RPWM, 1000)
lpwm_pwm = GPIO.PWM(LPWM, 1000)
rpwm_pwm.start(0)
lpwm_pwm.start(0)

def spin_motor(voltage, ms, direction="forward"):
    """
    Spins the motor at a given voltage level for a set duration.

    Args:
        voltage (float): 0.0 to 1.0 — represents duty cycle (% of max voltage)
        ms (int): Duration in milliseconds to spin
        direction (str): "forward" or "backward"
    """
    duty_cycle = max(0.0, min(1.0, voltage)) * 100  # clamp and scale to 0-100

    # Enable both channels
    GPIO.output(R_EN, GPIO.HIGH)
    GPIO.output(L_EN, GPIO.HIGH)

    if direction == "forward":
        rpwm_pwm.ChangeDutyCycle(duty_cycle)
        lpwm_pwm.ChangeDutyCycle(0)
    elif direction == "backward":
        rpwm_pwm.ChangeDutyCycle(0)
        lpwm_pwm.ChangeDutyCycle(duty_cycle)

    time.sleep(ms / 1000.0)  # convert ms to seconds

    # Stop motor
    rpwm_pwm.ChangeDutyCycle(0)
    lpwm_pwm.ChangeDutyCycle(0)
    GPIO.output(R_EN, GPIO.LOW)
    GPIO.output(L_EN, GPIO.LOW)


# --- Execute ---
spin_motor(voltage=0.75, ms=2000, direction="forward")

# Cleanup
rpwm_pwm.stop()
lpwm_pwm.stop()
GPIO.cleanup()