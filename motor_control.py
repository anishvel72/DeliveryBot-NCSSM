import gpiod
import time
import os

# Hardware PWM sysfs paths
PWM_CHIP_RPWM = 2   # pin 32, pwm7
PWM_CHAN_RPWM = 0
PWM_CHIP_LPWM = 1   # pin 33, pwm5
PWM_CHAN_LPWM = 0

PERIOD_NS = 1_000_000  # 1kHz

# EN pins via libgpiod
R_EN_LINE = 38
L_EN_LINE = 37

def pwm_path(chip, channel):
    return f"/sys/class/pwm/pwmchip{chip}/pwm{channel}"

def pwm_export(chip, channel):
    export_path = f"/sys/class/pwm/pwmchip{chip}/export"
    if not os.path.exists(pwm_path(chip, channel)):
        with open(export_path, 'w') as f:
            f.write(str(channel))
    time.sleep(0.1)

def pwm_write(chip, channel, period_ns, duty_ns, enable=1):
    base = pwm_path(chip, channel)
    with open(f"{base}/period", 'w') as f:
        f.write(str(period_ns))
    with open(f"{base}/duty_cycle", 'w') as f:
        f.write(str(duty_ns))
    with open(f"{base}/enable", 'w') as f:
        f.write(str(enable))

def pwm_set_duty(chip, channel, duty_fraction):
    duty_ns = int(PERIOD_NS * max(0.0, min(1.0, duty_fraction)))
    base = pwm_path(chip, channel)
    with open(f"{base}/duty_cycle", 'w') as f:
        f.write(str(duty_ns))

# Setup EN pins
chip = gpiod.Chip('gpiochip0')
r_en = chip.get_line(R_EN_LINE)
l_en = chip.get_line(L_EN_LINE)
r_en.request(consumer="motor", type=gpiod.LINE_REQ_DIR_OUT)
l_en.request(consumer="motor", type=gpiod.LINE_REQ_DIR_OUT)

# Export and init PWM
pwm_export(PWM_CHIP_RPWM, PWM_CHAN_RPWM)
pwm_export(PWM_CHIP_LPWM, PWM_CHAN_LPWM)
pwm_write(PWM_CHIP_RPWM, PWM_CHAN_RPWM, PERIOD_NS, 0, enable=1)
pwm_write(PWM_CHIP_LPWM, PWM_CHAN_LPWM, PERIOD_NS, 0, enable=1)

def spin_motor(voltage, ms, direction="forward"):
    duty = max(0.0, min(1.0, voltage))

    r_en.set_value(1)
    l_en.set_value(1)

    if direction == "forward":
        pwm_set_duty(PWM_CHIP_RPWM, PWM_CHAN_RPWM, duty)
        pwm_set_duty(PWM_CHIP_LPWM, PWM_CHAN_LPWM, 0)
    elif direction == "backward":
        pwm_set_duty(PWM_CHIP_RPWM, PWM_CHAN_RPWM, 0)
        pwm_set_duty(PWM_CHIP_LPWM, PWM_CHAN_LPWM, duty)

    time.sleep(ms / 1000.0)

    pwm_set_duty(PWM_CHIP_RPWM, PWM_CHAN_RPWM, 0)
    pwm_set_duty(PWM_CHIP_LPWM, PWM_CHAN_LPWM, 0)
    r_en.set_value(0)
    l_en.set_value(0)

# --- Execute ---
spin_motor(voltage=0.75, ms=2000, direction="forward")

# Cleanup
pwm_write(PWM_CHIP_RPWM, PWM_CHAN_RPWM, PERIOD_NS, 0, enable=0)
pwm_write(PWM_CHIP_LPWM, PWM_CHAN_LPWM, PERIOD_NS, 0, enable=0)
r_en.set_value(0)
l_en.set_value(0)
chip.close()