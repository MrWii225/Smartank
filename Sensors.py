import time 
import board
import busio 
import digitalio 
from w1thermsensor import W1ThermSensor

from adafruit_mcp3xxx.mcp3008 import MCP3008, P0 
from adafruit_mcp3xxx.analog_in import AnalogIn
import adafruit_mcp3xxx.mcp3xxx as MCP # for P0, P1, etc.


# SPI and MCP3008 setup
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D8) #CE0
mcp = MCP3008(spi, cs)

# Use CH0 for the pH sensor
ph_channel = AnalogIn(mcp, P0)

#Temperature sensor setup
temp_sensor = W1ThermSensor()
temperature_c = temp_sensor.get_temperature()
temperature_f = (temperature_c * 9/5) + 32 

def voltage_to_ph(voltage):
    #Calibrate with calibration fluids
    ph = (7.78 * voltage - 8.54)
    return round(ph, 2)

while True:
    voltage = ph_channel.voltage
    raw_value = ph_channel.value 
    print(f"Temperature {temperature_f:.2f}")
    print(voltage_to_ph(voltage))
    print(f"Raw ADC Value: {raw_value}, Voltage: {voltage:.3f} V")
    time.sleep(1)




