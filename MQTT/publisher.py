import time
import argparse
import io

import psutil
import paho.mqtt.client as mqtt

def main(args): # args: ip, port, file location 
    # Establish connection to mqtt broker
    client = mqtt.Client()
    client.connect(host=args['ip'], port=args['port'])
    client.loop_start()

    # Intervally send topic message
    count = 0
    try:
        while True:
            count += 1
            # Fill the payload
            f=open(f"./input/in{count % 3}.png", 'rb')
            fio = io.BytesIO()
            # print(type(fio))
            fileContent = f.read()
            buf = io.BytesIO(fileContent)
            # print(type(buf))
            byteArr = bytearray(buf.read())
            # Publish the message to topic
            client.publish(topic="png", payload=byteArr)
            time.sleep(1)
    except KeyboardInterrupt as e:
        client.loop_stop()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip",
                        default="localhost",
                        help="service ip of MQTT broker")
    parser.add_argument("--port",
                        default=1883,
                        type=int,
                        help="service port of MQTT broker")
    args = vars(parser.parse_args())
    main(args)
