import argparse
import logging
import ssl
import json
import time
import datetime

import paho.mqtt.client as mqtt
import freebox_v5_status.freeboxstatus


parser = argparse.ArgumentParser()
parser.add_argument("server", help="MQtt server to connect to.")
parser.add_argument("--user", help="MQtt username.")
parser.add_argument("--password", help="MQtt password.")
parser.add_argument("--interval", help="Check interval default 60s.", type=int, default=60)
parser.add_argument("--tls12", help="use TLS 1.2", dest="tls",
                    action="store_const", const=ssl.PROTOCOL_TLSv1_2)
parser.add_argument("--cacert", help="CA Certificate, default /etc/ssl/certs/ca-certificates.crt.",
                    default="/etc/ssl/certs/ca-certificates.crt")
parser.add_argument("--log", help="Logging level, default INFO",
                    default="INFO")
args = parser.parse_args()

# Convert to upper case to allow the user to
# specify --log=DEBUG or --log=debug
numeric_level = getattr(logging, args.log.upper(), None)
if not isinstance(numeric_level, int):
    raise ValueError("Invalid log level: {0}".format(args.log))
logging.basicConfig(level=numeric_level)

_LOGGER = logging.getLogger(__name__)


port_mqtt = 1883
client = mqtt.Client()
# client.on_log = on_log
if args.user:
    client.username_pw_set(args.user, args.password)
if args.tls:
    client.tls_set(args.cacert, tls_version=args.tls)
    port_mqtt = 8883

client.will_set("freebox/reading", "OFF", 1, True)

def on_connect(the_client, userdata, flags, rc):
    if rc == mqtt.CONNACK_ACCEPTED:
        client.publish("freebox/reading", "ON", 1, True)

client.on_connect = on_connect

client.connect(args.server, port_mqtt)
client.loop_start()

fbx = freebox_v5_status.freeboxstatus.FreeboxStatus()

class CustomEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime.timedelta):
            return obj.total_seconds()

        return json.JSONEncoder.default(self, obj)


# Main loop
while True:
    fbx.update()
    client.publish("freebox/status", json.dumps(fbx.status, cls=CustomEncoder),  retain=True)
    time.sleep(args.interval)
