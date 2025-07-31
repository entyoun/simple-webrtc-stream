import asyncio
import json
import logging
import os
import time
from aiohttp import web, WSMsgType

logging.basicConfig(level=logging.INFO)

# Store active WebSocket connections
websockets = set()

async def index(request):
    content = open(os.path.join(os.path.dirname(__file__), "static", "index.html"), "r").read()
    return web.Response(content_type="text/html", text=content)

async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    
    websockets.add(ws)
    # Reset message count for this new connection
    websocket_message_counts[ws] = 0
    logging.info(f"WebSocket client connected. Total connections: {len(websockets)}")
    
    try:
        async for msg in ws:
            if msg.type == WSMsgType.TEXT:
                data = json.loads(msg.data)
                if data.get('action') == 'start_stream':
                    logging.info("Client requested to start timestamp stream")
                    # Streaming will be handled by the background task
            elif msg.type == WSMsgType.ERROR:
                logging.error(f'WebSocket error: {ws.exception()}')
    except Exception as e:
        logging.error(f"WebSocket error: {e}")
    finally:
        websockets.discard(ws)
        # Clean up message count for this connection
        websocket_message_counts.pop(ws, None)
        logging.info(f"WebSocket client disconnected. Total connections: {len(websockets)}")
    
    return ws

# Store message counts per WebSocket connection
websocket_message_counts = {}

async def send_timestamps():
    """Background task to send timestamp messages to all connected WebSocket clients"""
    global websockets, websocket_message_counts
    
    logging.info("Starting timestamp streaming every 100ms")
    
    while True:
        try:
            if websockets:
                # Get current system time
                current_time = time.time()
                timestamp_iso = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(current_time))
                timestamp_ms = int(current_time * 1000)
                
                # Send to all connected WebSocket clients
                disconnected = set()
                for ws in websockets.copy():
                    try:
                        # Increment message count for this specific connection
                        if ws not in websocket_message_counts:
                            websocket_message_counts[ws] = 0
                        websocket_message_counts[ws] += 1
                        
                        message = {
                            'type': 'timestamp',
                            'timestamp_iso': timestamp_iso,
                            'timestamp_ms': timestamp_ms,
                            'message_count': websocket_message_counts[ws]
                        }
                        
                        message_json = json.dumps(message)
                        await ws.send_str(message_json)
                    except ConnectionResetError:
                        disconnected.add(ws)
                    except Exception as e:
                        logging.error(f"Error sending timestamp: {e}")
                        disconnected.add(ws)
                
                # Remove disconnected clients and clean up their message counts
                for ws in disconnected:
                    websockets.discard(ws)
                    websocket_message_counts.pop(ws, None)
            
            # Wait 100ms before next message
            await asyncio.sleep(0.1)
            
        except Exception as e:
            logging.error(f"Error in timestamp streaming: {e}")
            await asyncio.sleep(1)

async def init_app():
    app = web.Application()
    app.router.add_get("/", index)
    app.router.add_get("/ws", websocket_handler)
    app.router.add_static("/static/", path="static", name="static")
    
    # Start background timestamp streaming task
    asyncio.create_task(send_timestamps())
    
    return app

if __name__ == "__main__":
    app_coro = init_app()
    web.run_app(app_coro, host="0.0.0.0", port=8970)