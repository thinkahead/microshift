import os
import time
from sense_hat import SenseHat
from influxdb import InfluxDBClient

INFLUXDB_ADMIN_USER=os.getenv("INFLUXDB_ADMIN_USER",default="admin")
INFLUXDB_ADMIN_PASSWORD=os.getenv("INFLUXDB_ADMIN_PASSWORD",default="admin")
username=os.getenv("username",default="admin")
influx_client = InfluxDBClient('influxdb-service', 8086, username=INFLUXDB_ADMIN_USER, password=INFLUXDB_ADMIN_PASSWORD, database='balena-sense')
influx_client.create_database('balena-sense')

sense = SenseHat()

sense.clear()
sense.load_image("balena.png")
time.sleep(2)
sense.show_message("balena")

count = 0

while 1:
    measurements = [
        {
            'measurement': 'temperature',
            'fields': {
                'value': float(sense.temperature)
            }
        }
    ]

    measurements.extend([
        {
            'measurement': 'humidity',
            'fields': {
                'value': float(sense.humidity)
            }
        }
    ])

    measurements.extend([
        {
            'measurement': 'pressure',
            'fields': {
                'value': float(sense.pressure)
            }
        }
    ])

    sense.set_pixel(0, count, 0, 255, 0)
    count = count+1
    if count == 8:
        count = 0
    sense.set_pixel(0, count, 0, 0, 0)
    influx_client.write_points(measurements)
    time.sleep(10)
