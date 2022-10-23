# MQTT Garage Door opener for the Raspberry Pi Pico 

This project allows for you to create a garage door button within Home Assistant using MQTT. I have a garage door which only has a single trigger for open/close (Isomatic 500) and so I've therefore kept it very simple.

I used a Raspberry Pi Pico W and a single channel relay which you can get from here: https://thepihut.com/products/single-channel-relay-for-raspberry-pi-pico 

The specifications and instructions for the relay can be found here: https://learn.sb-components.co.uk/Pico-Single-Channel-Relay-Hat

I've used the Micropython library mqtt_as from here: https://github.com/peterhinch/micropython-mqtt/tree/master/mqtt_as This file should be placed in the root filesystem of the Pico as mqtt_as.py

The MQTT messages will be sent to the topic /garage/door/button/trigger from Home Assisant and I've also included an availability topic and also send the Pico's temperature to garage/door/button/available and garage/door/button/temp respectively.

From there, within Home Assistant, you can set up a button using the following in configuration.yaml:

     mqtt:
        button:
          - unique_id: garage_door_button_trigger
            name: "Garage Door Button"
            command_topic: "garage/door/button/trigger"
            payload_press: "trigger"
            availability:
              - topic: "garage/door/button/available"
            qos: 0
            retain: false
            entity_category: "config"
         sensor:
            - name: "Garage Temperature"
              state_topic: "garage/door/button/temp"
              unit_of_measurement: "°C"

From there, you should be able to edit your dashboard and add a card for the entity with the name: "Garage Door Button"
