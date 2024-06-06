import socket
import sys
# # Constants
# ROUTES = {
#     #"echo": handle_echo,
# }

# # Functions
# def handle_echo():
#     pass

def open_existing_file(directory, file_name):
    try:
        with open(f"/{directory}/{file_name}", "r") as f:
            body = f.read()
    except:
        body = None
    return body

def write_to_file(directory, file_name, post_content):
    try:
        with open(f"/{directory}/{file_name}", "w") as f:
            body = f.write(post_content)
    except:
        body = None
    return body

def check_encoding(headers):
        try :
            check = True if "gzip" in headers['Accept-Encoding'] else False
        except:
            check = False
        return check

def generate_response(method, path, path_elements, headers, post_content=None):
    if path == '/':
        response = b'HTTP/1.1 200 OK\r\n\r\n'
    elif "echo" in path:
        if check_encoding(headers):
            response = f'HTTP/1.1 200 OK\r\nContent-Encoding: gzip\r\nContent-Type: text/plain\r\nContent-Length: {len(path_elements[2])} \r\n\r\n{path_elements[2]}'.encode()
        else:
            response = f'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(path_elements[2])} \r\n\r\n{path_elements[2]}'.encode()
    elif 'user-agent' in path:
        response = f'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(headers['User-Agent'])} \r\n\r\n{headers['User-Agent']}'.encode()
    elif 'files' in path:
        directory = sys.argv[2]
        file_name = path_elements[2]
        if method == "POST" and post_content != None:
            file_content = write_to_file(directory, file_name, post_content)
            response = b'HTTP/1.1 201 Created\r\n\r\n'
        else:
            file_content = open_existing_file(directory, file_name)
            if file_content != None:
                response = f'HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: {len(file_content)}\r\n\r\n{file_content}'.encode()
            else:
                response = b'HTTP/1.1 404 Not Found\r\n\r\n'
    else:
        response = b'HTTP/1.1 404 Not Found\r\n\r\n'
        
    return response

def handle_connection(client_socket):
    client_request = client_socket.recv(1024)
    print(client_request)
    request_lines = client_request.decode()
    request_lines =  request_lines.split("\r\n")
    request_line = request_lines[0]
    
    method, path, http_version = request_line.split(' ')
    
    path_elements = path.split("/") 
    
    headers = {}
    for header_line in request_lines[1:]:
        if header_line == '':
            break
        header_key, header_value = header_line.split(': ', 1)
        headers[header_key] = header_value
    
    try:
        post_content = request_lines[-1]
    except:
        pass

    response = generate_response(method, path, path_elements, headers, post_content)
    client_socket.sendall(response)
    client_socket.close()
    print(f"Connection on port: {client_socket} closed.")

    

def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    
    while True:
        client_socket, client_adress = server_socket.accept()
        print(f"New connection from {client_adress}")
        print(f"Socket: {client_socket}")
        handle_connection(client_socket)
        
        

if __name__ == "__main__":
    main()
