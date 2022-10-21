import rp2
import machine
import utime
import network
from mqtt_as import MQTTClient, config
import uasyncio as asyncio

#WiFi connection
SERVER = 'server name or IP'
USERNAME = 'MQTT broker username'
PASSWORD = 'MQTT broker password'
SSID = 'WiFi SSID'
WIFIPW = 'WiFi Password'

#temp sensor
sensor_temp = machine.ADC(4)
conversion_factor = 3.3 / (65535)
#onboard LED
led = machine.Pin('LED', machine.Pin.OUT)
relay1 = machine.Pin(6, machine.Pin.OUT)

#this is us acting upon a message being pushed to the pico from home assistant
def callback(topic, msg, retained):
    print((topic, msg, retained))
    if msg == "trigger":
        led.on()
        relay1(1)
        utime.sleep(1)
        relay1(0)
        utime.sleep(1)
        led.off()

#the topic for which we are subscribing to above
async def conn_han(client):
    await client.subscribe('garage/door/button/trigger', 1)

#the main thread for publishing data to the topic
async def main(client):
    await client.connect()
    while True:
        reading = sensor_temp.read_u16() * conversion_factor
        temperature = round(27 - (reading - 0.706)/0.001721, 2)
        temp = str(temperature)
        pico_state = "online"
        await client.publish(b'garage/door/button/temp', temp)
        await client.publish(b'garage/door/button/available', pico_state)
        await asyncio.sleep(30)
 
#config
config['subs_cb'] = callback
config['connect_coro'] = conn_han
config['server'] = SERVER
config['user'] = USERNAME
config['password'] = PASSWORD
config['ssid'] = SSID
config['wifi_pw'] = WIFIPW 
 
MQTTClient.DEBUG = True  # Optional: print diagnostic messages
client = MQTTClient(config)
try:
    asyncio.run(main(client))
finally:
    client.close()  # Prevent LmacRxBlk:1 errors


