#!/usr/bin/python

from Adafruit_PWM_Servo_Driver import PWM
import time
import sys
import random
import pi3d

channel_lid = 0
channel_press = 1
channel_swivel = 2

servo_openLid = 140
servo_closeLid = 300
servo_pressMin = 150
servo_pressMax = 500
servo_swivelMin = 330
servo_swivelMax = 550

pwm_frequency = 60

# Initialise the PWM device using the default address
pwm = PWM(0x40)
# Note if you'd like more debug output you can instead run:
# pwm = PWM(0x40, debug=True)
pwm.setPWMFreq(pwm_frequency)  # Set frequency to 60 Hz


def setServoPulse(pwm, channel, pulse):
    pulseLength = 1000000                   # 1,000,000 us per second
    pulseLength /= 60                       # 60 Hz
    print("%d us per period" % pulseLength)
    pulseLength /= 4096                     # 12 bits of resolution
    print("%d us per bit" % pulseLength)
    pulse *= 1000
    pulse /= pulseLength
    pwm.setPWM(channel, 0, pulse)


def move_hand_out_of_way():
    pwm.setPWM(channel_press, 0, 450)
    pwm.setPWM(channel_swivel, 0, 450)


def press_keys(location=330):
    pwm.setPWM(channel_press, 0, 450)
    pwm.setPWM(channel_swivel, 0, location)
    time.sleep(0.25)
    pwm.setPWM(channel_press, 0, 480)
    time.sleep(0.25)
    pwm.setPWM(channel_press, 0, 450)


def close_lid():
    pwm.setPWM(channel_lid, 0, servo_closeLid)


def open_lid():
    pwm.setPWM(channel_lid, 0, servo_openLid-20)
    time.sleep(0.5)
    pwm.setPWM(channel_lid, 0, servo_openLid+40)

def angry_1():
    for i in range(random.randint(3,5)):
       press_keys(random.randint(-20,20) + 330)
    
    time.sleep(1)
    move_hand_out_of_way()
    time.sleep(1)
    # close_lid()

def happy_1():
    move_hand_out_of_way()
    open_lid()

def old_main():
    if len(sys.argv) < 3:
	print("angry")
        angry_1()
        time.sleep(1)
        happy_1()
	time.sleep(1)
        return
    elif len(sys.argv) != 3:
        print("Additional Arguments required\n\t[channel] [pulseLength]")
        return

    setServoPulse(pwm, int(sys.argv[1]), int(sys.argv[2]))
    time.sleep(1)

def main():
    while(1):
    	if (sys.stdin.readline() == 'a\n'):
		angry_1()
	elif (sys.stdin.readline() == 'b\n'):
		close_lid()
	elif (sys.stdin.readline() == 'c\n'):
		open_lid()
	

if __name__ == '__main__':
    main()


