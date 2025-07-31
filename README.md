# WebSocket Network Connectivity Monitor

A simple WebSocket-based server that sends timestamp messages every 100ms to connected clients. Perfect for monitoring network connectivity and detecting gaps or interruptions in real-time communication.

## Features

- Sends timestamp messages every 100ms via WebSocket
- Real-time network gap detection
- Message counter to track missed messages
- Simple web interface for monitoring
- Runs on configurable port (default: 8970)
- Visual indicators for connectivity issues

## Requirements

- Python 3.7 or higher
- Modern web browser with WebSocket support

**Note**: This application uses async/await syntax and is not compatible with Python 2.x (which reached end-of-life in 2020).

## Installation

1. Clone or download this repository
2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Start the server:
   ```bash
   python3 server.py
   ```

2. Open your web browser and navigate to:
   ```
   http://localhost:8970
   ```

3. Click "Start Stream" to begin receiving timestamp messages

4. Click "Stop Stream" to disconnect

## How It Works

1. **HTTP Server**: Serves the web interface on port 8970
2. **WebSocket Connection**: Client connects to `/ws` endpoint for streaming
3. **Timestamp Broadcasting**: Server sends JSON messages every 100ms containing:
   - Current system timestamp (ISO format)
   - Timestamp in milliseconds
   - Sequential message counter
4. **Gap Detection**: Client detects network gaps when messages are >150ms apart
5. **Real-time Display**: Shows latest timestamp, message count, and any detected gaps

## Message Format

The server sends JSON messages with this structure:
```json
{
  "type": "timestamp",
  "timestamp_iso": "2025-07-31 10:30:45",
  "timestamp_ms": 1722445845123,
  "message_count": 42
}
```

## Network Connectivity Testing

This application is useful for:

1. **Load Balancer Testing**: Deploy behind a load balancer to test WebSocket handling
2. **Network Reliability**: Monitor for packet loss or connection interruptions  
3. **Failover Testing**: Detect gaps during server migrations or failovers
4. **Latency Monitoring**: Observe real-time message delivery patterns

Any gap longer than 150ms will be highlighted as a potential connectivity issue.

## File Structure

```
simple-websocket-stream/
├── server.py              # Python WebSocket server
├── static/
│   └── index.html         # Web client interface
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Configuration

To change the port, edit `server.py` line 122:
```python
web.run_app(app_coro, host="0.0.0.0", port=8970)
```

## Troubleshooting

- **WebSocket connection fails**: Check firewall settings and ensure port 8970 is accessible
- **No timestamp updates**: Check browser console for JavaScript errors
- **Connection immediately drops**: Verify server is running and WebSocket support is enabled

## Technical Details

- **Backend**: Python with aiohttp WebSocket support
- **Frontend**: Vanilla JavaScript with WebSocket API
- **Message Transport**: JSON over WebSocket
- **Update Frequency**: 100ms (10 messages per second)
- **Gap Detection Threshold**: 150ms

## Browser Compatibility

Works with modern browsers that support WebSockets:
- Chrome 16+
- Firefox 11+
- Safari 7+
- Edge 12+