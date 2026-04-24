import Jetson.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

R_EN = 38
L_EN = 37
RPWM = 33
LPWM = 15

GPIO.setup(R_EN, GPIO.OUT)
GPIO.setup(L_EN, GPIO.OUT)
GPIO.setup(RPWM, GPIO.OUT)
GPIO.setup(LPWM, GPIO.OUT)

try:
    print("Enabling both EN pins HIGH...")
    GPIO.output(R_EN, GPIO.HIGH)
    GPIO.output(L_EN, GPIO.HIGH)
    
    print("Setting LPWM HIGH (full forward)...")
    GPIO.output(LPWM, GPIO.HIGH)
    GPIO.output(RPWM, GPIO.LOW)
    time.sleep(3)
    
    print("Stopping...")
    GPIO.output(LPWM, GPIO.LOW)
    GPIO.output(RPWM, GPIO.LOW)

finally:
    GPIO.cleanup()