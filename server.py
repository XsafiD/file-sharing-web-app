#!/usr/bin/env python3
"""
Dynamic File Share Server
Auto-reads files from /data folder and serves them via API
"""

import http.server
import socketserver
import json
import os
import urllib.parse
from pathlib import Path
from datetime import datetime

# Configuration
PORT = 8080
DATA_FOLDER = "data"

class FileShareHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Parse the path
        parsed_path = urllib.parse.urlparse(self.path)

        # API endpoint to get file list
        if parsed_path.path == '/api/files':
            self.send_file_list()
        else:
            # Serve static files normally
            super().do_GET()

    def send_file_list(self):
        """Read data folder and return JSON file list"""
        try:
            data_path = Path(DATA_FOLDER)

            if not data_path.exists():
                self.send_json_response([])
                return

            files = []
            # Recursive scan all files in data folder
            for file_path in data_path.rglob('*'):
                if file_path.is_file():
                    # Get relative path from data folder
                    relative_path = file_path.relative_to(data_path)
                    path_str = str(relative_path).replace('\\', '/')  # Normalize path separators

                    # Get file stats
                    stat = file_path.stat()

                    # Get file extension and determine type
                    ext = file_path.suffix.lower()
                    file_type = self.get_file_type(ext)

                    # Get category based on filename
                    category = self.get_category(file_path.name)

                    # Format file size
                    size_bytes = stat.st_size
                    size_formatted = self.format_size(size_bytes)

                    # Get modification date
                    mod_date = datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d')

                    # Get folder depth and path info
                    folder_path = relative_path.parent
                    folder_name = str(folder_path) if str(folder_path) != '.' else ''

                    files.append({
                        'id': len(files) + 1,
                        'name': file_path.name,
                        'path': path_str,  # Relative path for download
                        'folder': folder_name,  # Folder name for display
                        'type': file_type,
                        'size': size_bytes,
                        'sizeFormatted': size_formatted,
                        'date': mod_date,
                        'category': category,
                        'description': self.get_description(file_path.name, category, folder_name)
                    })

            # Sort by folder first, then by name
            files.sort(key=lambda x: (x['folder'], x['name']))

            self.send_json_response(files)

        except Exception as e:
            print(f"Error reading files: {e}")
            self.send_json_response([])

    def get_file_type(self, ext):
        """Determine file type icon based on extension"""
        type_map = {
            '.rar': 'archive',
            '.zip': 'archive',
            '.tar': 'archive',
            '.gz': 'archive',
            '.7z': 'archive',
            '.pdf': 'pdf',
            '.jpg': 'image',
            '.jpeg': 'image',
            '.png': 'image',
            '.gif': 'image',
            '.svg': 'image',
            '.webp': 'image',
            '.mp4': 'video',
            '.avi': 'video',
            '.mkv': 'video',
            '.mov': 'video',
            '.wmv': 'video',
            '.mp3': 'audio',
            '.wav': 'audio',
            '.flac': 'audio',
            '.aac': 'audio',
            '.py': 'code',
            '.js': 'code',
            '.html': 'code',
            '.css': 'code',
            '.json': 'code',
            '.txt': 'code',
            '.md': 'code',
            '.doc': 'document',
            '.docx': 'document',
            '.xls': 'document',
            '.xlsx': 'document',
            '.ppt': 'document',
            '.pptx': 'document',
        }
        return type_map.get(ext, 'file')

    def get_category(self, filename):
        """Determine category based on filename"""
        name_lower = filename.lower()

        if 'animasi' in name_lower or 'animation' in name_lower:
            return 'animation'
        elif 'ilustrasi' in name_lower or 'illustration' in name_lower or 'digital' in name_lower:
            return 'illustration'
        elif 'video' in name_lower or 'production' in name_lower:
            return 'video'
        elif 'foto' in name_lower or 'image' in name_lower or 'gambar' in name_lower:
            return 'image'
        elif 'audio' in name_lower or 'suara' in name_lower or 'music' in name_lower:
            return 'audio'
        else:
            return 'other'

    def get_description(self, filename, category, folder_name=''):
        """Generate description based on category, filename and folder"""
        descriptions = {
            'animation': 'Animation resources and assets',
            'illustration': 'Digital illustration files',
            'video': 'Video production materials',
            'image': 'Image files and photos',
            'audio': 'Audio files and sound effects',
            'other': 'Project files and resources'
        }

        base_desc = descriptions.get(category, 'Shared file')

        # Add folder info if file is in a subfolder
        if folder_name:
            return f"{base_desc} — {folder_name}"

        return base_desc

    def format_size(self, size_bytes):
        """Format file size in human-readable format"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                if unit == 'B':
                    return f"{size_bytes:.0f} {unit}"
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} TB"

    def send_json_response(self, data):
        """Send JSON response"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

        json_data = json.dumps(data, indent=2)
        self.wfile.write(json_data.encode())

    def log_message(self, format, *args):
        """Custom log message"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{timestamp}] {format % args}")


def main():
    # Ensure data folder exists
    data_path = Path(DATA_FOLDER)
    if not data_path.exists():
        print(f"Creating '{DATA_FOLDER}' folder...")
        data_path.mkdir(exist_ok=True)
        print(f"✓ Place your files in the '{DATA_FOLDER}' folder")

    # Start server
    with socketserver.TCPServer(("", PORT), FileShareHandler) as httpd:
        print("=" * 60)
        print("🚀 Dynamic File Share Server")
        print("=" * 60)
        print(f"📁 Serving files from: {data_path.absolute()}")
        print(f"🌐 Server running at: http://localhost:{PORT}")
        print(f"📊 API endpoint: http://localhost:{PORT}/api/files")
        print("=" * 60)
        print("\n✓ Files in /data folder will be automatically detected!")
        print("✓ Press Ctrl+C to stop the server\n")

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n👋 Server stopped. Goodbye!")


if __name__ == "__main__":
    main()
