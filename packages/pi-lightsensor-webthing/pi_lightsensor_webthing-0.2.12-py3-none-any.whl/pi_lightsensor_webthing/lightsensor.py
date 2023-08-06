import logging
import board
import adafruit_bh1750
from threading import Thread
from time import sleep


class LightSensor:

    def __init__(self):
        self.measures = list()
        i2c = board.I2C()
        self.sensor = adafruit_bh1750.BH1750(i2c)
        logging.info("light sensor connected")

    def listen(self, listener):
        Thread(target=self.__listen, args=(listener,), daemon=True).start()

    def __listen(self, listener):
        loop = 0
        while True:
            try:
                self.measures.append(self.sensor.lux)
                while len(self.measures) > 5:
                    self.measures.pop(0)
                loop +=1
                if loop > 5:
                    loop = 0
                    median = self.measures[int(len(self.measures) * 0.5)]
                    listener(int(median))
            except Exception as e:
                print("error occurred", e)
            sleep(1)