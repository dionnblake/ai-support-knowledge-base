import shutil
from pathlib import Path
from typing import Union
from app.config import UPLOAD_DIR

def save_uploaded_file(uploaded_file) -> Path:
    """
    Saves a Streamlit uploaded file to the local upload directory.
    
    Args:
        uploaded_file: The Streamlit UploadedFile object.
        
    Returns:
        Path: The path to the saved file on disk.
    """
    upload_path = Path(UPLOAD_DIR)
    upload_path.mkdir(parents=True, exist_ok=True)
    
    target_path = upload_path / uploaded_file.name
    with open(target_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
        
    return target_path

def clear_directory(directory_path: Union[str, Path]) -> None:
    """
    Deletes all files and folders in the specified directory, keeping the directory itself.
    
    Args:
        directory_path (Union[str, Path]): Path to the directory to clear.
    """
    path = Path(directory_path)
    if not path.exists():
        return
        
    for item in path.iterdir():
        try:
            if item.is_file() or item.is_symlink():
                item.unlink()
            elif item.is_dir():
                shutil.rmtree(item)
        except Exception as e:
            # Log or print error; in a real app, use a logger
            print(f"Error deleting {item}: {e}")
