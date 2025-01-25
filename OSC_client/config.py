import os
from pythonosc import udp_client

OUTPUT_DIR = "C:\\Users\\PC\\Desktop\\record"

def setup_default_device():
    clients = {}
    device_name = "device1"
    clients[device_name] = udp_client.SimpleUDPClient('127.0.0.1', 8000)
    return clients