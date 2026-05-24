# 📁 File Share — Dynamic File Sharing Web App

Aplikasi web sharing file yang dinamis dan interaktif. Tempatkan file di folder `data/` dan file otomatis muncul di website untuk didownload.

![File Share](https://img.shields.io/badge/Version-1.0-blue) ![Python](https://img.shields.io/badge/Python-3.7+-green) ![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ Fitur Utama

### 🔄 Dynamic File Detection
- File otomatis terdeteksi dari folder `data/`
- Real-time update setiap 30 detik
- Tidak perlu restart server saat menambah file

### 🎨 Modern UI (Coinbase-style)
- Clean dan professional design
- Responsive untuk semua device
- Grid dan List view modes
- Smooth animations dan transitions

### 📊 Smart File Management
- Auto-detection file type (archive, pdf, image, video, audio, code, document)
- Auto-categorization (Animation, Illustration, Video, dll)
- Human-readable file sizes (B, KB, MB, GB)
- Search dan filter functionality

### ⚡ Fast & Lightweight
- Pure Python HTTP server (tanpa dependencies)
- Vanilla JavaScript (tanpa framework)
- Tailwind CSS via CDN
- Lucide icons via CDN

## 🚀 Quick Start

### Prerequisites
- Python 3.7 atau higher
- Modern web browser (Chrome, Firefox, Safari, Edge)

### Installation

1. **Clone atau download project ini**
```bash
cd webshare
```

2. **Jalankan server**
```bash
python3 server.py
```

3. **Buka browser**
```
http://localhost:8080
```

That's it! 🎉 Server sekarang running di port 8080.

## 📂 Cara Menggunakan

### Menambah File Baru

Cukup copy file ke folder `data/`:

```bash
# Contoh menambah file
cp /path/to/your/file.rar data/

# Atau langsung move file
mv /path/to/file.pdf data/

# Bisa juga pakai file manager
# Drag & drop file ke folder data/
```

File akan **otomatis** muncul di website tanpa perlu restart server!

### Mengakses File

1. **Buka browser** → `http://localhost:8080`
2. **Browse file** di Grid atau List view
3. **Filter** berdasarkan kategori (Animation, Illustration, Video)
4. **Search** file dengan keyword
5. **Download** file dengan klik tombol Download

### Download Semua File

Klik tombol **"Download All"** di bar bawah untuk mendownload semua file sekaligus.

## 📁 Struktur Project

```
webshare/
├── server.py              # Custom Python HTTP server dengan API
├── index.html             # Frontend web app
├── data/                  # Folder untuk file-file (auto-detected)
│   ├── file1.rar
│   ├── file2.pdf
│   └── ...
├── README.md              # Documentation ini
└── DESIGN.md              # Design system reference
```

## 🛠️ Configuration

### Mengubah Port

Edit file `server.py`:

```python
PORT = 8080  # Ganti ke port yang diinginkan
```

### Mengubah Data Folder

Edit file `server.py`:

```python
DATA_FOLDER = "data"  # Ganti ke folder yang diinginkan
```

### Refresh Interval

Edit file `index.html`:

```javascript
// Auto-refresh files every 30 seconds
setInterval(fetchFiles, 30000);  // 30000 = 30 detik
```

## 🎨 Tech Stack

| Component | Technology |
|-----------|------------|
| **Backend** | Python 3 (http.server) |
| **Frontend** | HTML5, Vanilla JavaScript |
| **Styling** | Tailwind CSS (CDN) |
| **Icons** | Lucide Icons (CDN) |
| **Fonts** | Inter, JetBrains Mono (Google Fonts) |
| **API** | Custom REST API (`/api/files`) |

## 📡 API Endpoints

### GET `/api/files`

Return list semua file di folder `data/`.

**Response:**
```json
[
  {
    "id": 1,
    "name": "example.pdf",
    "type": "pdf",
    "size": 1048576,
    "sizeFormatted": "1.0 MB",
    "date": "2026-05-24",
    "category": "other",
    "description": "Shared file"
  }
]
```

**Fields:**
- `id`: Unique file identifier
- `name`: Nama file
- `type`: Tipe file (archive, pdf, image, video, audio, code, document, file)
- `size`: Ukuran file dalam bytes
- `sizeFormatted`: Ukuran file human-readable
- `date`: Tanggal modifikasi file (YYYY-MM-DD)
- `category`: Kategori file (animation, illustration, video, image, audio, other)
- `description`: Deskripsi otomatis berdasarkan kategori

## 🎯 Supported File Types

| Extension | Type | Category |
|-----------|------|----------|
| `.rar`, `.zip`, `.tar`, `.gz`, `.7z` | archive | based on name |
| `.pdf` | pdf | other |
| `.jpg`, `.jpeg`, `.png`, `.gif`, `.svg`, `.webp` | image | image |
| `.mp4`, `.avi`, `.mkv`, `.mov`, `.wmv` | video | video |
| `.mp3`, `.wav`, `.flac`, `.aac` | audio | audio |
| `.py`, `.js`, `.html`, `.css`, `.json`, `.txt`, `.md` | code | other |
| `.doc`, `.docx`, `.xls`, `.xlsx`, `.ppt`, `.pptx` | document | other |

## 🔍 Kategorization

File otomatis dikategorikan berdasarkan nama:

- **Animation** → `animasi`, `animation`
- **Illustration** → `ilustrasi`, `illustration`, `digital`
- **Video** → `video`, `production`
- **Image** → `foto`, `image`, `gambar`
- **Audio** → `audio`, `suara`, `music`
- **Other** → Default category

## 🐛 Troubleshooting

### Port 8080 already in use

```bash
# Kill process yang pakai port 8080
pkill -f "python3 server.py"

# Atau gunakan port lain
python3 server.py  # Edit PORT di server.py
```

### Files not showing up

1. **Check folder structure:**
```bash
ls -la data/
```

2. **Restart server:**
```bash
# Ctrl+C to stop, then
python3 server.py
```

3. **Clear browser cache:**
   - Ctrl+Shift+R (hard refresh)
   - Atau buka di Incognito mode

### Download not working

1. **Check file permissions:**
```bash
chmod 644 data/*
```

2. **Check browser console untuk errors**

3. **Try different browser**

## 📝 Design System

UI mengikuti **Coinbase Design System** (lihat `DESIGN.md` untuk detail):
- Primary color: `#0052ff` (Coinbase Blue)
- Display weight: 400 (calm, professional)
- Pill radius: 100px untuk buttons
- Card radius: 24px untuk containers
- Font: Inter (display), JetBrains Mono (numbers)

## 🤝 Contributing

Contributions are welcome! Areas for improvement:

- [ ] User authentication
- [ ] Upload functionality via web UI
- [ ] File preview (images, pdf, videos)
- [ ] Drag & drop upload
- [ ] Multiple folder support
- [ ] Custom categories/tags
- [ ] Download progress tracking
- [ ] File sharing via link

## 📄 License

MIT License — feel free to use for personal or commercial projects.

## 👤 Author

Created for UKK DKV 2026 project.

---

**Enjoy sharing files! 🎉**

Jika ada pertanyaan atau issues, feel free to ask. Happy coding!
