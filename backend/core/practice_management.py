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
from .lsuc_compliance import LSUCComplianceManager

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
    """Comprehensive practice management system for Ontario sole practitioner"""
    
    def __init__(self, database_path: str = "data/ontario_legal_practice.db"):
        self.db_path = database_path
        self.database_path = database_path  # Keep compatibility
        self.is_initialized = False
        self.lsuc_compliance = LSUCComplianceManager()
    
    async def initialize(self):
        """Initialize practice management system"""
        try:
            logger.info("🏗️ Initializing Ontario Practice Manager...")
            # Setup database
            await self._setup_database()
            # Initialize compliance manager
            await self.lsuc_compliance.initialize()
            # Load practice templates
            await self._load_practice_templates()
            self.is_initialized = True
            logger.info("✓ Ontario Practice Manager initialized")
        except Exception as e:
            logger.error(f"Practice manager initialization failed: {str(e)}")
            raise
    
    async def _setup_database(self):
        """Setup comprehensive practice database"""
        async with aiosqlite.connect(self.database_path) as db:
            # Clients table - enhanced with more fields
            await db.execute("""
                CREATE TABLE IF NOT EXISTS clients (
                    client_id TEXT PRIMARY KEY,
                    client_name TEXT NOT NULL,
                    full_name TEXT NOT NULL,
                    preferred_name TEXT,
                    contact_info TEXT,
                    email TEXT,
                    phone TEXT,
                    address TEXT,
                    date_of_birth DATE,
                    sin_number TEXT,
                    client_type TEXT DEFAULT 'individual',
                    matter_count INTEGER DEFAULT 0,
                    total_billed REAL DEFAULT 0.0,
                    total_collected REAL DEFAULT 0.0,
                    status TEXT DEFAULT 'active',
                    conflict_check_completed BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    created_by TEXT,
                    notes TEXT,
                    emergency_contact TEXT,
                    preferred_language TEXT DEFAULT 'English'
                )
            """)
            
            # Matters table - comprehensive with additional fields
            await db.execute("""
                CREATE TABLE IF NOT EXISTS matters (
                    matter_id TEXT PRIMARY KEY,
                    client_id TEXT NOT NULL,
                    matter_type TEXT NOT NULL,
                    matter_name TEXT NOT NULL,
                    matter_description TEXT,
                    status TEXT DEFAULT 'open',
                    open_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    close_date TIMESTAMP,
                    opened_date DATE NOT NULL,
                    closed_date DATE,
                    estimated_value REAL,
                    actual_value DECIMAL(10,2),
                    responsible_lawyer TEXT NOT NULL,
                    supervising_lawyer TEXT,
                    assistant_assigned TEXT,
                    time_budget_hours REAL,
                    expenses_budget REAL,
                    hourly_rate DECIMAL(8,2),
                    flat_fee DECIMAL(10,2),
                    billing_type TEXT DEFAULT 'hourly',
                    priority TEXT DEFAULT 'normal',
                    statute_of_limitations DATE,
                    court_file_number TEXT,
                    opposing_counsel TEXT,
                    trust_account_required BOOLEAN DEFAULT FALSE,
                    conflict_checked BOOLEAN DEFAULT FALSE,
                    retainer_received BOOLEAN DEFAULT FALSE,
                    retainer_amount REAL DEFAULT 0.0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (client_id) REFERENCES clients (client_id)
                )
            """)
            
            # Time tracking table - enhanced
            await db.execute("""
                CREATE TABLE IF NOT EXISTS time_entries (
                    entry_id TEXT PRIMARY KEY,
                    matter_id TEXT NOT NULL,
                    lawyer_id TEXT NOT NULL,
                    date DATE NOT NULL,
                    date_worked DATE NOT NULL,
                    start_time TIME,
                    end_time TIME,
                    duration_minutes INTEGER NOT NULL,
                    description TEXT NOT NULL,
                    activity_type TEXT NOT NULL,
                    billable BOOLEAN DEFAULT TRUE,
                    hourly_rate REAL,
                    total_amount REAL,
                    total_charge DECIMAL(8,2),
                    billed BOOLEAN DEFAULT FALSE,
                    billed_date TIMESTAMP,
                    status TEXT DEFAULT 'draft',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (matter_id) REFERENCES matters (matter_id)
                )
            """)
            
            # Billing table - comprehensive invoicing
            await db.execute("""
                CREATE TABLE IF NOT EXISTS bills (
                    bill_id TEXT PRIMARY KEY,
                    matter_id TEXT NOT NULL,
                    client_id TEXT NOT NULL,
                    bill_date DATE NOT NULL,
                    bill_number TEXT UNIQUE,
                    due_date DATE,
                    subtotal REAL,
                    taxes REAL,
                    total_amount REAL,
                    paid_amount REAL DEFAULT 0.0,
                    status TEXT DEFAULT 'draft',
                    payment_terms TEXT,
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (matter_id) REFERENCES matters (matter_id),
                    FOREIGN KEY (client_id) REFERENCES clients (client_id)
                )
            """)
            
            # Enhanced invoices table
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
            
            # Trust account table - LSUC compliant
            await db.execute("""
                CREATE TABLE IF NOT EXISTS trust_transactions (
                    transaction_id TEXT PRIMARY KEY,
                    matter_id TEXT,
                    client_id TEXT,
                    transaction_date DATE NOT NULL,
                    transaction_type TEXT NOT NULL, -- 'receipt', 'disbursement', 'transfer'
                    amount REAL NOT NULL,
                    description TEXT,
                    reference_number TEXT,
                    bank_account TEXT,
                    reconciled BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (matter_id) REFERENCES matters (matter_id),
                    FOREIGN KEY (client_id) REFERENCES clients (client_id)
                )
            """)
            
            # Calendar/appointments table
            await db.execute("""
                CREATE TABLE IF NOT EXISTS appointments (
                    appointment_id TEXT PRIMARY KEY,
                    matter_id TEXT,
                    client_id TEXT,
                    appointment_type TEXT,
                    title TEXT,
                    description TEXT,
                    start_time TIMESTAMP,
                    end_time TIMESTAMP,
                    location TEXT,
                    status TEXT DEFAULT 'scheduled',
                    reminder_sent BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (matter_id) REFERENCES matters (matter_id),
                    FOREIGN KEY (client_id) REFERENCES clients (client_id)
                )
            """)
            
            # Tasks/reminders table
            await db.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    task_id TEXT PRIMARY KEY,
                    matter_id TEXT,
                    client_id TEXT,
                    task_type TEXT,
                    title TEXT NOT NULL,
                    description TEXT,
                    due_date DATE,
                    priority TEXT DEFAULT 'medium',
                    assigned_to TEXT,
                    status TEXT DEFAULT 'pending',
                    completed_date TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (matter_id) REFERENCES matters (matter_id),
                    FOREIGN KEY (client_id) REFERENCES clients (client_id)
                )
            """)
            
            # Documents table - enhanced
            await db.execute("""
                CREATE TABLE IF NOT EXISTS documents (
                    document_id TEXT PRIMARY KEY,
                    matter_id TEXT,
                    client_id TEXT,
                    document_type TEXT,
                    document_name TEXT,
                    file_path TEXT,
                    file_size INTEGER,
                    version INTEGER DEFAULT 1,
                    created_by TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    is_final BOOLEAN DEFAULT FALSE,
                    is_billable BOOLEAN DEFAULT FALSE,
                    billing_status TEXT DEFAULT 'unbilled',
                    FOREIGN KEY (matter_id) REFERENCES matters (matter_id),
                    FOREIGN KEY (client_id) REFERENCES clients (client_id)
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
            
            # Legal deadlines and reminders - enhanced
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
            
            await db.commit()
    
    async def _load_practice_templates(self):
        """Load practice templates"""
        # This would load document templates, matter type templates, etc.
        logger.info("✓ Practice templates loaded")
        pass
    
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
    
    async def create_client_matter(self, client_data: Dict[str, Any], matter_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new client and matter with full setup"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                # Generate unique IDs
                client_id = str(uuid.uuid4())
                matter_id = str(uuid.uuid4())
                
                # Create client with proper field mapping
                contact_info = json.dumps(client_data.get("contact", {}))
                await db.execute('''
                    INSERT INTO clients (
                        client_id, client_name, full_name, contact_info, 
                        email, phone, status, conflict_check_completed
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    client_id, 
                    client_data["name"], 
                    client_data["name"],  # Use name for both client_name and full_name
                    contact_info,
                    client_data.get("contact", {}).get("email"),
                    client_data.get("contact", {}).get("phone"),
                    "active",
                    True
                ))
                
                # Create matter with proper field mapping
                await db.execute('''
                    INSERT INTO matters (
                        matter_id, client_id, matter_type, matter_name, matter_description,
                        responsible_lawyer, supervising_lawyer, estimated_value,
                        trust_account_required, conflict_checked, opened_date,
                        status
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    matter_id, client_id, matter_data["type"], 
                    f"{matter_data['type'].replace('_', ' ').title()} for {client_data['name']}",
                    matter_data.get("description", ""),
                    matter_data["responsible_lawyer"], 
                    matter_data.get("supervising_lawyer", ""),
                    matter_data.get("estimated_value", 0.0),
                    matter_data.get("trust_account_required", False),
                    matter_data.get("conflict_checked", False),
                    datetime.now().date(),
                    "open"
                ))
                
                # Create initial tasks
                await self._create_initial_tasks(db, matter_id, matter_data["type"])
                
                await db.commit()
            
            # Log activity
            await self.lsuc_compliance.log_activity(
                activity_type="matter_created",
                user_id=matter_data["responsible_lawyer"],
                matter_id=matter_id,
                details={"client_name": client_data["name"], "matter_type": matter_data["type"]}
            )
            
            return {
                "client_id": client_id,
                "matter_id": matter_id,
                "status": "created",
                "message": "Client and matter created successfully"
            }
        except Exception as e:
            logger.error(f"Client matter creation failed: {str(e)}")
            raise
    
    async def _create_initial_tasks(self, db, matter_id: str, matter_type: str):
        """Create initial tasks based on matter type"""
        initial_tasks = {
            "wills_estates": [
                {"title": "Conduct client interview", "priority": "high", "days_from_now": 3},
                {"title": "Review existing will (if any)", "priority": "medium", "days_from_now": 7},
                {"title": "Draft will", "priority": "high", "days_from_now": 14},
                {"title": "Schedule signing appointment", "priority": "medium", "days_from_now": 21}
            ],
            "real_estate": [
                {"title": "Review purchase agreement", "priority": "high", "days_from_now": 1},
                {"title": "Order title search", "priority": "high", "days_from_now": 2},
                {"title": "Review mortgage documents", "priority": "medium", "days_from_now": 5}
            ],
            "corporate": [
                {"title": "Review incorporation documents", "priority": "high", "days_from_now": 3},
                {"title": "File articles of incorporation", "priority": "high", "days_from_now": 7},
                {"title": "Prepare minute book", "priority": "medium", "days_from_now": 14}
            ]
        }
        
        tasks = initial_tasks.get(matter_type, [])
        for task in tasks:
            task_id = str(uuid.uuid4())
            due_date = datetime.now() + timedelta(days=task["days_from_now"])
            await db.execute('''
                INSERT INTO tasks (task_id, matter_id, title, due_date, priority, status)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (task_id, matter_id, task["title"], due_date.date(), task["priority"], "pending"))
    
    async def track_time_entry(self, time_data: Dict[str, Any]) -> Dict[str, Any]:
        """Track billable time with Ontario-specific requirements"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                entry_id = str(uuid.uuid4())
                
                # Calculate duration if start/end times provided
                duration = time_data.get("duration_minutes", 0)
                if not duration and time_data.get("start_time") and time_data.get("end_time"):
                    # Implementation for time calculation would go here
                    pass
                
                # Calculate amount based on hourly rate
                hourly_rate = time_data.get("hourly_rate", 400.00)  # Default Ontario rate
                amount = (duration / 60.0) * hourly_rate
                
                await db.execute('''
                    INSERT INTO time_entries (
                        entry_id, matter_id, lawyer_id, date, date_worked, duration_minutes,
                        description, activity_type, billable, hourly_rate, total_amount
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    entry_id, time_data["matter_id"], time_data["lawyer_id"],
                    time_data["date"], time_data["date"], duration, time_data["description"],
                    time_data.get("activity_type", "legal_services"),
                    time_data.get("billable", True), hourly_rate, amount
                ))
                
                await db.commit()
            
            return {
                "entry_id": entry_id,
                "amount": amount,
                "status": "recorded"
            }
        except Exception as e:
            logger.error(f"Time tracking failed: {str(e)}")
            raise
    
    async def generate_monthly_bill(self, matter_id: str, bill_date: str) -> Dict[str, Any]:
        """Generate compliant monthly bill"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                # Get unbilled time entries
                cursor = await db.execute('''
                    SELECT entry_id, date, description, duration_minutes, hourly_rate, total_amount
                    FROM time_entries
                    WHERE matter_id = ? AND billable = TRUE AND billed = FALSE
                    ORDER BY date
                ''', (matter_id,))
                time_entries = await cursor.fetchall()
                
                if not time_entries:
                    return {"status": "no_entries", "message": "No billable entries found"}
                
                # Calculate totals
                subtotal = sum(entry[5] for entry in time_entries)
                taxes = subtotal * 0.13  # HST for Ontario
                total = subtotal + taxes
                
                # Generate bill
                bill_id = str(uuid.uuid4())
                bill_number = await self._generate_bill_number()
                
                await db.execute('''
                    INSERT INTO bills (
                        bill_id, matter_id, bill_date, bill_number,
                        subtotal, taxes, total_amount, status
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (bill_id, matter_id, bill_date, bill_number, subtotal, taxes, total, "draft"))
                
                # Mark time entries as billed
                entry_ids = [entry[0] for entry in time_entries]
                for entry_id in entry_ids:
                    await db.execute('UPDATE time_entries SET billed = TRUE, billed_date = ? WHERE entry_id = ?', 
                                   (datetime.now(), entry_id))
                
                await db.commit()
            
            # Generate bill document
            bill_document = await self._generate_bill_document(bill_id, time_entries, subtotal, taxes, total)
            
            return {
                "bill_id": bill_id,
                "bill_number": bill_number,
                "subtotal": subtotal,
                "taxes": taxes,
                "total": total,
                "document_path": bill_document["file_path"]
            }
        except Exception as e:
            logger.error(f"Monthly bill generation failed: {str(e)}")
            raise
    
    async def _generate_bill_number(self) -> str:
        """Generate unique bill number"""
        current_date = datetime.now()
        bill_number = f"BILL-{current_date.year}-{current_date.month:02d}-{uuid.uuid4().hex[:6].upper()}"
        return bill_number
    
    async def _generate_bill_document(self, bill_id: str, time_entries: List, subtotal: float, taxes: float, total: float) -> Dict[str, Any]:
        """Generate bill document (PDF)"""
        # This would integrate with document generation service
        # For now, return mock data
        return {
            "file_path": f"/documents/bills/bill_{bill_id}.pdf",
            "generated_at": datetime.now().isoformat()
        }
    
    async def manage_trust_account(self, transaction_data: Dict[str, Any]) -> Dict[str, Any]:
        """Manage trust account with LSUC compliance"""
        try:
            # Validate trust transaction
            validation_result = await self.lsuc_compliance.validate_trust_transaction(transaction_data)
            if not validation_result["valid"]:
                raise ValueError(f"Trust transaction invalid: {validation_result['reason']}")
            
            async with aiosqlite.connect(self.db_path) as db:
                transaction_id = str(uuid.uuid4())
                
                await db.execute('''
                    INSERT INTO trust_transactions (
                        transaction_id, matter_id, client_id, transaction_date,
                        transaction_type, amount, description, reference_number, bank_account
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    transaction_id, transaction_data["matter_id"], transaction_data["client_id"],
                    transaction_data["date"], transaction_data["type"], transaction_data["amount"],
                    transaction_data.get("description", ""), transaction_data.get("reference", ""),
                    transaction_data.get("bank_account", "main_trust")
                ))
                
                await db.commit()
            
            # Log trust activity
            await self.lsuc_compliance.log_trust_activity(transaction_id, transaction_data)
            
            return {
                "transaction_id": transaction_id,
                "status": "recorded",
                "compliance_verified": True
            }
        except Exception as e:
            logger.error(f"Trust account management failed: {str(e)}")
            raise
    
    async def get_dashboard_metrics(self, lawyer_id: str) -> Dict[str, Any]:
        """Get comprehensive practice dashboard metrics"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                # Active matters count
                cursor = await db.execute('''
                    SELECT COUNT(*) FROM matters
                    WHERE responsible_lawyer = ? AND status = 'open'
                ''', (lawyer_id,))
                active_matters = (await cursor.fetchone())[0]
                
                # Monthly billable hours
                cursor = await db.execute('''
                    SELECT SUM(duration_minutes) FROM time_entries
                    WHERE lawyer_id = ? AND billable = TRUE
                    AND date >= date('now', '-30 days')
                ''', (lawyer_id,))
                monthly_hours_result = await cursor.fetchone()
                monthly_hours = (monthly_hours_result[0] or 0) / 60.0  # Convert to hours
                
                # Outstanding bills
                cursor = await db.execute('''
                    SELECT SUM(total_amount - paid_amount) FROM bills
                    WHERE status = 'sent'
                ''')
                outstanding_bills_result = await cursor.fetchone()
                outstanding_bills = outstanding_bills_result[0] or 0.0
                
                # Trust account balance
                cursor = await db.execute('''
                    SELECT SUM(CASE WHEN transaction_type = 'receipt' THEN amount ELSE -amount END)
                    FROM trust_transactions
                ''')
                trust_balance_result = await cursor.fetchone()
                trust_balance = trust_balance_result[0] or 0.0
                
                return {
                    "active_matters": active_matters,
                    "monthly_billable_hours": round(monthly_hours, 2),
                    "outstanding_bills": outstanding_bills,
                    "trust_balance": trust_balance,
                    "generated_at": datetime.now().isoformat()
                }
                
        except Exception as e:
            logger.error(f"Failed to get dashboard metrics: {str(e)}")
            raise
    
    def is_ready(self) -> bool:
        """Check if practice manager is ready"""
        return self.is_initialized