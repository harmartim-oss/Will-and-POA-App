from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    document_type = db.Column(db.String(50), nullable=False)  # 'will', 'poa_property', 'poa_care'
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=True)  # JSON string of document data
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_completed = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f'<Document {self.title}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'document_type': self.document_type,
            'title': self.title,
            'content': json.loads(self.content) if self.content else {},
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'is_completed': self.is_completed
        }
    
    def set_content(self, content_dict):
        self.content = json.dumps(content_dict)
    
    def get_content(self):
        return json.loads(self.content) if self.content else {}

class DocumentTemplate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    document_type = db.Column(db.String(50), nullable=False)
    template_name = db.Column(db.String(100), nullable=False)
    template_content = db.Column(db.Text, nullable=False)  # Template with placeholders
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<DocumentTemplate {self.template_name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'document_type': self.document_type,
            'template_name': self.template_name,
            'template_content': self.template_content,
            'created_at': self.created_at.isoformat()
        }

class AIsuggestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    document_id = db.Column(db.Integer, db.ForeignKey('document.id'), nullable=False)
    section = db.Column(db.String(100), nullable=False)
    original_text = db.Column(db.Text, nullable=True)
    suggested_text = db.Column(db.Text, nullable=False)
    suggestion_type = db.Column(db.String(50), nullable=False)  # 'improvement', 'legal_compliance', 'clarity'
    is_accepted = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    document = db.relationship('Document', backref=db.backref('ai_suggestions', lazy=True))
    
    def __repr__(self):
        return f'<AIsuggestion {self.section}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'document_id': self.document_id,
            'section': self.section,
            'original_text': self.original_text,
            'suggested_text': self.suggested_text,
            'suggestion_type': self.suggestion_type,
            'is_accepted': self.is_accepted,
            'created_at': self.created_at.isoformat()
        }

