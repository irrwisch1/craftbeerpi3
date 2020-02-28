import time
from thread import start_new_thread
from modules import cbpi
import os

PWM_PATH = '/sys/class/pwm/'

class Buzzer(object):

    sound = ["H", 0.1, "L", 0.1, "H", 0.1, "L", 0.1, "H", 0.1, "L"]
    def __init__(self, pwm, pwmchip, beep_level):
        try:
            cbpi.app.logger.info("INIT BUZZER PWMCHIP %s PWM %s" % (pwmchip, pwm))
            #self.gpio = int(gpio)
            self.pwmchip=int(pwmchip)
            self.pwm=int(pwm)
            self.beep_level = beep_level

            if not os.path.exists(PWM_PATH + ('pwmchip%d/pwm%d' % (self.pwmchip, self.pwm))):
                with open(PWM_PATH + ('pwmchip%d/export' % self.pwmchip), 'w') as fp:
                    fp.write(str(pwm))

	    with open(PWM_PATH + ('pwmchip%d/pwm%d/period' % (self.pwmchip, self.pwm)), 'w') as fp:
                fp.write(str(1000000))

	    with open(PWM_PATH + ('pwmchip%d/pwm%d/duty_cycle' % (self.pwmchip, self.pwm)), 'w') as fp:
                fp.write(str(300000))

 
            self.state = True
            cbpi.app.logger.info("BUZZER SETUP OK")
        except Exception as e:
            cbpi.app.logger.error("BUZZER EXCEPTION %s" % str(e))
            self.state = False

    def beep(self):
        if self.state is False:
            cbpi.app.logger.error("BUZZER not working")
            return

        def play(sound):
            try:
                for i in sound:
                    if (isinstance(i, str)):
                        if i == "H" and self.beep_level == "HIGH":
                           # GPIO.output(int(self.gpio), GPIO.HIGH)
	                    with open(PWM_PATH + ('pwmchip%d/pwm%d/enable' % (self.pwmchip, self.pwm)), 'w') as fp:
                                fp.write('1')
                        elif i == "H" and self.beep_level != "HIGH":
                           # GPIO.output(int(self.gpio), GPIO.LOW)
	                    with open(PWM_PATH + ('pwmchip%d/pwm%d/enable' % (self.pwmchip, self.pwm)), 'w') as fp:
                                fp.write('0')
                        elif i == "L" and self.beep_level == "HIGH":
                           # GPIO.output(int(self.gpio), GPIO.LOW)
	                    with open(PWM_PATH + ('pwmchip%d/pwm%d/enable' % (self.pwmchip, self.pwm)), 'w') as fp:
                                fp.write('0')
                        else:
                            #GPIO.output(int(self.gpio), GPIO.HIGH)
	                    with open(PWM_PATH + ('pwmchip%d/pwm%d/enable' % (self.pwmchip, self.pwm)), 'w') as fp:
                                fp.write('1')
                    else:
                        time.sleep(i)
            except Exception as e:
                pass

        start_new_thread(play, (self.sound,))

@cbpi.initalizer(order=1)
def init(cbpi):
    cbpi.app.logger.info("INIT buzz")
    pwmchip = cbpi.get_config_parameter("buzzer_pwmchip", 0)
    pwm = cbpi.get_config_parameter("buzzer_pwm", 0)
    beep_level = cbpi.get_config_parameter("buzzer_beep_level", "HIGH")

    cbpi.buzzer = Buzzer(pwm, pwmchip, beep_level)
    cbpi.beep()
    cbpi.app.logger.info("INIT OK")
