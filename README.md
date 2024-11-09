# HTTP Proxy Server with Caching

A lightweight HTTP proxy server implementation in Python that includes caching capabilities. This proxy server acts as an intermediary between clients and web servers, with the ability to cache responses for improved performance.

## 🚀 Features

- **HTTP Request Forwarding**: Forwards client requests to target web servers
- **Response Caching**: Caches successful responses for faster subsequent access
- **Size-Limited Caching**: Implements a 16MB size limit for cached files
- **Error Handling**: Manages various HTTP response scenarios
- **Buffer Management**: Efficient data transfer with 4KB buffer size
- **Configurable Port**: Dynamic port assignment based on input

## 📋 Prerequisites

- Python 3.x
- Basic understanding of HTTP protocols
- Socket programming knowledge

## 🛠️ Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd [repository-name]
```

2. Ensure you have Python 3.x installed:
```bash
python --version
```

3. No additional dependencies required (uses standard Python libraries)

## 💻 Usage

1. Start the proxy server:
```bash
python3 proxy.py <port>
```
Example:
```bash
python3 proxy.py 8080
```

2. The actual port will be calculated as:
```python
actual_port = input_port + (4196840 % 100)
```

3. The server will start listening on localhost at the calculated port

## 🔧 Configuration

Key constants that can be modified in the code:

```python
MAX_FILE_SIZE = 16 * 1024 * 1024  # Maximum cache file size (16MB)
CACHE_DIR = "./cache"             # Cache directory location
BUFFER_SIZE = 4096                # Buffer size for data transfer
```

## 📁 Project Structure

```plaintext
.
├── proxy.py           # Main proxy server implementation
├── cache/            # Directory for cached responses
└── README.md         # Project documentation
```

## 🔍 Key Components

### 1. Main Server
- Creates socket server
- Listens for incoming connections
- Handles client connections

### 2. Request Handler
```python
def handle_client(client_socket):
    # Handles incoming client requests
    # Checks cache and serves/forwards accordingly
```

### 3. URL Parser
```python
def parsed_url(request):
    # Parses HTTP requests
    # Extracts method, host, port, and path
```

### 4. Request Forwarder
```python
def forward_request(client_socket, host, port, path, method, http_version):
    # Forwards requests to target servers
    # Manages server connections
```

## 🚥 Flow Process

1. Client sends request to proxy
2. Proxy checks cache for requested content
3. If cached:
   - Serves content from cache
4. If not cached:
   - Forwards request to web server
   - Receives response
   - Caches if response is successful (200)
   - Sends response to client

## ⚠️ Error Handling

- Returns 500 Internal Error for problematic responses
- Handles connection errors gracefully
- Validates request formats

## 🔒 Limitations

- Only handles basic HTTP requests
- No HTTPS support
- Maximum cache size of 16MB per file
- Basic error handling
- No concurrent connection handling

## 🔄 Cache Management

- Cached files stored in `./cache` directory
- Automatic cache directory creation
- Size-limited caching (16MB max)
- Caches only successful (200) responses

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## 📝 Notes

- For educational purposes
- Basic implementation - not recommended for production use
- Can be extended for more complex scenarios

## 🔮 Future Improvements

- Add HTTPS support
- Implement concurrent connection handling
- Add cache expiration
- Improve error handling
- Add request/response logging
- Implement cache size management
- Add support for more HTTP methods

## 👥 Authors

Krushikesh Thotange
