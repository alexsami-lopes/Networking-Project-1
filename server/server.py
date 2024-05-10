import socket
import threading
import time
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

class Broker:
    def __init__(self):
        self.header = 64
        self.format = 'utf-8'
        self.temperature_request = "GET_TEMPERATURE"
        self.vent_status_request = "GET_VENT_STATUS"
        self.vent_open_request = "GET_VENT_OPEN"
        self.vent_close_request = "GET_VENT_CLOSE"
        self.devices_current_id = 0
        self.devices = {} 
        self.ip = socket.gethostbyname(socket.gethostname())
        self.port = self.find_free_port(8061, 8070)
        self.disconnect_message = "!DISCONECT"
        self.device_connected_message = "!DEVICE_CONNECTED"
        self.dispositivo_address = "172.158.56.1:8061"
        self.device_tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.dispositivo_ip, self.dispositivo_port = self.parse_address(self.dispositivo_address)
        #self.start_udp_server()
        threading.Thread(target=self.start_udp_server).start()
        #input("Enter to start: ")
        #print(self.get_device_message_in_dictio(self.dispositivo_ip))
        
  
        
           
        

    def find_free_port(self, start_port, end_port):
        for port in range(start_port, end_port + 1):
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.bind(("", port))
                s.close()
                return port
            except:
                pass
        raise Exception("No free port available")
    
    def parse_address(self, address):
        parts = address.split(":")
        if len(parts) != 2:
            raise ValueError("Invalid address format. Use IP:Porta.")
        ip = parts[0]
        port = int(parts[1])
        return ip, port
    

    def send_tcp_message_to_device(self, msg):
        #print(f"[TCP SENT]")
        message = msg.encode(self.format)
        msg_lengh = len(message)
        send_lengh = str(msg_lengh).encode(self.format)
        send_lengh += b' ' * (self.header - len(send_lengh))
        self.device_tcp_socket.send(send_lengh)
        self.device_tcp_socket.send(message)
        if message == self.disconnect_message:
            print(f"[DEVICE DISCONNECTED]")

    def start_udp_server(self):
        self.server_udp_socket.bind((self.ip, self.port+1))
        print(f"[STARTING] Server is running on {self.ip}:{self.port}")

        while True:
            data, address = self.server_udp_socket.recvfrom(1024)
            threading.Thread(target=self.handle_device, args=(data, address)).start()


    def handle_device(self, data, address):
        msg = data.decode(self.format)
        device_name = f"device{threading.active_count()}"
        self.set_message_to_device_in_dictio(address[0], msg)

        if msg == self.device_connected_message:
            print(f"[NEW DEVICE] {address[0]} connected!")
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 2}")
            self.add_device_in_dictio(address[0])
            self.device_tcp_socket.connect((address[0], self.port))
            self.request_temperature_to_device(address[0])
        elif msg == self.disconnect_message:
            self.remove_device_in_dictio(address)
            print(f"[DISCONNECT] {address[0]} disconnected!")  
        #input("Enter to start: ")
        #print(self.get_device_message_in_dictio(address[0]))              
        
    def make_request_to_device(self, device_ip, message_request):
        try:

            device_name = self.find_device_by_ip_in_dictio(device_ip)
            if device_name:
                self.send_tcp_message_to_device(message_request)

        except Exception as e:
            print(f"Error requesting {message_request} from device: {e}")
            return "N/A"
        
    def add_device_in_dictio(self, address):
        self.devices_current_id += 1
        self.devices[f"device{self.devices_current_id}"] = {"ip": address, "message": None}

    def remove_device_in_dictio(self, device_name):
        if device_name in self.devices:
            del self.devices[device_name]

    def find_device_by_ip_in_dictio(self, ip_address):
        for device_name, device_info in self.devices.items():
            if ip_address == device_info["ip"]:
                return device_name
        return None  # Retorna None se o endereço IP não for encontrado

    def set_message_to_device_in_dictio(self, ip_address, message):
        device_name = self.find_device_by_ip_in_dictio(ip_address)
        if device_name:
            self.devices[device_name]["message"] = message


    def get_device_message_in_dictio(self, ip_address):
        for device_name, device_info in self.devices.items():
            if ip_address == device_info["ip"]:
                message = device_info["message"]
                return ("[" + ip_address + "] " + message)
            
    def request_temperature_to_device(self, device_ip):
        try:
            self.send_tcp_message_to_device(self.temperature_request)

        except Exception as e:
            print(f"Error requesting Temperature from device: {e}")
            return "N/A"
    def request_vent_status_to_device(self, device_ip):
        try:
            self.send_tcp_message_to_device(self.vent_status_request)

        except Exception as e:
            print(f"Error requesting Temperature from device: {e}")
            return "N/A"
    def request_vent_open_to_device(self, device_ip):
        try:
            self.send_tcp_message_to_device(self.vent_open_request)

        except Exception as e:
            print(f"Error requesting Temperature from device: {e}")
            return "N/A"
    def request_vent_close_to_device(self, device_ip):
        try:
            self.send_tcp_message_to_device(self.vent_close_request)

        except Exception as e:
            print(f"Error requesting Temperature from device: {e}")
            return "N/A"
broker = Broker()        
@app.route('/temperature/<device_ip>', methods=['GET'])
def get_temperature(device_ip):
    # Aqui você retorna a temperatura atual, pode adaptar conforme necessário
    broker.request_temperature_to_device(device_ip)
    temperature = broker.get_device_message_in_dictio(device_ip)
    return temperature, 200, {'Content-Type': 'text/plain'}
 
@app.route('/vent-status/<device_ip>', methods=['GET'])
def get_vent_status(device_ip):
    # Aqui você retorna o status da escotilha, pode adaptar conforme necessário
    broker.request_vent_status_to_device(device_ip)
    vent_status = broker.get_device_message_in_dictio(device_ip)
    return vent_status, 200, {'Content-Type': 'text/plain'}

@app.route('/vent-open/<device_ip>', methods=['GET'])
def get_vent_open(device_ip):
    # Aqui você abre a escotilha, pode adaptar conforme necessário
    broker.request_vent_open_to_device(device_ip)
    vent_status = broker.get_device_message_in_dictio(device_ip)
    return vent_status, 200, {'Content-Type': 'text/plain'}

@app.route('/vent-close/<device_ip>', methods=['GET'])
def get_vent_close(device_ip):
    # Aqui você fecha a escotilha, pode adaptar conforme necessário
    broker.request_vent_close_to_device(device_ip)
    vent_status = broker.get_device_message_in_dictio(device_ip)
    return vent_status, 200, {'Content-Type': 'text/plain'}

if __name__ == "__main__":
    
    app.run(host='0.0.0.0', port=9000)
