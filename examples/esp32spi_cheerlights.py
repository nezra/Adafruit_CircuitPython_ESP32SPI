
import utime

#uPy libraries
from pyb import Pin, SPI
import esp32spi
import esp32spi_wifimanager

# Get wifi details and more from a secrets.py file
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

print("ESP32 SPI webclient test")

DATA_SOURCE = "https://api.thingspeak.com/channels/1417/feeds.json?results=1"
DATA_LOCATION = ["feeds", 0, "field2"]

esp32_cs = Pin("P3", Pin.OUT_OD) 
esp32_ready = Pin("P7", Pin.IN) 
esp32_reset = Pin("P8", Pin.OUT_PP) 
spi = SPI(2,SPI.MASTER,baudrate=8000000,polarity=0,phase=0) 
esp = esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset,debug=True) 

wifi = esp32spi_wifimanager.ESPSPI_WiFiManager(esp, secrets)

# we'll save the value in question
last_value = value = None
while True:
    try:
        print("Fetching json from", DATA_SOURCE)
        response = wifi.get(DATA_SOURCE)
        #print(response)# .json())
        value = response.json()
        for key in DATA_LOCATION:
            value = value[key]
            print(value)
        response.close()
    except (ValueError, RuntimeError) as e:
        print("Failed to get data, retrying\n", e)
        wifi.reset()
        continue

    if not value:
        continue
    if last_value != value:
        color = int(value[1:], 16)
        red = color >> 16 & 0xFF
        green = color >> 8 & 0xFF
        blue = color& 0xFF
        gamma_corrected = fancy.gamma_adjust(fancy.CRGB(red, green, blue)).pack()

        pixels.fill(gamma_corrected)
        last_value = value
    response = None
    utime.sleep(60)
