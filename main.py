#!/home/nikhila/Desktop/UsbLedMqttRelay/env/bin python3

# MQTT
import paho.mqtt.client as mqtt

# running uhubctl commands
import subprocess

# this is the ip address of the mqtt broker that you are using
broker_address = "broker.emqx.io"
# this is the port that you use to access the mqtt broker
# @ above ip address over a websocket this should probably be 8080
# @ tcp is 1883
broker_port = 1883
client_id = "e8401a08-37ef-47ef-81c9-31e8177f1c70-usb-led-relay"
command_topic = "slime-mould-stock-monitor/led_relay/command"
will_topic = "slime-mould-stock-monitor/led_relay/status"

#### Methods
def on_connect(client, userdata, connect_flags, reason_code, properties):
    if reason_code == 0:
        print(f" ∟ Connected to {broker_address}:{broker_port} with reason: {reason_code}")
        print("Now listening...")
    else:
        print(f" ∟ Failed to connect to {broker_address}:{broker_port} with reason: {reason_code}")
    
    # on reconnect we should resubscribe to the topic sending commands to the relay
    client.subscribe(command_topic)
    
def on_message(client, userdata, msg):
    print(f"{msg.topic} {msg.payload}")
    payload_str = msg.payload.decode("utf-8")
    # if msg.payload == "on" turn on usb ports
    # if msg.payload == "off", otherwise turn them off
    if msg.topic == command_topic:
        if payload_str == "on":
            print(" ∟ Received on, turning USB ports on.")
            subprocess.run(["sudo", "uhubctl", "-l", "1-1", "-p", "2", "-a", "on"], check=True)
        elif payload_str == "off":
            print(" ∟ Received off, turning USB ports off.")
            subprocess.run(["sudo", "uhubctl", "-l", "1-1", "-p", "2", "-a", "off"], check=True)

#### MAIN ##### 
if __name__=='__main__':
    print("Starting MQTT client...")
    mqttc = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2, client_id=client_id, clean_session=True)
    mqttc.on_connect = on_connect
    mqttc.on_message = on_message
    mqttc.will_set(will_topic, b'{"status": "Off"}')
    
    print(" ∟ Started.")
    print("Attempting to connect to MQTT broker...")
    
    mqttc.connect(host=broker_address, port=broker_port, keepalive=100)


    mqttc.loop_forever()
    
    


    