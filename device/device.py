import socket
import threading
import time

class Dispositivo:
    def __init__(self):
        self.header = 64
        self.format = 'utf-8'
        self.disconnect_message = "!DISCONECT"
        self.device_connected_message = "!DEVICE_CONNECTED"
        self.ip = socket.gethostbyname(socket.gethostname())
        self.vent_status = "Openned"
        self.rising = True
        self.broker_address = input("Digite o endereço IP do Servidor (no formato IP:Porta): ")
        self.broker_ip, self.broker_port = self.parse_address(self.broker_address)
        self.port = self.broker_port
        self.temperature = 18
        self.start_temperature_thread()
        self.client_udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.send_udp_message_to_server(self.device_connected_message)
        self.server_tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.start_tcp_server()

    
    def parse_address(self, address):
        parts = address.split(":")
        if len(parts) != 2:
            raise ValueError("Invalid address format. Use IP:Porta.")
        ip = parts[0]
        port = int(parts[1])
        return ip, port

    def start_temperature_thread(self):
        #threading.Thread(target=self.update_temperature).start()
        threading.Thread(target=self.control_temperature).start()

    def update_temperature(self):
        
        
        while True:
            #print(f'Temperatura atual: {temperatura}°C')
            time.sleep(1)
            
            if self.rising:
                self.temperature += 0.2
                if self.temperature >= 32:
                    self.temperature = False
            else:
                self.temperature -= 0.2
                if self.temperature <= 10:
                    self.temperature = True
    def control_temperature(self):
        while True:
            #print(f'Temperatura atual: {self.temperatura}°C')
            time.sleep(1)

            if self.vent_status == "Openned":
                self.temperature -= 0.1
                if self.temperature <= 17:
                    self.vent_status = "Closed"
            else:
                self.temperature += 0.1
                if self.temperature >= 32:
                    self.vent_status = "Openned"

    def start_tcp_server(self):
        self.server_tcp_socket.bind((self.ip, self.port))
        self.server_tcp_socket.listen(5)
        print(f"[STARTING] Server is running on {self.ip}:{self.port}")

        while True:
            connection, address = self.server_tcp_socket.accept()
            threading.Thread(target=self.handle_client, args=(connection, address)).start()


    def handle_client(self, conn, addr):

        connected = True
        while connected:
            try:
                msg_length = conn.recv(self.header).decode(self.format)
                if msg_length:
                    msg_length = int(msg_length)
                    msg = conn.recv(self.header).decode(self.format)
                    if msg == self.disconnect_message:
                        connected = False
                    elif msg == "GET_TEMPERATURE":
                        #formated_temp = str("{:.1f}".format(self.temperature)) + "°C"
                        formated_temp = str(round(self.temperature, 1)) + " C"
                        self.send_udp_message_to_server(formated_temp)
                    elif msg == "GET_VENT_STATUS":
                        self.send_udp_message_to_server(self.vent_status)
                    elif msg == "GET_VENT_OPEN":
                        self.vent_status = "Openned"
                        self.send_udp_message_to_server(self.vent_status)
                    elif msg == "GET_VENT_CLOSE":
                        self.vent_status = "Closed"  
                        self.send_udp_message_to_server(self.vent_status)  
                    #print(f"[{addr}] {msg}")

            except Exception as e:
                print(f"Error handling client [{addr}]: {e}")
                break


    def send_tcp_message_to_server(self, msg):
        message = msg.encode(self.format)
        msg_lengh = len(message)
        send_lengh = str(msg_lengh).encode(self.format)
        send_lengh += b' ' * (self.header - len(send_lengh))
        self.device_tcp_socket.send(send_lengh)
        self.device_tcp_socket.send(message)
        if message == self.disconnect_message:
            print(f"[DEVICE DISCONNECTED]")

    def send_udp_message_to_server(self, msg):
        message = msg.encode(self.format)
        self.client_udp_socket.sendto(message, (self.broker_ip, self.broker_port+1))
        if msg == self.disconnect_message:
            print("[DEVICE DISCONNECTED]")


if __name__ == "__main__":
    dispositivo = Dispositivo()
