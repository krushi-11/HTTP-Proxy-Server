import sys
import socket
from urllib.parse import urlparse
from pathlib import Path

# Constants
MAX_FILE_SIZE = 16 * 1024 * 1024  # Maximum file size to cache (16MB)
CACHE_DIR = "./cache"  # Cache directory
BUFFER_SIZE = 4096  # Buffer size for reading data

# Create the cache directory if it doesn't exist
Path(CACHE_DIR).mkdir(parents=True, exist_ok=True)

# Function to forward a request to the web server
def forward_request(client_socket, host, port, path, method, http_version):
    server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server_socket.connect((host, port))

    request = f"{method} {path}{http_version}\r\nHost: {host}\r\nConnection: close\r\n\r\n"
    server_socket.sendall(request.encode())

    while True:
        data = server_socket.recv(BUFFER_SIZE)
        if not data:
            break
        client_socket.sendall(data)

    server_socket.close()

def parsed_url(request):
    # Parse the client's request to extract host, port, and path
    request_lines = request.split("\r\n")
    request_line = request_lines[0]
    method, url, http_version = request_line.split(' ')
    parsed_url = urlparse(url)
    host = parsed_url.netloc
    port = parsed_url.port if parsed_url.port else 80
    path = parsed_url.path
    return method,http_version,host,port,path

# Function to handle client requests
def handle_client(client_socket):
    request = client_socket.recv(BUFFER_SIZE).decode()
    
    method,host,port,path,http_version = parsed_url(request)
    
    
    # Check if the file is in the cache
    cache_path = f"{CACHE_DIR}/{host}{path}"
    cached_file = Path(cache_path)
    
    if cached_file.is_file():
        # Serve the file from the cache
        with open(cache_path, 'rb') as file:
            data = file.read()
            client_socket.send(data)
    else:
        # Request the file from the web server
        forward_request(client_socket, host, port, path, method, http_version)

        # Receive the response from the web server
        response = b""
        while True:
            data = client_socket.recv(BUFFER_SIZE)
            if not data:
                break
            response += data

        # Check the HTTP response status
        response_str = response.decode()
        status_code = int(response_str.split()[1])
        
        if status_code == 200:
            # Cache the file
            if len(response) <= MAX_FILE_SIZE:
                with open(cache_path, 'wb') as file:
                    file.write(response)
        elif status_code != 404:
            # Send a 500 Internal Error response if not 200 or 404
            error_response = "HTTP/1.1 500 Internal Error\r\n\r\n"
            client_socket.send(error_response.encode())

    client_socket.close()

# Main function
def main():
    if len(sys.argv) != 2:
        print("Usage: python3 proxy.py <port>")
        return
    
    port = int(sys.argv[1])
    port = port + (4196840)%100
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', port))
    server_socket.listen(5)
    
    print(f"Proxy server listening on port {port}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Received a client connection from: {addr}")
        handle_client(client_socket)

if __name__ == "__main__":
    main()
