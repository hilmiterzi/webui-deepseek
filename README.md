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

MIT License

Copyright (c) 2024 Hilmis WebUI

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE. 