import socket
import threading
import os

def RetrFile(name, sock):
  filename = sock.recv(1024).decode()
  if os.path.isfile(filename):
    message = "EXISTS " + str(os.path.getsize(filename))
    sock.send(message.encode())
    userResponse = sock.recv(1024).decode()
    if userResponse[:2] == 'OK': 
      with open(filename, 'rb') as f:
        bytesToSend = f.read(1024)
        sock.send(bytesToSend)
        while len(bytesToSend) > 0:
          print(bytesToSend)
          bytesToSend = f.read(1024)
          sock.send(bytesToSend)
  else:
    sock.send("ERR".encode())
  sock.close()
      
def Main():
  host = '127.0.0.1'
  port = 5000

  s = socket.socket()
  s.bind((host,port))

  s.listen(5)

  print("Server Started.")
  while True:
    conn, addr = s.accept()
    print("Client connected ip:<" + str(addr) + ">")
    t = threading.Thread(target=RetrFile, args=("retrThread", conn))
    t.start()
  s.close()

if __name__ == '__main__':
  Main()