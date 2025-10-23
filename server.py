import socket
import os
import random
import string
import stat

def generate_random_name(length=10):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def overwrite_file(file_path, pattern, passes=7):
    if not os.path.exists(file_path):
        return False
    try:
        with open(file_path, 'wb') as f:
            file_size = os.path.getsize(file_path)
            for _ in range(passes):
                if pattern == 'random':
                    data = bytes(random.getrandbits(8) for _ in range(file_size))
                else:
                    data = bytes([pattern]) * file_size
                f.seek(0)
                f.write(data)
                f.flush()
        return True
    except Exception as e:
        print(f"Error overwriting file: {e}")
        return False

def secure_delete(file_path, rename_count=5):
    if not os.path.exists(file_path):
        return "File does not exist"
    
    # Make file writable if read-only
    try:
        os.chmod(file_path, stat.S_IWRITE)
    except:
        pass
    
    # Overwrite with German VSITR patterns
    patterns = [0x00, 0xFF, 0x00, 0xFF, 0x00, 0xFF, 'random']
    for i, pattern in enumerate(patterns):
        if not overwrite_file(file_path, pattern):
            return f"Failed at overwrite pass {i+1}"
    
    # Rename multiple times
    dir_path = os.path.dirname(file_path)
    base_name = os.path.basename(file_path)
    for _ in range(rename_count):
        new_name = generate_random_name()
        new_path = os.path.join(dir_path, new_name)
        try:
            os.rename(file_path, new_path)
            file_path = new_path
        except Exception as e:
            return f"Failed to rename: {e}"
    
    # Delete the file
    try:
        os.remove(file_path)
        return "File securely deleted"
    except Exception as e:
        return f"Failed to delete: {e}"

def start_server(host='localhost', port=12345):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"Server listening on {host}:{port}")
        while True:
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")
                data = conn.recv(1024)
                if not data:
                    break
                file_path = data.decode('utf-8')
                result = secure_delete(file_path)
                conn.sendall(result.encode('utf-8'))

if __name__ == "__main__":
    start_server()