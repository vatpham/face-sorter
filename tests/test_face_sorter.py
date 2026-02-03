from pathlib import Path
import shutil

import pytest
from app.utils.face_sorter import sort_images
from app.utils.file_utils import allowed_file


def test_sort_images():
    base = Path(__file__).parent / "test_images"
    input_dir, output_dir = base / "input", base / "output"
    total_faces = sort_images(str(input_dir), str(output_dir))
    assert total_faces == 2
    

