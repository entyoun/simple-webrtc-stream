# Load Balancer Audio Stream Test

A WebSocket-based audio streaming server designed for testing F5 load balancers and live migration scenarios. All traffic flows through port 8080, making it perfect for load balancer testing.

## Features

- Stream audio files (MP3/WAV) to web browsers via WebSocket
- All traffic flows through port 8080 (load balancer compatible)
- Real-time audio streaming using raw PCM data
- Perfect for testing live migrations and failover scenarios
- Simple web interface for connecting and listening
- Low-latency audio delivery

## Requirements

- Python 3.8 or higher

**Note**: The required audio processing libraries (FFmpeg) are included with the PyAV package installation. No additional system libraries need to be installed on most systems.

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

4. Add your audio file:
   - Place an audio file named `audio.mp3` or `audio.wav` in the project root directory
   - The server will automatically detect and stream the audio file

## Usage

1. Start the server:
   ```bash
   python server.py
   ```

2. Open your web browser and navigate to:
   ```
   http://localhost:8080
   ```

3. Click "Start Stream" to begin receiving the audio stream

4. Click "Stop Stream" to disconnect

## How It Works

1. **HTTP Server**: Serves the web interface on port 8080
2. **WebSocket Connection**: Client connects to `/ws` endpoint for streaming
3. **Audio Processing**: Server decodes audio file and converts to raw PCM data
4. **Real-time Streaming**: Audio chunks sent via WebSocket as binary data
5. **Client Playback**: Browser receives PCM data and plays via Web Audio API

**Load Balancer Compatibility**: All traffic (HTTP and WebSocket) flows through port 8080, ensuring your F5 load balancer can properly route and monitor all connections.

## Load Balancer Testing

This application is specifically designed for testing F5 load balancers during live migrations:

1. **Deploy behind F5**: Configure your F5 to forward traffic to multiple instances
2. **Start streaming**: Connect clients and start audio playback
3. **Perform migration**: Live migrate servers or perform failover
4. **Monitor continuity**: Any audio interruption indicates load balancer issues

The continuous audio stream makes it easy to detect even brief interruptions during migrations.

## File Structure

```
load-balancer-audio-test/
├── server.py              # Python WebSocket server
├── static/
│   └── index.html         # Web client interface
├── audio.mp3              # Your audio file (add this)
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Troubleshooting

- **"No audio file found" warning**: Make sure you have `audio.mp3` or `audio.wav` in the project root
- **WebSocket connection fails**: Check your load balancer WebSocket configuration
- **No audio playback**: Click in the browser first to satisfy autoplay policies
- **Audio choppy through load balancer**: Check load balancer session persistence settings

## Technical Details

- **Backend**: Python with aiohttp and PyAV
- **Frontend**: Vanilla JavaScript with Web Audio API
- **Audio Transport**: Raw PCM data over WebSocket
- **Connection**: HTTP upgrade to WebSocket on port 8080
- **Audio Format**: 44.1kHz 16-bit stereo PCM

## Load Balancer Configuration

For F5 load balancers, ensure:
- WebSocket support is enabled
- Session persistence is configured if needed
- Health checks monitor the HTTP endpoint
- Timeout values account for long-lived WebSocket connections

## Browser Compatibility

Works with modern browsers that support WebSockets and Web Audio API:
- Chrome 23+
- Firefox 25+
- Safari 14+
- Edge 12+