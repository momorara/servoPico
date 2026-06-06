import mqtt_file
import mqtt_pub

topic = mqtt_file.topic_get()
print(topic)

data = -5
mqtt_pub.mqtt_send(topic,data)