# Face Sorter

A Flask web application that automatically sorts uploaded images by detecting and grouping faces of the same person.

## Features

- Upload multiple images and automatically detect faces
- Group images by person using facial recognition
- Download sorted images as ZIP files (all or by person)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/vatpham/face-sorter.git
cd face-sorter
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install Node.js dependencies and build CSS:
```bash
npm install
npm run build:css
```

5. Set up environment variables:
```bash
cp .env.example .env  # Edit .env and set your FLASK_SECRET_KEY
```

## Running the Application

```bash
python run.py
```

Or using Flask CLI:
```bash
flask run
```

## Docker

Run locally with Docker Compose:

```bash
docker compose up --build
```

- Visit: http://localhost:5000
- Set `FLASK_SECRET_KEY` via `.env`

## Usage

1. Upload multiple images (JPG, JPEG, PNG formats)
2. The app will automatically detect faces and group images by person
3. View results and download sorted images as ZIP files