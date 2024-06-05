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
        
        client_header = client_socket.recv(1024)
        client_header_args = client_header.decode()
        client_header_args =  client_header_args.split(" ")
        method, path, protocol, host = tuple(client_header_args)
        path_strings = path.split('/')
        
        if path == '/':
            response = b'HTTP/1.1 200 OK\r\n\r\n'
        elif "echo" in path:
            response = f'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(path_strings[2])} \r\n\r\n{path_strings[2]}'.encode()
        else:
            response = b'HTTP/1.1 404 Not Found\r\n\r\n'
        
        
        client_socket.sendall(response)
        
        client_socket.close()

if __name__ == "__main__":
    main()
