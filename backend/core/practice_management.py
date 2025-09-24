# backend/core/practice_management.py
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import logging
import asyncio
import uuid
from dataclasses import dataclass
import json
import aiosqlite

logger = logging.getLogger(__name__)

@dataclass
class ClientMatter:
    matter_id: str
    client_name: str
    matter_type: str
    status: str
    open_date: datetime
    close_date: Optional[datetime]
    responsible_lawyer: str
    estimated_value: float
    time_entries: List[Dict[str, Any]]
    documents: List[Dict[str, Any]]

class OntarioPracticeManager:
    """Comprehensive practice management system for Ontario legal practitioners"""
    
    def __init__(self, database_path: str = "data/practice_management.db"):
        self.database_path = database_path
        self.is_initialized = False
    
    async def initialize(self):
        """Initialize the practice management system"""
        try:
            await self._setup_database()
            self.is_initialized = True
            logger.info("✓ Ontario Practice Manager initialized")
        except Exception as e:
            logger.error(f"Practice management initialization failed: {str(e)}")
            raise
    
    async def _setup_database(self):
        """Setup database tables for practice management"""
        async with aiosqlite.connect(self.database_path) as db:
            # Clients table
            await db.execute("""
                CREATE TABLE IF NOT EXISTS clients (
                    client_id TEXT PRIMARY KEY,
                    full_name TEXT NOT NULL,
                    preferred_name TEXT,
                    email TEXT,
                    phone TEXT,
                    address TEXT,
                    date_of_birth DATE,
                    sin_number TEXT,
                    client_type TEXT DEFAULT 'individual',
                    status TEXT DEFAULT 'active',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    created_by TEXT,
                    notes TEXT,
                    emergency_contact TEXT,
                    preferred_language TEXT DEFAULT 'English'
                )
            """)
            
            # Matters table
            await db.execute("""
                CREATE TABLE IF NOT EXISTS matters (
                    matter_id TEXT PRIMARY KEY,
                    client_id TEXT NOT NULL,
                    matter_name TEXT NOT NULL,
                    matter_type TEXT NOT NULL,
                    matter_description TEXT,
                    status TEXT DEFAULT 'active',
                    responsible_lawyer TEXT NOT NULL,
                    assistant_assigned TEXT,
                    opened_date DATE NOT NULL,
                    closed_date DATE,
                    estimated_value DECIMAL(10,2),
                    actual_value DECIMAL(10,2),
                    hourly_rate DECIMAL(8,2),
                    flat_fee DECIMAL(10,2),
                    billing_type TEXT DEFAULT 'hourly',
                    priority TEXT DEFAULT 'normal',
                    statute_of_limitations DATE,
                    court_file_number TEXT,
                    opposing_counsel TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (client_id) REFERENCES clients (client_id)
                )
            """)
            
            # Time entries table
            await db.execute("""
                CREATE TABLE IF NOT EXISTS time_entries (
                    entry_id TEXT PRIMARY KEY,
                    matter_id TEXT NOT NULL,
                    lawyer_id TEXT NOT NULL,
                    date_worked DATE NOT NULL,
                    start_time TIME,
                    end_time TIME,
                    duration_minutes INTEGER NOT NULL,
                    description TEXT NOT NULL,
                    activity_type TEXT NOT NULL,
                    billable BOOLEAN DEFAULT TRUE,
                    hourly_rate DECIMAL(8,2),
                    total_charge DECIMAL(8,2),
                    status TEXT DEFAULT 'draft',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (matter_id) REFERENCES matters (matter_id)
                )
            """)
            
            # Document matter associations
            await db.execute("""
                CREATE TABLE IF NOT EXISTS matter_documents (
                    association_id TEXT PRIMARY KEY,
                    matter_id TEXT NOT NULL,
                    document_id TEXT NOT NULL,
                    document_type TEXT NOT NULL,
                    document_name TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    created_by TEXT,
                    FOREIGN KEY (matter_id) REFERENCES matters (matter_id)
                )
            """)
            
            # Legal deadlines and reminders
            await db.execute("""
                CREATE TABLE IF NOT EXISTS deadlines (
                    deadline_id TEXT PRIMARY KEY,
                    matter_id TEXT NOT NULL,
                    deadline_type TEXT NOT NULL,
                    description TEXT NOT NULL,
                    due_date DATE NOT NULL,
                    reminder_date DATE,
                    priority TEXT DEFAULT 'medium',
                    status TEXT DEFAULT 'pending',
                    responsible_lawyer TEXT NOT NULL,
                    completed_at TIMESTAMP,
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (matter_id) REFERENCES matters (matter_id)
                )
            """)
            
            # Billing and invoicing
            await db.execute("""
                CREATE TABLE IF NOT EXISTS invoices (
                    invoice_id TEXT PRIMARY KEY,
                    matter_id TEXT NOT NULL,
                    client_id TEXT NOT NULL,
                    invoice_number TEXT NOT NULL UNIQUE,
                    invoice_date DATE NOT NULL,
                    due_date DATE NOT NULL,
                    total_amount DECIMAL(10,2) NOT NULL,
                    hst_amount DECIMAL(10,2) DEFAULT 0,
                    amount_paid DECIMAL(10,2) DEFAULT 0,
                    status TEXT DEFAULT 'draft',
                    payment_terms TEXT DEFAULT '30 days',
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    created_by TEXT,
                    FOREIGN KEY (matter_id) REFERENCES matters (matter_id),
                    FOREIGN KEY (client_id) REFERENCES clients (client_id)
                )
            """)
            
            await db.commit()
    
    async def create_client(self, client_data: Dict[str, Any]) -> str:
        """Create a new client record"""
        try:
            client_id = f"client_{uuid.uuid4().hex[:8]}"
            
            async with aiosqlite.connect(self.database_path) as db:
                await db.execute("""
                    INSERT INTO clients 
                    (client_id, full_name, preferred_name, email, phone, address, 
                     date_of_birth, client_type, created_by, notes, emergency_contact, 
                     preferred_language)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    client_id,
                    client_data["full_name"],
                    client_data.get("preferred_name"),
                    client_data.get("email"),
                    client_data.get("phone"),
                    client_data.get("address"),
                    client_data.get("date_of_birth"),
                    client_data.get("client_type", "individual"),
                    client_data.get("created_by"),
                    client_data.get("notes"),
                    client_data.get("emergency_contact"),
                    client_data.get("preferred_language", "English")
                ))
                await db.commit()
            
            logger.info(f"Client created: {client_id}")
            return client_id
            
        except Exception as e:
            logger.error(f"Failed to create client: {str(e)}")
            raise
    
    async def create_matter(self, matter_data: Dict[str, Any]) -> str:
        """Create a new legal matter"""
        try:
            matter_id = f"matter_{uuid.uuid4().hex[:8]}"
            
            async with aiosqlite.connect(self.database_path) as db:
                await db.execute("""
                    INSERT INTO matters 
                    (matter_id, client_id, matter_name, matter_type, matter_description,
                     responsible_lawyer, assistant_assigned, opened_date, estimated_value,
                     hourly_rate, flat_fee, billing_type, priority, statute_of_limitations,
                     court_file_number, opposing_counsel)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    matter_id,
                    matter_data["client_id"],
                    matter_data["matter_name"],
                    matter_data["matter_type"],
                    matter_data.get("matter_description"),
                    matter_data["responsible_lawyer"],
                    matter_data.get("assistant_assigned"),
                    matter_data.get("opened_date", datetime.now().date()),
                    matter_data.get("estimated_value", 0),
                    matter_data.get("hourly_rate"),
                    matter_data.get("flat_fee"),
                    matter_data.get("billing_type", "hourly"),
                    matter_data.get("priority", "normal"),
                    matter_data.get("statute_of_limitations"),
                    matter_data.get("court_file_number"),
                    matter_data.get("opposing_counsel")
                ))
                await db.commit()
            
            logger.info(f"Matter created: {matter_id}")
            return matter_id
            
        except Exception as e:
            logger.error(f"Failed to create matter: {str(e)}")
            raise
    
    async def add_time_entry(self, time_entry: Dict[str, Any]) -> str:
        """Add a time entry for billing"""
        try:
            entry_id = f"time_{uuid.uuid4().hex[:8]}"
            
            # Calculate total charge
            duration_hours = time_entry["duration_minutes"] / 60.0
            hourly_rate = time_entry.get("hourly_rate", 0)
            total_charge = duration_hours * hourly_rate if time_entry.get("billable", True) else 0
            
            async with aiosqlite.connect(self.database_path) as db:
                await db.execute("""
                    INSERT INTO time_entries 
                    (entry_id, matter_id, lawyer_id, date_worked, start_time, end_time,
                     duration_minutes, description, activity_type, billable, hourly_rate,
                     total_charge, status)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    entry_id,
                    time_entry["matter_id"],
                    time_entry["lawyer_id"],
                    time_entry["date_worked"],
                    time_entry.get("start_time"),
                    time_entry.get("end_time"),
                    time_entry["duration_minutes"],
                    time_entry["description"],
                    time_entry["activity_type"],
                    time_entry.get("billable", True),
                    hourly_rate,
                    total_charge,
                    time_entry.get("status", "draft")
                ))
                await db.commit()
            
            logger.info(f"Time entry added: {entry_id}")
            return entry_id
            
        except Exception as e:
            logger.error(f"Failed to add time entry: {str(e)}")
            raise
    
    async def associate_document_with_matter(self, matter_id: str, document_id: str, 
                                           document_type: str, document_name: str,
                                           created_by: str) -> str:
        """Associate a document with a legal matter"""
        try:
            association_id = f"assoc_{uuid.uuid4().hex[:8]}"
            
            async with aiosqlite.connect(self.database_path) as db:
                await db.execute("""
                    INSERT INTO matter_documents 
                    (association_id, matter_id, document_id, document_type, 
                     document_name, created_by)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    association_id,
                    matter_id,
                    document_id,
                    document_type,
                    document_name,
                    created_by
                ))
                await db.commit()
            
            logger.info(f"Document associated with matter: {association_id}")
            return association_id
            
        except Exception as e:
            logger.error(f"Failed to associate document with matter: {str(e)}")
            raise
    
    async def add_deadline(self, deadline_data: Dict[str, Any]) -> str:
        """Add a legal deadline or reminder"""
        try:
            deadline_id = f"deadline_{uuid.uuid4().hex[:8]}"
            
            async with aiosqlite.connect(self.database_path) as db:
                await db.execute("""
                    INSERT INTO deadlines 
                    (deadline_id, matter_id, deadline_type, description, due_date,
                     reminder_date, priority, responsible_lawyer, notes)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    deadline_id,
                    deadline_data["matter_id"],
                    deadline_data["deadline_type"],
                    deadline_data["description"],
                    deadline_data["due_date"],
                    deadline_data.get("reminder_date"),
                    deadline_data.get("priority", "medium"),
                    deadline_data["responsible_lawyer"],
                    deadline_data.get("notes")
                ))
                await db.commit()
            
            logger.info(f"Deadline added: {deadline_id}")
            return deadline_id
            
        except Exception as e:
            logger.error(f"Failed to add deadline: {str(e)}")
            raise
    
    async def get_client_matters(self, client_id: str) -> List[Dict[str, Any]]:
        """Get all matters for a specific client"""
        try:
            async with aiosqlite.connect(self.database_path) as db:
                cursor = await db.execute("""
                    SELECT * FROM matters WHERE client_id = ? ORDER BY opened_date DESC
                """, (client_id,))
                rows = await cursor.fetchall()
                
                matters = []
                for row in rows:
                    columns = [description[0] for description in cursor.description]
                    matter = dict(zip(columns, row))
                    matters.append(matter)
                
                return matters
                
        except Exception as e:
            logger.error(f"Failed to get client matters: {str(e)}")
            raise
    
    async def get_time_summary(self, matter_id: str, start_date: str = None, 
                             end_date: str = None) -> Dict[str, Any]:
        """Get time summary for a matter"""
        try:
            query = "SELECT * FROM time_entries WHERE matter_id = ?"
            params = [matter_id]
            
            if start_date:
                query += " AND date_worked >= ?"
                params.append(start_date)
            
            if end_date:
                query += " AND date_worked <= ?"
                params.append(end_date)
            
            async with aiosqlite.connect(self.database_path) as db:
                db.row_factory = aiosqlite.Row  # Enable column access by name
                cursor = await db.execute(query, params)
                rows = await cursor.fetchall()
                
                total_minutes = 0
                total_billable_amount = 0.0
                billable_minutes = 0
                
                for row in rows:
                    duration_minutes = row['duration_minutes'] or 0
                    total_charge = float(row['total_charge'] or 0)
                    
                    total_minutes += duration_minutes
                    if row['billable']:  # billable
                        billable_minutes += duration_minutes
                        total_billable_amount += total_charge
                
                return {
                    "total_hours": round(total_minutes / 60.0, 2),
                    "billable_hours": round(billable_minutes / 60.0, 2),
                    "total_billable_amount": total_billable_amount,
                    "entry_count": len(rows)
                }
                
        except Exception as e:
            logger.error(f"Failed to get time summary: {str(e)}")
            raise
    
    async def get_upcoming_deadlines(self, lawyer_id: str, days_ahead: int = 30) -> List[Dict[str, Any]]:
        """Get upcoming deadlines for a lawyer"""
        try:
            future_date = datetime.now() + timedelta(days=days_ahead)
            
            async with aiosqlite.connect(self.database_path) as db:
                cursor = await db.execute("""
                    SELECT d.*, m.matter_name, c.full_name as client_name
                    FROM deadlines d
                    JOIN matters m ON d.matter_id = m.matter_id
                    JOIN clients c ON m.client_id = c.client_id
                    WHERE d.responsible_lawyer = ? 
                      AND d.due_date <= ? 
                      AND d.status = 'pending'
                    ORDER BY d.due_date ASC
                """, (lawyer_id, future_date.date()))
                
                rows = await cursor.fetchall()
                columns = [description[0] for description in cursor.description]
                
                deadlines = []
                for row in rows:
                    deadline = dict(zip(columns, row))
                    deadlines.append(deadline)
                
                return deadlines
                
        except Exception as e:
            logger.error(f"Failed to get upcoming deadlines: {str(e)}")
            raise
    
    async def generate_invoice(self, invoice_data: Dict[str, Any]) -> str:
        """Generate an invoice for a matter"""
        try:
            invoice_id = f"invoice_{uuid.uuid4().hex[:8]}"
            
            # Generate invoice number
            current_date = datetime.now()
            invoice_number = f"INV-{current_date.year}-{invoice_id[-4:]}"
            
            # Calculate HST (13% for Ontario)
            total_amount = invoice_data["total_amount"]
            hst_amount = total_amount * 0.13
            
            async with aiosqlite.connect(self.database_path) as db:
                await db.execute("""
                    INSERT INTO invoices 
                    (invoice_id, matter_id, client_id, invoice_number, invoice_date,
                     due_date, total_amount, hst_amount, payment_terms, notes, created_by)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    invoice_id,
                    invoice_data["matter_id"],
                    invoice_data["client_id"],
                    invoice_number,
                    invoice_data.get("invoice_date", datetime.now().date()),
                    invoice_data.get("due_date", (datetime.now() + timedelta(days=30)).date()),
                    total_amount,
                    hst_amount,
                    invoice_data.get("payment_terms", "30 days"),
                    invoice_data.get("notes"),
                    invoice_data.get("created_by")
                ))
                await db.commit()
            
            logger.info(f"Invoice generated: {invoice_id}")
            return invoice_id
            
        except Exception as e:
            logger.error(f"Failed to generate invoice: {str(e)}")
            raise
    
    def is_ready(self) -> bool:
        """Check if practice manager is ready"""
        return self.is_initialized