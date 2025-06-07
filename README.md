# Hilmis WebUI

A modern web interface for AI chat interactions, built with Flask and featuring real-time streaming responses.

## Features

- Real-time chat interface with streaming responses
- Syntax highlighting for code blocks
- Chat history management
- Dark theme UI
- Markdown support
- Code editing capabilities

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd hilmis-webui
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
```

3. Activate the virtual environment:
- Windows:
```bash
.\venv\Scripts\activate
```
- Linux/Mac:
```bash
source venv/bin/activate
```

4. Install the required packages:
```bash
pip install -r requirements.txt
```

5. Create a `.env` file in the root directory with your API key:
```
DEEPSEEK_API_KEY=your_api_key_here
```

## Running the Application

1. Make sure your virtual environment is activated

2. Start the Flask server:
```bash
python app.py
```

3. Open your web browser and navigate to:
```
http://localhost:5000
```

## Project Structure

- `app.py` - Main Flask application
- `templates/` - HTML templates
  - `index.html` - Main chat interface
- `requirements.txt` - Python dependencies
- `.env` - Environment variables (create this file)

## Dependencies

- Flask - Web framework
- Flask-CORS - Cross-origin resource sharing
- Flask-SQLAlchemy - Database ORM
- OpenAI - API client
- python-dotenv - Environment variable management

## Development

The application uses:
- Flask for the backend
- SQLite for the database
- Prism.js for code syntax highlighting
- Marked.js for Markdown rendering

## License

[Your License Here] 