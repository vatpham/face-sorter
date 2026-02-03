import pytest
from app.utils.file_utils import allowed_file

@pytest.mark.parametrize("filename, expected", [
    ("image.png", True),
    ("image.gif", False),
    ("image.jpg", True),
    ("image.tif", False),
    ("image.webp", False),
    ("image.jpeg", True),
    ("image.svg", False),
])
def test_allowed_file(filename, expected):
    assert allowed_file(filename) == expected
    



