import socket
import threading
import sys

def forward(src, dst):
    try:
        while True:
            data = src.recv(4096)
            if not data:
                break
            dst.sendall(data)
    except Exception:
        pass
    finally:
        try:
            src.close()
        except:
            pass
        try:
            dst.close()
        except:
            pass

def start_proxy(local_port=5434, target_host="172.19.130.255", target_port=5432):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("127.0.0.1", local_port))
    server.listen(10)
    print(f"PostgreSQL TCP Bridge listening on 127.0.0.1:{local_port} -> {target_host}:{target_port}")

    while True:
        client_sock, _ = server.accept()
        target_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            target_sock.connect((target_host, target_port))
            threading.Thread(target=forward, args=(client_sock, target_sock), daemon=True).start()
            threading.Thread(target=forward, args=(target_sock, client_sock), daemon=True).start()
        except Exception as e:
            print(f"Connection to target failed: {e}")
            client_sock.close()

if __name__ == "__main__":
    start_proxy()
