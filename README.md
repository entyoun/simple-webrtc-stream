# Simple WebRTC Audio Stream

A simple WebRTC audio streaming server that streams audio files to web browsers using Python and aiortc.

## Features

- Stream audio files (MP3/WAV) to web browsers via WebRTC
- Real-time audio streaming using RTP over UDP
- Simple web interface for connecting and listening
- Low-latency audio delivery

## Requirements

- Python 3.8 or higher
- FFmpeg libraries (for audio processing)

### macOS Setup

Install FFmpeg using Homebrew:
```bash
brew install ffmpeg
```

### Linux Setup

Install FFmpeg and development libraries:
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install ffmpeg libavformat-dev libavcodec-dev libavdevice-dev libavutil-dev libswscale-dev libswresample-dev libavfilter-dev

# CentOS/RHEL/Fedora
sudo dnf install ffmpeg-devel
```

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

1. **HTTP Server**: Serves the web interface and handles WebRTC signaling on port 8080
2. **WebRTC Negotiation**: Client and server exchange SDP offers/answers via HTTP
3. **RTP Streaming**: Audio data flows via RTP over UDP on dynamically allocated ports
4. **ICE**: Uses STUN servers for NAT traversal and peer-to-peer connection establishment

## File Structure

```
simple-webrtc-stream/
├── server.py              # Python WebRTC server
├── static/
│   └── index.html         # Web client interface
├── audio.mp3              # Your audio file (add this)
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Troubleshooting

- **"No audio file found" warning**: Make sure you have `audio.mp3` or `audio.wav` in the project root
- **Connection timeout**: Check your firewall settings and ensure UDP traffic is allowed
- **No audio playback**: Verify your browser supports WebRTC and audio autoplay policies

## Technical Details

- **Backend**: Python with aiortc library
- **Frontend**: Vanilla JavaScript with WebRTC APIs
- **Audio Transport**: RTP over UDP
- **Signaling**: HTTP REST API
- **NAT Traversal**: STUN (stun.l.google.com:19302)

## Browser Compatibility

Works with modern browsers that support WebRTC:
- Chrome 23+
- Firefox 22+
- Safari 11+
- Edge 15+