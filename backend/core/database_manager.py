# backend/core/database_manager.py
"""
Ontario Legal AI Database Manager
Handles storage and retrieval of AI analysis results, documents, and legal data
"""

import asyncio
import aiosqlite
import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path

logger = logging.getLogger(__name__)

class DatabaseManager:
    """Comprehensive database manager for Ontario Legal AI System"""
    
    def __init__(self, database_path: str = "data/ontario_legal_ai.db"):
        self.database_path = database_path
        self.is_connected = False
        self._connection = None
        
    async def initialize(self):
        """Initialize database with all required tables"""
        try:
            logger.info("Initializing Ontario Legal AI Database...")
            
            # Ensure data directory exists
            Path(self.database_path).parent.mkdir(parents=True, exist_ok=True)
            
            # Create database connection
            self._connection = await aiosqlite.connect(self.database_path)
            
            # Create all required tables
            await self._create_tables()
            
            self.is_connected = True
            logger.info("✓ Database initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize database: {str(e)}")
            raise
    
    async def _create_tables(self):
        """Create all required database tables"""
        
        # Analysis requests table
        await self._connection.execute("""
            CREATE TABLE IF NOT EXISTS analysis_requests (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                document_type TEXT NOT NULL,
                text_length INTEGER NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                processing_time REAL
            )
        """)
        
        # Analysis results table
        await self._connection.execute("""
            CREATE TABLE IF NOT EXISTS analysis_results (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                document_type TEXT NOT NULL,
                confidence REAL NOT NULL,
                entities TEXT, -- JSON
                requirements TEXT, -- JSON
                compliance_issues TEXT, -- JSON
                recommendations TEXT, -- JSON
                sentiment TEXT, -- JSON
                processing_time REAL NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Generated documents table
        await self._connection.execute("""
            CREATE TABLE IF NOT EXISTS generated_documents (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                document_type TEXT NOT NULL,
                documents TEXT, -- JSON
                ai_recommendations TEXT, -- JSON
                blockchain_hash TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Document generation logs table
        await self._connection.execute("""
            CREATE TABLE IF NOT EXISTS document_generation_logs (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                document_type TEXT NOT NULL,
                document_id TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # User sessions table
        await self._connection.execute("""
            CREATE TABLE IF NOT EXISTS user_sessions (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                session_token TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                expires_at DATETIME NOT NULL,
                last_activity DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Document access permissions table
        await self._connection.execute("""
            CREATE TABLE IF NOT EXISTS document_access (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                document_id TEXT NOT NULL,
                access_level TEXT NOT NULL DEFAULT 'read',
                granted_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        await self._connection.commit()
        logger.info("✓ All database tables created successfully")
    
    async def log_analysis_request(self, user_id: str, document_type: str, text_length: int) -> str:
        """Log an analysis request"""
        request_id = f"req_{datetime.now().timestamp()}"
        
        await self._connection.execute(
            "INSERT INTO analysis_requests (id, user_id, document_type, text_length) VALUES (?, ?, ?, ?)",
            (request_id, user_id, document_type, text_length)
        )
        await self._connection.commit()
        
        return request_id
    
    async def store_analysis(self, user_id: str, analysis_result: Dict[str, Any], processing_time: float) -> str:
        """Store analysis results"""
        document_id = f"doc_{datetime.now().timestamp()}"
        
        await self._connection.execute("""
            INSERT INTO analysis_results 
            (id, user_id, document_type, confidence, entities, requirements, 
             compliance_issues, recommendations, sentiment, processing_time)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            document_id,
            user_id,
            analysis_result.get("document_type", "unknown"),
            analysis_result.get("confidence", 0.0),
            json.dumps(analysis_result.get("entities", [])),
            json.dumps(analysis_result.get("requirements", [])),
            json.dumps(analysis_result.get("compliance_issues", [])),
            json.dumps(analysis_result.get("recommendations", [])),
            json.dumps(analysis_result.get("sentiment", {})),
            processing_time
        ))
        await self._connection.commit()
        
        return document_id
    
    async def store_document(self, user_id: str, document_type: str, documents: Dict[str, Any], 
                           ai_recommendations: List[str]) -> str:
        """Store generated document"""
        document_id = f"gen_{datetime.now().timestamp()}"
        
        await self._connection.execute("""
            INSERT INTO generated_documents 
            (id, user_id, document_type, documents, ai_recommendations)
            VALUES (?, ?, ?, ?, ?)
        """, (
            document_id,
            user_id,
            document_type,
            json.dumps(documents),
            json.dumps(ai_recommendations)
        ))
        await self._connection.commit()
        
        # Grant access to the user
        await self._connection.execute("""
            INSERT INTO document_access (id, user_id, document_id, access_level)
            VALUES (?, ?, ?, ?)
        """, (f"access_{document_id}", user_id, document_id, "full"))
        await self._connection.commit()
        
        return document_id
    
    async def log_document_generation(self, user_id: str, document_type: str, document_id: str):
        """Log document generation activity"""
        log_id = f"log_{datetime.now().timestamp()}"
        
        await self._connection.execute("""
            INSERT INTO document_generation_logs (id, user_id, document_type, document_id)
            VALUES (?, ?, ?, ?)
        """, (log_id, user_id, document_type, document_id))
        await self._connection.commit()
    
    async def verify_document_access(self, user_id: str, document_id: str) -> bool:
        """Verify user has access to document"""
        cursor = await self._connection.execute("""
            SELECT COUNT(*) FROM document_access 
            WHERE user_id = ? AND document_id = ?
        """, (user_id, document_id))
        
        result = await cursor.fetchone()
        return result[0] > 0
    
    async def get_document(self, document_id: str, format: str) -> Optional[Dict[str, Any]]:
        """Get document by ID and format"""
        cursor = await self._connection.execute("""
            SELECT documents FROM generated_documents WHERE id = ?
        """, (document_id,))
        
        result = await cursor.fetchone()
        if not result:
            return None
        
        documents = json.loads(result[0])
        
        # Return appropriate format
        if format == "pdf" and "pdf_content" in documents:
            return {
                "filename": f"{document_id}.pdf",
                "content_type": "application/pdf",
                "content": documents["pdf_content"]
            }
        elif format == "docx" and "docx_content" in documents:
            return {
                "filename": f"{document_id}.docx",
                "content_type": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                "content": documents["docx_content"]
            }
        
        return None
    
    async def get_user_documents(self, user_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Get user's documents"""
        cursor = await self._connection.execute("""
            SELECT gd.id, gd.document_type, gd.created_at 
            FROM generated_documents gd
            JOIN document_access da ON gd.id = da.document_id
            WHERE da.user_id = ?
            ORDER BY gd.created_at DESC
            LIMIT ?
        """, (user_id, limit))
        
        results = await cursor.fetchall()
        return [
            {
                "document_id": row[0],
                "document_type": row[1],
                "created_at": row[2]
            }
            for row in results
        ]
    
    async def get_analysis_history(self, user_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Get user's analysis history"""
        cursor = await self._connection.execute("""
            SELECT id, document_type, confidence, processing_time, timestamp
            FROM analysis_results
            WHERE user_id = ?
            ORDER BY timestamp DESC
            LIMIT ?
        """, (user_id, limit))
        
        results = await cursor.fetchall()
        return [
            {
                "analysis_id": row[0],
                "document_type": row[1],
                "confidence": row[2],
                "processing_time": row[3],
                "timestamp": row[4]
            }
            for row in results
        ]
    
    def is_connected(self) -> bool:
        """Check if database is connected"""
        return self.is_connected and self._connection is not None
    
    async def close(self):
        """Close database connection"""
        if self._connection:
            await self._connection.close()
            self.is_connected = False
            logger.info("Database connection closed")