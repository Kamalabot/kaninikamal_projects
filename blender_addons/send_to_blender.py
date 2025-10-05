import socket, sys, pathlib

PORT = 9001

# read the script you want to send
path = pathlib.Path(sys.argv[1])
code = path.read_text()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("localhost", PORT))
sock.sendall(code.encode("utf-8"))
sock.close()

print(f"Sent {path.name} to Blender")
