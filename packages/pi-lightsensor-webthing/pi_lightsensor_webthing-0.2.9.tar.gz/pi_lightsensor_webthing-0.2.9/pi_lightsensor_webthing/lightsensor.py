import logging
import board
import adafruit_bh1750
from threading import Thread
from time import sleep


class LightSensor:

    def __init__(self, measure_period: int):
        self.measure_period = measure_period
        i2c = board.I2C()
        self.sensor = adafruit_bh1750.BH1750(i2c)
        logging.info("light sensor connected")

    def listen(self, listener):
        Thread(target=self.__listen, args=(listener,), daemon=True).start()

    def __listen(self, listener):
        while True:
            try:
                listener(int(self.sensor.lux))
            except Exception as e:
                print("error occurred", e)
            sleep(self.measure_period)

