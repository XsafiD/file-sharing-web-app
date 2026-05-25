"""
File Service - Handles file scanning and metadata generation
Optimized for async operations and caching
"""

import asyncio
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
import aiofiles.os as aios


class FileService:
    """Service for scanning and managing file metadata"""

    # File type mapping
    TYPE_MAP = {
        '.rar': 'archive', '.zip': 'archive', '.tar': 'archive',
        '.gz': 'archive', '.7z': 'archive',
        '.pdf': 'pdf',
        '.jpg': 'image', '.jpeg': 'image', '.png': 'image',
        '.gif': 'image', '.svg': 'image', '.webp': 'image',
        '.mp4': 'video', '.avi': 'video', '.mkv': 'video',
        '.mov': 'video', '.wmv': 'video',
        '.mp3': 'audio', '.wav': 'audio', '.flac': 'audio',
        '.aac': 'audio',
        '.py': 'code', '.js': 'code', '.html': 'code',
        '.css': 'code', '.json': 'code', '.txt': 'code',
        '.md': 'code',
        '.doc': 'document', '.docx': 'document',
        '.xls': 'document', '.xlsx': 'document',
        '.ppt': 'document', '.pptx': 'document',
    }

    # Category keywords
    CATEGORY_KEYWORDS = {
        'animation': ['animasi', 'animation'],
        'illustration': ['ilustrasi', 'illustration', 'digital'],
        'video': ['video', 'production'],
        'image': ['foto', 'image', 'gambar'],
        'audio': ['audio', 'suara', 'music'],
    }

    # Category descriptions
    CATEGORY_DESCRIPTIONS = {
        'animation': 'Animation resources and assets',
        'illustration': 'Digital illustration files',
        'video': 'Video production materials',
        'image': 'Image files and photos',
        'audio': 'Audio files and sound effects',
        'other': 'Project files and resources'
    }

    def __init__(self, data_folder: str = "data"):
        self.data_folder = Path(data_folder)

    async def scan_files(self, force_refresh: bool = False) -> List[Dict]:
        """
        Scan data folder and return file metadata
        Returns sorted list of files
        """
        if not self.data_folder.exists():
            return []

        files = []
        # Async file scanning
        for file_path in self.data_folder.rglob('*'):
            if file_path.is_file():
                file_data = await self._process_file(file_path)
                if file_data:
                    files.append(file_data)

        # Sort by folder, then by name
        files.sort(key=lambda x: (x['folder'], x['name']))
        return files

    async def _process_file(self, file_path: Path) -> Optional[Dict]:
        """Process a single file and extract metadata"""
        try:
            # Get relative path
            relative_path = file_path.relative_to(self.data_folder)
            path_str = str(relative_path).replace('\\', '/')

            # Get file stats (sync is fine for stat)
            stat = file_path.stat()

            # Extract metadata
            ext = file_path.suffix.lower()
            file_type = self._get_file_type(ext)
            category = self._get_category(file_path.name)
            size_bytes = stat.st_size
            size_formatted = self._format_size(size_bytes)
            mod_date = datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d')

            # Get folder info
            folder_path = relative_path.parent
            folder_name = str(folder_path) if str(folder_path) != '.' else ''

            return {
                'id': None,  # Will be set after sorting
                'name': file_path.name,
                'path': path_str,
                'folder': folder_name,
                'type': file_type,
                'size': size_bytes,
                'sizeFormatted': size_formatted,
                'date': mod_date,
                'category': category,
                'description': self._get_description(file_path.name, category, folder_name)
            }

        except Exception as e:
            print(f"Error processing file {file_path}: {e}")
            return None

    def _get_file_type(self, ext: str) -> str:
        """Determine file type based on extension"""
        return self.TYPE_MAP.get(ext, 'file')

    def _get_category(self, filename: str) -> str:
        """Determine category based on filename keywords"""
        name_lower = filename.lower()

        for category, keywords in self.CATEGORY_KEYWORDS.items():
            if any(keyword in name_lower for keyword in keywords):
                return category

        return 'other'

    def _get_description(self, filename: str, category: str, folder_name: str = '') -> str:
        """Generate description for file"""
        base_desc = self.CATEGORY_DESCRIPTIONS.get(category, 'Shared file')

        if folder_name:
            return f"{base_desc} — {folder_name}"

        return base_desc

    def _format_size(self, size_bytes: int) -> str:
        """Format file size in human-readable format"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                if unit == 'B':
                    return f"{size_bytes:.0f} {unit}"
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} TB"

    async def get_file_count(self) -> int:
        """Get total number of files in data folder"""
        if not self.data_folder.exists():
            return 0

        count = 0
        for _ in self.data_folder.rglob('*'):
            if _.is_file():
                count += 1
        return count
