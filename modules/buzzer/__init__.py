import time
from thread import start_new_thread
from modules import cbpi

try:
    import RPi.GPIO as GPIO
    import wiringpi
except Exception as e:
    pass

class Buzzer(object):

    sound = ["H", 0.1, "L", 0.1, "H", 0.1, "L", 0.1, "H", 0.1, "L"]
    def __init__(self, gpio, beep_level):
        try:
            cbpi.app.logger.info("INIT BUZZER NOW GPIO%s" % gpio)
            #self.gpio = int(gpio)
            self.gpio=27
            self.beep_level = beep_level
            wiringpi.wiringPiSetup()
            wiringpi.softToneCreate(self.gpio)
            #GPIO.setmode(GPIO.BCM)
            #GPIO.setup(self.gpio, GPIO.OUT)
            self.state = True
            cbpi.app.logger.info("BUZZER SETUP OK")
        except Exception as e:
            cbpi.app.logger.info("BUZZER EXCEPTION %s" % str(e))
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
                            wiringpi.softToneWrite(self.gpio, 1000);
                        elif i == "H" and self.beep_level != "HIGH":
                           # GPIO.output(int(self.gpio), GPIO.LOW)
                            wiringpi.softToneWrite(self.gpio, 0);
                        elif i == "L" and self.beep_level == "HIGH":
                           # GPIO.output(int(self.gpio), GPIO.LOW)
                            wiringpi.softToneWrite(self.gpio, 0);
                        else:
                            #GPIO.output(int(self.gpio), GPIO.HIGH)
                            wiringpi.softToneWrite(self.gpio, 1000);
                    else:
                        time.sleep(i)
            except Exception as e:
                pass

        start_new_thread(play, (self.sound,))

@cbpi.initalizer(order=1)
def init(cbpi):
    gpio = cbpi.get_config_parameter("buzzer", 22)
    beep_level = cbpi.get_config_parameter("buzzer_beep_level", "HIGH")

    cbpi.buzzer = Buzzer(gpio, beep_level)
    cbpi.beep()
    cbpi.app.logger.info("INIT OK")
