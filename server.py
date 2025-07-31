import asyncio
import json
import logging
import os
from aiohttp import web
from aiortc import RTCPeerConnection, RTCSessionDescription, RTCConfiguration, RTCIceServer
from aiortc.contrib.media import MediaPlayer

logging.basicConfig(level=logging.INFO)

pcs = set()

async def index(request):
    content = open(os.path.join(os.path.dirname(__file__), "static", "index.html"), "r").read()
    return web.Response(content_type="text/html", text=content)

async def offer(request):
    params = await request.json()
    offer = RTCSessionDescription(sdp=params["sdp"], type=params["type"])

    pc = RTCPeerConnection(
        configuration=RTCConfiguration([
            RTCIceServer(urls=["stun:stun.l.google.com:19302"])
        ])
    )
    pcs.add(pc)

    @pc.on("connectionstatechange")
    async def on_connectionstatechange():
        logging.info(f"Connection state is {pc.connectionState}")
        if pc.connectionState == "closed":
            pcs.discard(pc)
    
    @pc.on("iceconnectionstatechange")
    async def on_iceconnectionstatechange():
        logging.info(f"ICE connection state is {pc.iceConnectionState}")
    
    @pc.on("icegatheringstatechange")
    async def on_icegatheringstatechange():
        logging.info(f"ICE gathering state is {pc.iceGatheringState}")
    
    @pc.on("icecandidate")
    async def on_icecandidate(candidate):
        logging.info(f"ICE candidate: {candidate}")
    
    @pc.on("track")
    async def on_track(track):
        logging.info(f"Track received: {track.kind}")

    try:
        # Set remote description first
        await pc.setRemoteDescription(offer)
        
        # Find and add audio file after setting remote description
        audio_file = os.path.join(os.path.dirname(__file__), "audio.wav")
        if not os.path.exists(audio_file):
            audio_file = os.path.join(os.path.dirname(__file__), "audio.mp3")
        
        if os.path.exists(audio_file):
            player = MediaPlayer(audio_file, loop=True)
            if player.audio:
                # Simple addTrack without direction specification
                track = pc.addTrack(player.audio)
                logging.info(f"Added audio track to peer connection: {track}")
        else:
            logging.warning("No audio file found (audio.wav or audio.mp3)")
        
        # Create and set answer
        answer = await pc.createAnswer()
        
        # Workaround for aiortc direction bug
        for transceiver in pc.getTransceivers():
            if transceiver._offerDirection is None:
                transceiver._offerDirection = "recvonly"
        
        await pc.setLocalDescription(answer)

        return web.Response(
            content_type="application/json",
            text=json.dumps({
                "sdp": pc.localDescription.sdp,
                "type": pc.localDescription.type
            })
        )
    except Exception as e:
        logging.error(f"Error in offer handling: {e}")
        import traceback
        traceback.print_exc()
        if pc in pcs:
            pcs.discard(pc)
        return web.Response(
            status=500,
            content_type="application/json",
            text=json.dumps({"error": str(e)})
        )

async def on_shutdown(app):
    coros = [pc.close() for pc in pcs]
    await asyncio.gather(*coros)
    pcs.clear()

if __name__ == "__main__":
    app = web.Application()
    app.router.add_get("/", index)
    app.router.add_post("/offer", offer)
    app.router.add_static("/static/", path="static", name="static")
    app.on_shutdown.append(on_shutdown)
    
    web.run_app(app, host="0.0.0.0", port=8080)