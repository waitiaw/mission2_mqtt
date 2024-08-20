import paho.mqtt.client as mqtt
import json


# 브로커에 연결되면 호출되는 콜백 함수
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected OK")
        # 브로커에 연결되면 "common" 토픽을 구독
        client.subscribe("common")
    else:
        print("Bad connection Returned code=", rc)


# 브로커 연결이 끊어지면 호출되는 콜백 함수
def on_disconnect(client, userdata, flags, rc=0):
    print("Disconnected with result code " + str(rc))


# 메시지가 발행되면 호출되는 콜백 함수
def on_publish(client, userdata, mid):
    print("Message Published with mid= ", mid)


# 메시지를 수신하면 호출되는 콜백 함수
def on_message(client, userdata, msg):
    # 수신한 메시지 출력
    print("Received message: ", msg.topic, str(msg.payload.decode("utf-8")))


# 새로운 클라이언트 생성
client = mqtt.Client()

# 콜백 함수 설정
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_publish = on_publish
client.on_message = on_message

# 브로커에 연결
client.connect('localhost', 1883)
client.loop_start()

# 사용자로부터 입력을 받아서 "common" 토픽으로 메시지 발행
try:
    while True:
        message = input("Enter message to publish: ")
        if message.lower() == 'exit':
            break
        client.publish('common', json.dumps({"message": message}), 1)
except KeyboardInterrupt:
    pass

# 루프 종료 및 연결 종료
client.loop_stop()
client.disconnect()