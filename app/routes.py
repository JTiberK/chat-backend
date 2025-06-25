from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from .models import User, Conversation, Message
from . import db
import google.generativeai as genai
from datetime import datetime

main = Blueprint('main', __name__)

@main.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    user = User.query.filter_by(username=username).first()
    if not user or not user.password == password:  # In production, use proper password hashing
        return jsonify({"message": "Invalid credentials"}), 401
    
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)

@main.route('/api/chat', methods=['POST'])
@jwt_required()
def chat():
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    if not user:
        return jsonify({"message": "User not found"}), 404
    
    data = request.get_json()
    message = data.get('message')
    
    # Initialize Gemini
    genai.configure(api_key=current_app.config['GEMINI_API_KEY'])
    model = genai.GenerativeModel('gemini-pro')
    
    # Get or create conversation
    conversation = Conversation.query.filter_by(user_id=user.id).order_by(Conversation.created_at.desc()).first()
    if not conversation:
        conversation = Conversation(user_id=user.id, title=f"Conversation {datetime.now().strftime('%Y-%m-%d')}")
        db.session.add(conversation)
        db.session.commit()
    
    # Save user message
    user_msg = Message(conversation_id=conversation.id, content=message, is_user=True)
    db.session.add(user_msg)
    
    # Get AI response
    try:
        response = model.generate_content(message)
        ai_response = response.text
        
        # Save AI response
        ai_msg = Message(conversation_id=conversation.id, content=ai_response, is_user=False)
        db.session.add(ai_msg)
        db.session.commit()
        
        return jsonify({"response": ai_response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route('/api/conversations', methods=['GET'])
@jwt_required()
def get_conversations():
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    if not user:
        return jsonify({"message": "User not found"}), 404
    
    conversations = Conversation.query.filter_by(user_id=user.id).all()
    result = [{
        "id": conv.id,
        "title": conv.title,
        "created_at": conv.created_at.isoformat(),
        "message_count": len(conv.messages)
    } for conv in conversations]
    
    return jsonify(result)
