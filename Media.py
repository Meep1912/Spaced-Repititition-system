import hashlib
import os
import shutil
from PIL import Image   # pip install pillow

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MEDIA_DIR = os.path.join(BASE_DIR, "Data_Files", "media")


def import_media(source_path):
    #Copy a file into the media folder under a hash-based name.
    #Returns the new filename, which is what you store in the card.

    # reject files that aren't real images (raises PIL.UnidentifiedImageError,
    # which is an OSError, so done_button's `except OSError` catches it)
    with Image.open(source_path) as img:
        img.verify()

    os.makedirs(MEDIA_DIR, exist_ok=True)

    with open(source_path, "rb") as f:
        digest = hashlib.sha256(f.read()).hexdigest()[:16]

    ext = os.path.splitext(source_path)[1].lower()   # ".png", ".jpg"
    name = digest + ext
    dest = os.path.join(MEDIA_DIR, name)

    if not os.path.exists(dest):                     # same image twice = stored once
        shutil.copy2(source_path, dest)

    return name