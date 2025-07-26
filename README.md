# MarkItDown API

A FastAPI-based web service that converts various document formats to Markdown using Microsoft's MarkItDown library.

## Features

- **Universal Document Conversion**: Convert multiple file formats to Markdown
- **REST API**: Simple HTTP endpoints for document processing
- **Docker Support**: Ready-to-deploy containerized application
- **File Format Support**: PDF, Word, PowerPoint, Excel, Images, HTML, CSV, JSON, XML, ZIP, EPub, Audio files

## Supported Formats

- **Documents**: `.pdf`, `.docx`, `.pptx`, `.xlsx`
- **Images**: `.png`, `.jpg`, `.jpeg`, `.gif`, `.bmp`, `.tiff`
- **Text Formats**: `.html`, `.htm`, `.csv`, `.json`, `.xml`, `.txt`
- **Archives**: `.zip`
- **Ebooks**: `.epub`
- **Audio**: `.mp3`, `.wav`, `.m4a`, `.flac`
- **Other**: YouTube URLs

## API Endpoints

### `GET /`
Health check endpoint that returns a welcome message.

### `GET /env`
Environment variable example endpoint.

### `POST /upload`
Upload and convert a document to Markdown.

**Request**: Multipart form data with a file
**Response**: JSON with converted Markdown content, metadata, and file information

### `GET /supported-formats`
Returns a list of all supported file formats and their categories.

## Quick Start

### Using Docker

```bash
# Build the image
docker build -t markitdown-api .

# Run the container
docker run -p 8000:80 markitdown-api
```

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
uvicorn src.index:app --host 0.0.0.0 --port 8000
```

## Usage Example

```bash
# Upload a document for conversion
curl -X POST "http://localhost:8000/upload" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@document.pdf"

# Check supported formats
curl -X GET "http://localhost:8000/supported-formats"
```

## Requirements

- Python 3.11+
- FastAPI
- MarkItDown library with all extensions
- Uvicorn ASGI server

## License

MIT License - see [LICENSE.md](LICENSE.md) for details.

## Built With

- [FastAPI](https://fastapi.tiangolo.com/) - Modern, fast web framework
- [MarkItDown](https://github.com/microsoft/markitdown) - Microsoft's document conversion library
- [Uvicorn](https://www.uvicorn.org/) - ASGI server implementation