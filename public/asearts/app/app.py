# import os
# import sys
# import subprocess
# import ctypes

# # Check if the script is running with administrator privileges
# def is_admin():
#     try:
#         # return ctypes.windll.shell32.IsUserAnAdmin()
#         return True
#     except:
#         return False

# # Function to check and install required modules
# def check_and_install_modules():
#     required_modules = [
#         'flask', 'psutil', 'requests', 'bs4', 'scapy', 'sqlite3'
#     ]
#     for module in required_modules:
#         try:
#             __import__(module)
#         except ImportError:
#             subprocess.check_call([sys.executable, '-m', 'pip', 'install', module])

# # Check and install required modules
# check_and_install_modules()

# if not is_admin():
#     print("This script requires administrator privileges. Please run as an administrator.")
#     ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
#     sys.exit()



# from flask import Flask, jsonify, request
# import psutil
# import os
# import sqlite3
# from datetime import datetime, timedelta
# import shutil
# from urllib.parse import urlparse
# import subprocess
# import shlex
# from scapy.all import sniff, IP, TCP, UDP
# from collections import Counter
# import socket
# import threading
# import requests
# from bs4 import BeautifulSoup
# from urllib.parse import urljoin

# app = Flask(__name__)

# def get_system_metrics():
#     memory = psutil.virtual_memory().percent
#     cpu = psutil.cpu_percent(interval=1)
#     network = psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv
#     return {'Memory': memory, 'CPU': cpu, 'Network': network}

# def get_chrome_history(start_date, end_date):
#     # Path to the Chrome history file
#     history_path = os.path.expanduser('~') + r"\AppData\Local\Google\Chrome\User Data\Default\History"

#     # Copying the file to a temporary location because the original file is locked by Chrome
#     tmp_history_path = os.path.expanduser('~') + r"\AppData\Local\Temp\chrome_history"
#     shutil.copy2(history_path, tmp_history_path)

#     # Connect to the history database
#     conn = sqlite3.connect(tmp_history_path)
#     cursor = conn.cursor()

#     # Query to get the URLs from the history file
#     query = "SELECT url, visit_count, last_visit_time FROM urls"
#     cursor.execute(query)

#     # Fetch all results
#     results = cursor.fetchall()

#     # Close the connection
#     conn.close()

#     # Convert Chrome's timestamp format to a readable format
#     def chrome_time_to_readable(chrome_time):
#         epoch_start = datetime(1601, 1, 1)
#         delta = timedelta(microseconds=chrome_time)
#         return epoch_start + delta

#     # Filter results based on the date range and extract domain names
#     history_list = []
#     for url, visit_count, last_visit_time in results:
#         readable_time = chrome_time_to_readable(last_visit_time)
#         if start_date <= readable_time <= end_date:
#             domain = urlparse(url).netloc
#             history_list.append({
#                 'url': url,
#                 'domain': domain,
#                 'visit_count': visit_count,
#                 'last_visit_time': readable_time
#             })

#     return history_list

# @app.route('/metrics', methods=['GET'])
# def metrics():
#     return jsonify(get_system_metrics())

# @app.route('/metrics2', methods=['GET'])
# def metrics2():
#     start_date_str = request.args.get('start_date')
#     start_time_str = request.args.get('start_time')
#     end_date_str = request.args.get('end_date')
#     end_time_str = request.args.get('end_time')

#     start_datetime_str = f"{start_date_str} {start_time_str}"
#     end_datetime_str = f"{end_date_str} {end_time_str}"

#     try:
#         start_date = datetime.strptime(start_datetime_str, "%d/%m/%Y %H:%M")
#         end_date = datetime.strptime(end_datetime_str, "%d/%m/%Y %H:%M")
#         history = get_chrome_history(start_date, end_date)
#         return jsonify(history)
#     except ValueError as e:
#         return jsonify({'error': str(e)})

# @app.route('/clean-temp-files', methods=['POST'])
# def clean_temp_files():
#     temp_dir = 'C:\Windows\Temp'  # Update this to the actual temporary directory path
#     deleted_files = []
#     skipped_files = []

#     for filename in os.listdir(temp_dir):
#         file_path = os.path.join(temp_dir, filename)
#         try:
#             if os.path.isfile(file_path):
#                 os.remove(file_path)
#                 deleted_files.append(filename)
#             elif os.path.isdir(file_path):
#                 shutil.rmtree(file_path)
#                 deleted_files.append(filename)
#             else:
#                 skipped_files.append(filename)
#         except Exception as e:
#             print(f"Error deleting {file_path}: {e}")
#             skipped_files.append(filename)
    
#     return jsonify({
#         'deleted': deleted_files,
#         'skipped': skipped_files
#     })



# current_directory = os.getcwd()  # Start in the current working directory

# @app.route('/execute-cmd', methods=['POST'])
# def execute_cmd():
#     global current_directory
#     data = request.get_json()
#     command = data.get('command')

#     try:
#         if command.startswith('cd '):
#             # Handle 'cd' command separately
#             new_directory = command[3:].strip()
#             new_directory_path = os.path.abspath(os.path.join(current_directory, new_directory))

#             if os.path.isdir(new_directory_path):
#                 current_directory = new_directory_path
#                 return jsonify({"output": f"Changed directory to {current_directory}"})
#             else:
#                 return jsonify({"output": f"No such directory: {new_directory}"}), 500
#         else:
#             # Execute other commands
#             process = subprocess.Popen(command, shell=True, cwd=current_directory, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
#             stdout, stderr = process.communicate()

#             if process.returncode == 0:
#                 return jsonify({"output": stdout})
#             else:
#                 return jsonify({"output": stderr}), 500
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500
    
# def get_storage_info():
#     usage = psutil.disk_usage('/')
#     total = usage.total / (1024 ** 3)  # Convert to GB
#     used = usage.used / (1024 ** 3)   
#     free = usage.free / (1024 ** 3)    
#     percent = usage.percent
    
#     return  {
#         "total": f"{total:.2f} GB",
#         "used": f"{used:.2f} GB",
#         "free": f"{free:.2f} GB",
#         "percent": f"{percent:.2f}%"
#     }

# @app.route('/storage', methods=['GET'])
# def storage_info():
#     return jsonify(get_storage_info())


# captured_packets = []

# def resolve_domain(ip):
#     try:
#         return socket.gethostbyaddr(ip)[0]
#     except socket.herror:
#         return "Unknown"

# def process_packet(packet):
#     global captured_packets

#     if packet.haslayer(IP):
#         src_ip = packet[IP].src
#         dst_ip = packet[IP].dst

#         if packet.haslayer(TCP):
#             src_port = packet[TCP].sport
#             dst_port = packet[TCP].dport
#             protocol = "TCP"
#         elif packet.haslayer(UDP):
#             src_port = packet[UDP].sport
#             dst_port = packet[UDP].dport
#             protocol = "UDP"
#         else:
#             src_port = "N/A"
#             dst_port = "N/A"
#             protocol = "Unknown"

#         src_site = resolve_domain(src_ip)
#         dst_site = resolve_domain(dst_ip)

#         packet_info = {
#             "src_site": src_site,
#             "src_ip": src_ip,
#             "src_port": src_port,
#             "dst_site": dst_site,
#             "dst_ip": dst_ip,
#             "dst_port": dst_port,
#             "protocol": protocol
#         }

#         captured_packets.append(packet_info)

# @app.route('/packets', methods=['GET'])
# def get_packets():
#     return jsonify(captured_packets)

# def sniff_packets(interface):
#     sniff(iface=interface, store=False, prn=process_packet)



# @app.route('/scrape', methods=['GET'])
# def scrape():
#     url = request.args.get('url')
#     try:
#         response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
#         response.raise_for_status()
#         soup = BeautifulSoup(response.content, 'html.parser')

#         # Extracting data
#         title = soup.title.string if soup.title else 'No title found'
#         headings = [h.get_text() for h in soup.find_all(['h1', 'h2', 'h3'])]
#         links = [{'href': a.get('href'), 'text': a.get_text()} for a in soup.find_all('a', href=True)]
#         meta_description = soup.find('meta', attrs={'name': 'description'})
#         description = meta_description['content'] if meta_description else 'No description found'
#         images = [urljoin(url, img.get('src')) for img in soup.find_all('img', src=True)]

#         data = {
#             'title': title,
#             'headings': headings,
#             'links': links,
#             'description': description,
#             'images': images,
#             'html': soup.prettify()
#         }
#         return jsonify(data)
#     except requests.exceptions.RequestException as e:
#         return jsonify({'error': str(e)}), 500
# # if __name__ == "__main__":
# #     interface = 'Wi-Fi'
# #     threading.Thread(target=sniff_packets, args=(interface,), daemon=True).start()
# #     app.run(port=5001, debug=True)

# if __name__ == '__main__':
#     interface = 'Wi-Fi'
#     threading.Thread(target=sniff_packets, args=(interface,), daemon=True).start()
#     app.run(host='0.0.0.0', port=5001, debug=True)





# /////////////////////////////////////////////////////////////////////new version/////////////////////////////////////////////////////////////////////////

import os
import sys
import subprocess
import ctypes

# Check if the script is running with administrator privileges
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except:
        return False

# Function to check and install required modules
def check_and_install_modules():
    required_modules = [
        'flask', 'psutil', 'requests', 'bs4', 'scapy'
    ]
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', module])

# Check and install required modules
check_and_install_modules()

if not is_admin():
    print("This script requires administrator privileges. Please run as an administrator.")
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    sys.exit()

from flask import Flask, jsonify, request
import psutil
import os
import sqlite3
from datetime import datetime, timedelta
import shutil
from urllib.parse import urlparse
import subprocess
from scapy.all import sniff, IP, TCP, UDP, conf
import socket
import threading
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

app = Flask(__name__)

def get_system_metrics():
    memory = psutil.virtual_memory().percent
    cpu = psutil.cpu_percent(interval=1)
    network = psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv
    return {'Memory': memory, 'CPU': cpu, 'Network': network}

def get_chrome_history(start_date, end_date):
    # Attempt to find the Chrome history file path
    try:
        history_path = find_chrome_history()
    except FileNotFoundError:
        return jsonify({'error': 'Chrome history file not found. Please check your Chrome installation path.'}), 500

    # Copying the file to a temporary location because the original file is locked by Chrome
    tmp_history_path = os.path.expanduser('~') + r"\AppData\Local\Temp\chrome_history"
    shutil.copy2(history_path, tmp_history_path)

    # Connect to the history database
    conn = sqlite3.connect(tmp_history_path)
    cursor = conn.cursor()

    # Query to get the URLs from the history file
    query = "SELECT url, visit_count, last_visit_time FROM urls"
    cursor.execute(query)

    # Fetch all results
    results = cursor.fetchall()

    # Close the connection
    conn.close()

    # Convert Chrome's timestamp format to a readable format
    def chrome_time_to_readable(chrome_time):
        epoch_start = datetime(1601, 1, 1)
        delta = timedelta(microseconds=chrome_time)
        return epoch_start + delta

    # Filter results based on the date range and extract domain names
    history_list = []
    for url, visit_count, last_visit_time in results:
        readable_time = chrome_time_to_readable(last_visit_time)
        if start_date <= readable_time <= end_date:
            domain = urlparse(url).netloc
            history_list.append({
                'url': url,
                'domain': domain,
                'visit_count': visit_count,
                'last_visit_time': readable_time
            })

    return history_list

def find_chrome_history():
    # List of possible Chrome history file paths
    possible_paths = [
        os.path.expanduser('~') + r"\AppData\Local\Google\Chrome\User Data\Default\History",
        os.path.expanduser('~') + r"\AppData\Local\Microsoft\Edge\User Data\Default\History",  # Example for Edge
    ]

    for path in possible_paths:
        if os.path.exists(path):
            return path

    # If no valid path is found, raise an error
    raise FileNotFoundError("Chrome history file not found in known locations.")

@app.route('/metrics', methods=['GET'])
def metrics():
    return jsonify(get_system_metrics())

@app.route('/metrics2', methods=['GET'])
def metrics2():
    start_date_str = request.args.get('start_date')
    start_time_str = request.args.get('start_time')
    end_date_str = request.args.get('end_date')
    end_time_str = request.args.get('end_time')

    start_datetime_str = f"{start_date_str} {start_time_str}"
    end_datetime_str = f"{end_date_str} {end_time_str}"

    try:
        start_date = datetime.strptime(start_datetime_str, "%d/%m/%Y %H:%M")
        end_date = datetime.strptime(end_datetime_str, "%d/%m/%Y %H:%M")
        history = get_chrome_history(start_date, end_date)
        return jsonify(history)
    except ValueError as e:
        return jsonify({'error': str(e)})

@app.route('/clean-temp-files', methods=['POST'])
def clean_temp_files():
    temp_dir = 'C:\Windows\Temp'  # Update this to the actual temporary directory path
    deleted_files = []
    skipped_files = []

    for filename in os.listdir(temp_dir):
        file_path = os.path.join(temp_dir, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
                deleted_files.append(filename)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
                deleted_files.append(filename)
            else:
                skipped_files.append(filename)
        except Exception as e:
            print(f"Error deleting {file_path}: {e}")
            skipped_files.append(filename)
    
    return jsonify({
        'deleted': deleted_files,
        'skipped': skipped_files
    })


current_directory = os.getcwd()  # Start in the current working directory

@app.route('/execute-cmd', methods=['POST'])
def execute_cmd():
    global current_directory
    data = request.get_json()
    command = data.get('command')

    try:
        if command.startswith('cd '):
            # Handle 'cd' command separately
            new_directory = command[3:].strip()
            new_directory_path = os.path.abspath(os.path.join(current_directory, new_directory))

            if os.path.isdir(new_directory_path):
                current_directory = new_directory_path
                return jsonify({"output": f"Changed directory to {current_directory}"})
            else:
                return jsonify({"output": f"No such directory: {new_directory}"}), 500
        else:
            # Execute other commands
            process = subprocess.Popen(command, shell=True, cwd=current_directory, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate()

            if process.returncode == 0:
                return jsonify({"output": stdout})
            else:
                return jsonify({"output": stderr}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
def get_storage_info():
    usage = psutil.disk_usage('/')
    total = usage.total / (1024 ** 3)  # Convert to GB
    used = usage.used / (1024 ** 3)   
    free = usage.free / (1024 ** 3)    
    percent = usage.percent
    
    return  {
        "total": f"{total:.2f} GB",
        "used": f"{used:.2f} GB",
        "free": f"{free:.2f} GB",
        "percent": f"{percent:.2f}%"
    }

@app.route('/storage', methods=['GET'])
def storage_info():
    return jsonify(get_storage_info())


captured_packets = []

def resolve_domain(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except socket.herror:
        return "Unknown"

def process_packet(packet):
    global captured_packets

    if packet.haslayer(IP):
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst

        if packet.haslayer(TCP):
            src_port = packet[TCP].sport
            dst_port = packet[TCP].dport
            protocol = "TCP"
        elif packet.haslayer(UDP):
            src_port = packet[UDP].sport
            dst_port = packet[UDP].dport
            protocol = "UDP"
        else:
            src_port = "N/A"
            dst_port = "N/A"
            protocol = "Unknown"

        src_site = resolve_domain(src_ip)
        dst_site = resolve_domain(dst_ip)

        packet_info = {
            "src_site": src_site,
            "src_ip": src_ip,
            "src_port": src_port,
            "dst_site": dst_site,
            "dst_ip": dst_ip,
            "dst_port": dst_port,
            "protocol": protocol
        }

        captured_packets.append(packet_info)

@app.route('/packets', methods=['GET'])
def get_packets():
    return jsonify(captured_packets)

def sniff_packets(interface):
    conf.use_pcap = True  # Ensure Scapy uses pcap if available
    sniff(iface=interface, store=False, prn=process_packet)

@app.route('/scrape', methods=['GET'])
def scrape():
    url = request.args.get('url')
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extracting data
        title = soup.title.string if soup.title else 'No title found'
        headings = [h.get_text() for h in soup.find_all(['h1', 'h2', 'h3'])]
        links = [{'href': a.get('href'), 'text': a.get_text()} for a in soup.find_all('a', href=True)]
        meta_description = soup.find('meta', attrs={'name': 'description'})
        description = meta_description['content'] if meta_description else 'No description found'
        images = [urljoin(url, img.get('src')) for img in soup.find_all('img', src=True)]

        data = {
            'title': title,
            'headings': headings,
            'links': links,
            'description': description,
            'images': images,
            'html': soup.prettify()
        }
        return jsonify(data)
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    interface = 'Wi-Fi'  # Change this to the actual interface name
    threading.Thread(target=sniff_packets, args=(interface,), daemon=True).start()
    app.run(host='0.0.0.0', port=5001, debug=True)
