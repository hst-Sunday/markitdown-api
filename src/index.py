from fastapi import FastAPI, UploadFile, File, HTTPException
from markitdown import MarkItDown
import os
import uuid
import re



app = FastAPI()
md = MarkItDown()


@app.get("/")
async def root():
    return {"message": "Hello, World!"}


@app.get("/env")
async def env():
    message = f"Here is an example of getting an environment variable: {os.getenv('MESSAGE', 'Not set')}"
    return {"message": message}


@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """
    Universal document upload endpoint that converts files to markdown using MarkItDown
    Supports: PDF, Word, PowerPoint, Excel, Images, HTML, CSV, JSON, XML, ZIP, EPub, Audio
    """
    
    # Check if file is selected
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail={
                'success': False,
                'error': 'No file selected',
                'message': 'Please select a file to upload'
            }
        )
    
    try:
        # Secure the filename using regex (replace werkzeug's secure_filename)
        filename = re.sub(r'[^a-zA-Z0-9._-]', '_', file.filename)
        
        # Create unique temporary file path in /tmp directory (required for Vercel)
        file_extension = os.path.splitext(filename)[1].lower()
        unique_filename = f"{uuid.uuid4().hex}_{filename}"
        temp_file_path = os.path.join('/tmp', unique_filename)
        
        # Ensure /tmp directory exists (should exist on Vercel, but check anyway)
        os.makedirs('/tmp', exist_ok=True)
        
        # Save uploaded file to /tmp
        file_content = await file.read()
        with open(temp_file_path, 'wb') as temp_file:
            temp_file.write(file_content)
        
        try:
            # Convert file to markdown using MarkItDown
            result = md.convert(temp_file_path)
            
            # Get file information
            file_size = os.path.getsize(temp_file_path)
            
            response_data = {
                'success': True,
                'data': {
                    'filename': filename,
                    'file_extension': file_extension,
                    'file_size_bytes': file_size,
                    'markdown_content': result.text_content,
                    'title': getattr(result, 'title', None),
                    'metadata': getattr(result, 'metadata', {})
                },
                'message': 'File successfully converted to markdown'
            }
            
            return response_data
            
        except Exception as conversion_error:
            raise HTTPException(
                status_code=422,
                detail={
                    'success': False,
                    'error': 'Conversion failed',
                    'message': f'Failed to convert file to markdown: {str(conversion_error)}',
                    'filename': filename
                }
            )
            
        finally:
            # Clean up temporary file from /tmp
            if os.path.exists(temp_file_path):
                try:
                    os.unlink(temp_file_path)
                except OSError:
                    # Log but don't fail if cleanup fails
                    pass
                
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                'success': False,
                'error': 'Upload failed',
                'message': f'An error occurred during file upload: {str(e)}'
            }
        )

@app.get("/supported-formats")
async def supported_formats():
    """
    Returns list of supported file formats
    """
    formats = {
        'documents': ['.pdf', '.docx', '.pptx', '.xlsx'],
        'images': ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff'],
        'text_formats': ['.html', '.htm', '.csv', '.json', '.xml', '.txt'],
        'archives': ['.zip'],
        'ebooks': ['.epub'],
        'audio': ['.mp3', '.wav', '.m4a', '.flac'],
        'other': ['youtube_urls']
    }
    
    return {
        'success': True,
        'supported_formats': formats,
        'max_file_size_mb': 256,
        'message': 'These are the file formats supported by the MarkItDown conversion service'
    }

