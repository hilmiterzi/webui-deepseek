from flask import Flask, render_template, request, Response, stream_with_context, jsonify
from flask_cors import CORS
from openai import OpenAI
import os
from dotenv import load_dotenv
import json
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

load_dotenv()

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chats.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    messages = db.relationship('Message', backref='chat', lazy=True, cascade='all, delete-orphan')

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(20), nullable=False)
    content = db.Column(db.Text, nullable=False)
    reasoning_content = db.Column(db.Text, nullable=True)
    chat_id = db.Column(db.Integer, db.ForeignKey('chat.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Initialize database
with app.app_context():
    db.create_all()  # This will only create tables if they don't exist

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/chats', methods=['GET'])
def get_chats():
    try:
        chats = Chat.query.order_by(Chat.created_at.desc()).all()
        return jsonify([{
            'id': chat.id,
            'title': chat.title,
            'created_at': chat.created_at.isoformat(),
            'message_count': len(chat.messages)
        } for chat in chats])
    except Exception as e:
        print(f"Error getting chats: {str(e)}")
        return jsonify([])

@app.route('/api/chats/<int:chat_id>', methods=['GET'])
def get_chat(chat_id):
    try:
        chat = Chat.query.get_or_404(chat_id)
        return jsonify({
            'id': chat.id,
            'title': chat.title,
            'messages': [{
                'id': msg.id,
                'role': msg.role,
                'content': msg.content,
                'reasoning_content': msg.reasoning_content
            } for msg in chat.messages]
        })
    except Exception as e:
        print(f"Error getting chat {chat_id}: {str(e)}")
        return jsonify({'error': 'Chat not found'}), 404

@app.route('/api/chats', methods=['POST'])
def create_chat():
    try:
        data = request.json
        chat = Chat(title=data.get('title', 'New Chat'))
        db.session.add(chat)
        db.session.commit()
        return jsonify({'id': chat.id, 'title': chat.title})
    except Exception as e:
        print(f"Error creating chat: {str(e)}")
        return jsonify({'error': 'Failed to create chat'}), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        messages = data.get('messages', [])
        chat_id = data.get('chat_id')
        
        print(f"Received chat request - chat_id: {chat_id}, message count: {len(messages)}")
        
        if chat_id:
            chat = Chat.query.get(chat_id)
            if not chat:
                return jsonify({'error': 'Chat not found'}), 404
        else:
            # Create new chat with first message as title
            title = messages[0]['content'][:50] + '...' if messages else 'New Chat'
            chat = Chat(title=title)
            db.session.add(chat)
            db.session.commit()
            chat_id = chat.id
            print(f"Created new chat with ID: {chat_id}")
        
        def generate():
            try:
                print("Starting chat completion request...")
                response = client.chat.completions.create(
                    model="deepseek-reasoner",
                    messages=messages,
                    stream=True
                )
                
                reasoning_content = ""
                content = ""
                saved_messages = []
                
                # Save user messages first
                for msg in messages:
                    message = Message(role=msg['role'], content=msg['content'], chat_id=chat_id)
                    db.session.add(message)
                    db.session.commit()
                    saved_messages.append({
                        'id': message.id,
                        'role': message.role,
                        'content': message.content
                    })
                    yield f"data: {json.dumps({'type': 'message_id', 'id': message.id})}\n\n"
                
                print("Processing stream response...")
                for chunk in response:
                    if hasattr(chunk.choices[0].delta, 'reasoning_content') and chunk.choices[0].delta.reasoning_content:
                        reasoning_content += chunk.choices[0].delta.reasoning_content
                        yield f"data: {json.dumps({'type': 'reasoning', 'content': reasoning_content})}\n\n"
                    elif hasattr(chunk.choices[0].delta, 'content') and chunk.choices[0].delta.content:
                        content += chunk.choices[0].delta.content
                        yield f"data: {json.dumps({'type': 'content', 'content': content})}\n\n"
                
                if content:
                    print("Saving assistant message...")
                    message = Message(
                        role='assistant',
                        content=content,
                        reasoning_content=reasoning_content,
                        chat_id=chat_id
                    )
                    db.session.add(message)
                    db.session.commit()
                    yield f"data: {json.dumps({'type': 'message_id', 'id': message.id})}\n\n"
                
                print("Stream completed successfully")
            except Exception as e:
                print(f"Error in generate function: {str(e)}")
                yield f"data: {json.dumps({'type': 'error', 'error': str(e)})}\n\n"
        
        return Response(stream_with_context(generate()), mimetype='text/event-stream')
    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/chats/<int:chat_id>', methods=['PUT'])
def update_chat(chat_id):
    try:
        data = request.json
        chat = Chat.query.get_or_404(chat_id)
        chat.title = data.get('title', chat.title)
        db.session.commit()
        return jsonify({
            'id': chat.id,
            'title': chat.title
        })
    except Exception as e:
        print(f"Error updating chat {chat_id}: {str(e)}")
        return jsonify({'error': 'Failed to update chat'}), 500

@app.route('/api/chats/<int:chat_id>/messages/<int:message_id>', methods=['PUT'])
def update_message(chat_id, message_id):
    try:
        data = request.json
        message = Message.query.filter_by(id=message_id, chat_id=chat_id).first_or_404()
        
        if 'content' in data:
            message.content = data['content']
        if 'reasoning_content' in data:
            message.reasoning_content = data['reasoning_content']
            
        db.session.commit()
        return jsonify({
            'id': message.id,
            'role': message.role,
            'content': message.content,
            'reasoning_content': message.reasoning_content
        })
    except Exception as e:
        print(f"Error updating message {message_id}: {str(e)}")
        return jsonify({'error': 'Failed to update message'}), 500

if __name__ == '__main__':
    app.run(debug=True) 