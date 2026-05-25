"""
File Routes - API endpoints for file operations
"""

from fastapi import APIRouter, HTTPException, Query
from typing import List, Dict, Optional
from app.services.file_service import FileService
from app.services.cache_service import get_cache
from app.websocket.manager import get_manager
import asyncio

router = APIRouter(prefix="/api", tags=["files"])

# Initialize services
file_service = FileService()
cache = get_cache()
ws_manager = get_manager()


@router.get("/files")
async def get_files(
    refresh: Optional[bool] = Query(False, description="Force refresh from disk")
) -> List[Dict]:
    """
    Get list of all files in data folder

    Args:
        refresh: Force cache refresh

    Returns:
        List of file metadata with id, name, path, type, size, etc.
    """
    cache_key = "file_list"

    # Try to get from cache unless refresh is requested
    if not refresh:
        cached_data = await cache.get(cache_key)
        if cached_data is not None:
            # Add IDs after retrieving from cache
            for idx, file in enumerate(cached_data, 1):
                file['id'] = idx
            return cached_data

    # Scan files from disk
    try:
        files = await file_service.scan_files()

        # Add sequential IDs
        for idx, file in enumerate(files, 1):
            file['id'] = idx

        # Cache the results
        await cache.set(cache_key, files)

        return files

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error scanning files: {str(e)}")


@router.get("/files/stats")
async def get_file_stats() -> Dict:
    """
    Get file statistics

    Returns:
        Statistics including total count and cache info
    """
    try:
        total_files = await file_service.get_file_count()
        cache_stats = await cache.get_stats()
        connection_count = await ws_manager.get_connection_count()

        return {
            'total_files': total_files,
            'active_connections': connection_count,
            'cache': cache_stats
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting stats: {str(e)}")


@router.post("/files/refresh")
async def refresh_files() -> Dict:
    """
    Force refresh file list and notify all connected clients

    Returns:
        Confirmation message with file count
    """
    try:
        # Invalidate cache and rescan
        await cache.invalidate("file_list")
        files = await get_files(refresh=True)

        # Broadcast update to all WebSocket clients
        await ws_manager.broadcast_files(files)

        return {
            'message': 'File list refreshed',
            'count': len(files),
            'timestamp': asyncio.get_event_loop().time()
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error refreshing files: {str(e)}")


@router.get("/health")
async def health_check() -> Dict:
    """
    Health check endpoint

    Returns:
        Server health status
    """
    return {
        'status': 'healthy',
        'service': 'webshare-fastapi',
        'version': '2.0.0'
    }
