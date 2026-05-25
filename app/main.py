"""
Webshare FastAPI Server
A scalable file sharing server supporting 100-500+ concurrent connections
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
import uvicorn
from pathlib import Path

from app.routes.files import router as files_router
from app.websocket.manager import get_manager
from app.services.file_service import FileService
from app.services.cache_service import get_cache
import os

# Configuration
PORT = int(os.getenv("PORT", 8080))
DATA_FOLDER = os.getenv("DATA_FOLDER", "data")
HOST = os.getenv("HOST", "0.0.0.0")


# Services
file_service = FileService(data_folder=DATA_FOLDER)
cache = get_cache()
ws_manager = get_manager()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    print(f"📁 Serving files from: {Path(DATA_FOLDER).absolute()}")

    # Ensure data folder exists
    data_path = Path(DATA_FOLDER)
    if not data_path.exists():
        print(f"Creating '{DATA_FOLDER}' folder...")
        data_path.mkdir(exist_ok=True)
        print(f"✓ Place your files in the '{DATA_FOLDER}' folder")

    yield

    # Shutdown
    print("👋 Shutting down...")


# Create FastAPI app
app = FastAPI(
    title="Webshare FastAPI",
    description="Scalable file sharing server with real-time updates",
    version="2.0.0",
    lifespan=lifespan
)

# Include API routes
app.include_router(files_router)

# Mount static files for downloads
app.mount("/files", StaticFiles(directory=DATA_FOLDER), name="files")


# WebSocket endpoint for real-time updates
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for real-time file updates

    Clients connect here to receive instant updates when files change
    instead of polling every 30 seconds.
    """
    await ws_manager.connect(websocket)

    try:
        # Send current file list on connection
        from app.routes.files import get_files
        files = await get_files(refresh=False)
        await websocket.send_json({
            'type': 'initial',
            'timestamp': None,
            'data': files
        })

        # Keep connection alive
        while True:
            # Receive ping/pong messages
            data = await websocket.receive_text()

            # Echo back for connection health
            await websocket.send_json({
                'type': 'pong',
                'timestamp': None
            })

    except WebSocketDisconnect:
        await ws_manager.disconnect(websocket)
    except Exception as e:
        print(f"WebSocket error: {e}")
        await ws_manager.disconnect(websocket)


# Root endpoint - serve index.html
@app.get("/")
async def read_root():
    """Serve the main HTML file"""
    index_path = Path("index.html")
    if index_path.exists():
        return FileResponse("index.html")
    return {"message": "Webshare FastAPI Server", "version": "2.0.0"}


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    connection_count = await ws_manager.get_connection_count()
    return {
        "status": "healthy",
        "service": "webshare-fastapi",
        "version": "2.0.0",
        "active_connections": connection_count
    }


def main():
    """Run the server"""
    print("=" * 60)
    print("🚀 Webshare FastAPI Server")
    print("=" * 60)
    print(f"📁 Serving files from: {Path(DATA_FOLDER).absolute()}")
    print(f"🌐 Server running at: http://{HOST}:{PORT}")
    print(f"📊 API endpoint: http://{HOST}:{PORT}/api/files")
    print(f"🔌 WebSocket: ws://{HOST}:{PORT}/ws")
    print(f"📖 Docs: http://{HOST}:{PORT}/docs")
    print("=" * 60)
    print("\n✓ Files in /data folder will be automatically detected!")
    print("✓ WebSocket replaces polling for real-time updates")
    print("✓ Press Ctrl+C to stop the server\n")

    # Run with uvicorn
    uvicorn.run(
        "app.main:app",
        host=HOST,
        port=PORT,
        reload=False,
        access_log=True,
        log_level="info"
    )


if __name__ == "__main__":
    main()
