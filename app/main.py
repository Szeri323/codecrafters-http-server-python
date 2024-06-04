# Uncomment this to pass the first stage
import socket


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    
    while True:
        client_socket, client_adress = server_socket.accept()
        print(f"New connection from {client_adress}")
        print(f"Socket: {client_socket}")
        
        recived = client_socket.recv(1024)
        
        if recived == b'GET / HTTP/1.1\r\nHost: localhost:4221\r\n\r\n':
            print(f"recived: {recived}")
            response = b'HTTP/1.1 200 OK\r\n\r\n'
        else:
            print(f"recived: {recived}")
            response = b'HTTP/1.1 404 Not Found\r\n\r\n'
        
        
        client_socket.sendall(response)
        
        client_socket.close()

if __name__ == "__main__":
    main()
