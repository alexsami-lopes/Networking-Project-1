# Networking Project 1: IoT
## Vent Control System
This software simulates a device equipped with a temperature sensor that controls a roof vent in a greenhouse environment. It operates through a broker-client architecture, where the simulated device communicates with a broker. The client, in turn, interacts with the vent, via the broker, managing its operations based on temperature readings received from the device. Additionally, the system provides real-time temperature data in Celsius (°C) to monitor the greenhouse environment effectively. The device communicates with the broker via TCP/IP using sockets, while the broker communicates with the client via REST.
