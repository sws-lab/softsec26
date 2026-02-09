# Photo App

A simple Flask web application that allows users to upload and manage their photos, with public and private visibility options.

## Features

- User registration and authentication
- Upload images (supported formats: PNG, JPG, JPEG, GIF)
- Toggle image visibility between public and private
- View all public images
- View specific user's public images
- Responsive design using Bootstrap

## Setup

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

4. Open your browser and navigate to `http://localhost:5000`

## Testing

Run the tests with:
```bash
pytest -v
```

## Usage

1. Register a new account or login with existing credentials
2. Upload images through your dashboard
3. Toggle image visibility using the buttons on your dashboard
4. View public images on the home page
5. Click on usernames to view their public images

## Directory Structure

- `/static/uploads/` - Stores uploaded images
- `/templates/` - Contains HTML templates
- `app.py` - Main application file
- `requirements.txt` - Python dependencies

## Security Notes

- Uploaded files are validated for type and size
- Private images are only accessible to their owners
- Passwords are hashed before storage
- File names are sanitized before storage

## License

MIT License 