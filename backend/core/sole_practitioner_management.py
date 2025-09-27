# backend/core/sole_practitioner_management.py
"""
Enhanced Practice Management System for Ontario Sole Practitioner
Comprehensive client, matter, and billing management
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import sqlite3
import aiosqlite
from pathlib import Path
import json

logger = logging.getLogger(__name__)

@dataclass
class Matter:
    id: str
    client_name: str
    matter_type: str
    status: str
    opened_date: datetime
    closed_date: Optional[datetime]
    responsible_lawyer: str
    legal_assistant: str
    estimated_value: float
    billing_method: str
    trust_funds: float
    documents_count: int
    tasks_count: int
    next_deadline: Optional[datetime]
    priority: str

@dataclass
class TimeEntry:
    id: str
    matter_id: str
    lawyer_id: str
    date: datetime
    duration_minutes: int
    description: str
    hourly_rate: float
    billable: bool
    billed: bool
    activity_type: str

@dataclass
class Client:
    id: str
    name: str
    email: str
    phone: str
    address: str
    matter_count: int
    total_billed: float
    outstanding_balance: float
    trust_balance: float
    status: str
    referral_source: str
    conflict_check_completed: bool

class OntarioSolePractitionerManager:
    """Comprehensive practice management system for Ontario sole practitioner"""
    
    def __init__(self):
        self.is_initialized = False
        self.db_path = "/tmp/ontario_practice.db"
        self.lawyer_name = "John Doe, Barrister & Solicitor"
        self.law_society_number = "12345P"
        self.office_address = "123 Main Street, Toronto, ON M5V 1A1"
        
    async def initialize(self):
        """Initialize practice management system"""
        try:
            logger.info("Initializing Ontario Sole Practitioner Management System...")
            
            # Initialize database
            await self._init_database()
            
            # Load practice templates
            await self._load_practice_templates()
            
            # Setup billing rates
            await self._setup_billing_rates()
            
            # Initialize matter tracking
            await self._init_matter_tracking()
            
            self.is_initialized = True
            logger.info("✓ Practice Management System initialized")
            
        except Exception as e:
            logger.error(f"Failed to initialize Practice Management: {str(e)}")
            raise
    
    async def _init_database(self):
        """Initialize SQLite database for practice management"""
        async with aiosqlite.connect(self.db_path) as db:
            # Create tables
            await db.execute("""
                CREATE TABLE IF NOT EXISTS clients (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    email TEXT,
                    phone TEXT,
                    address TEXT,
                    matter_count INTEGER DEFAULT 0,
                    total_billed REAL DEFAULT 0.0,
                    outstanding_balance REAL DEFAULT 0.0,
                    trust_balance REAL DEFAULT 0.0,
                    status TEXT DEFAULT 'active',
                    referral_source TEXT,
                    conflict_check_completed BOOLEAN DEFAULT FALSE,
                    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            await db.execute("""
                CREATE TABLE IF NOT EXISTS matters (
                    id TEXT PRIMARY KEY,
                    client_id TEXT NOT NULL,
                    client_name TEXT NOT NULL,
                    matter_type TEXT NOT NULL,
                    status TEXT DEFAULT 'open',
                    opened_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    closed_date TIMESTAMP,
                    responsible_lawyer TEXT,
                    legal_assistant TEXT,
                    estimated_value REAL DEFAULT 0.0,
                    billing_method TEXT DEFAULT 'hourly',
                    trust_funds REAL DEFAULT 0.0,
                    documents_count INTEGER DEFAULT 0,
                    tasks_count INTEGER DEFAULT 0,
                    next_deadline TIMESTAMP,
                    priority TEXT DEFAULT 'medium',
                    FOREIGN KEY (client_id) REFERENCES clients (id)
                )
            """)
            
            await db.execute("""
                CREATE TABLE IF NOT EXISTS time_entries (
                    id TEXT PRIMARY KEY,
                    matter_id TEXT NOT NULL,
                    lawyer_id TEXT NOT NULL,
                    date TIMESTAMP NOT NULL,
                    duration_minutes INTEGER NOT NULL,
                    description TEXT NOT NULL,
                    hourly_rate REAL NOT NULL,
                    billable BOOLEAN DEFAULT TRUE,
                    billed BOOLEAN DEFAULT FALSE,
                    activity_type TEXT,
                    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (matter_id) REFERENCES matters (id)
                )
            """)
            
            await db.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id TEXT PRIMARY KEY,
                    matter_id TEXT NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT,
                    due_date TIMESTAMP,
                    priority TEXT DEFAULT 'medium',
                    status TEXT DEFAULT 'pending',
                    assigned_to TEXT,
                    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    completed_date TIMESTAMP,
                    FOREIGN KEY (matter_id) REFERENCES matters (id)
                )
            """)
            
            await db.execute("""
                CREATE TABLE IF NOT EXISTS documents (
                    id TEXT PRIMARY KEY,
                    matter_id TEXT NOT NULL,
                    document_type TEXT NOT NULL,
                    title TEXT NOT NULL,
                    file_path TEXT,
                    version INTEGER DEFAULT 1,
                    status TEXT DEFAULT 'draft',
                    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (matter_id) REFERENCES matters (id)
                )
            """)
            
            await db.commit()

    async def _load_practice_templates(self):
        """Load practice management templates"""
        self.templates = {
            "client_intake": {
                "questions": [
                    "What is the legal issue?",
                    "What is your desired outcome?",
                    "Have you consulted other lawyers?",
                    "What is your budget/timeline?"
                ],
                "documents_required": ["ID verification", "Conflict check"]
            },
            "matter_checklist": {
                "will": [
                    "Conflict check completed",
                    "Client ID verified",
                    "Asset list prepared",
                    "Beneficiaries identified",
                    "Executor appointed",
                    "Guardian appointed (if applicable)",
                    "Document drafted",
                    "Review completed",
                    "Execution arranged",
                    "Registration completed"
                ],
                "poa_property": [
                    "Conflict check completed",
                    "Capacity assessment",
                    "Attorney identified",
                    "Powers specified",
                    "Limitations defined",
                    "Document drafted",
                    "Review completed",
                    "Execution arranged",
                    "Registration completed"
                ],
                "poa_personal_care": [
                    "Conflict check completed",
                    "Age verification (16+)",
                    "Capacity assessment",
                    "Attorney identified",
                    "Healthcare wishes discussed",
                    "Document drafted",
                    "Review completed",
                    "Execution arranged"
                ]
            }
        }

    async def _setup_billing_rates(self):
        """Setup billing rates and fee structures"""
        self.billing_rates = {
            "senior_lawyer": 450.00,
            "junior_lawyer": 350.00,
            "legal_assistant": 150.00,
            "clerk": 100.00
        }
        
        self.fixed_fees = {
            "simple_will": 750.00,
            "complex_will": 1500.00,
            "poa_property": 350.00,
            "poa_personal_care": 300.00,
            "both_poa": 600.00,
            "will_poa_package": 1200.00
        }

    async def _init_matter_tracking(self):
        """Initialize matter tracking system"""
        self.matter_types = {
            "wills_estates": "Wills and Estate Planning",
            "poa": "Powers of Attorney", 
            "estate_admin": "Estate Administration",
            "real_estate": "Real Estate",
            "corporate": "Corporate Law",
            "family": "Family Law",
            "litigation": "Civil Litigation"
        }

    async def create_new_client(self, client_data: Dict[str, Any]) -> str:
        """Create new client record"""
        try:
            client_id = f"CLT_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute("""
                    INSERT INTO clients (id, name, email, phone, address, referral_source)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    client_id,
                    client_data.get('name'),
                    client_data.get('email'),
                    client_data.get('phone'),
                    client_data.get('address'),
                    client_data.get('referral_source', 'Unknown')
                ))
                await db.commit()
            
            logger.info(f"Created new client: {client_id}")
            return client_id
            
        except Exception as e:
            logger.error(f"Failed to create client: {str(e)}")
            raise

    async def create_new_matter(self, matter_data: Dict[str, Any]) -> str:
        """Create new matter"""
        try:
            matter_id = f"MTR_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute("""
                    INSERT INTO matters (
                        id, client_id, client_name, matter_type, responsible_lawyer,
                        legal_assistant, estimated_value, billing_method, priority
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    matter_id,
                    matter_data.get('client_id'),
                    matter_data.get('client_name'),
                    matter_data.get('matter_type'),
                    matter_data.get('responsible_lawyer', self.lawyer_name),
                    matter_data.get('legal_assistant', 'Legal Assistant'),
                    matter_data.get('estimated_value', 0.0),
                    matter_data.get('billing_method', 'hourly'),
                    matter_data.get('priority', 'medium')
                ))
                await db.commit()
            
            # Create initial tasks based on matter type
            await self._create_initial_tasks(matter_id, matter_data.get('matter_type'))
            
            logger.info(f"Created new matter: {matter_id}")
            return matter_id
            
        except Exception as e:
            logger.error(f"Failed to create matter: {str(e)}")
            raise

    async def _create_initial_tasks(self, matter_id: str, matter_type: str):
        """Create initial tasks based on matter type"""
        tasks = []
        
        if matter_type == "will":
            tasks = [
                {"title": "Client intake and conflict check", "priority": "high", "days_from_now": 0},
                {"title": "Gather asset information", "priority": "high", "days_from_now": 3},
                {"title": "Draft will document", "priority": "high", "days_from_now": 7},
                {"title": "Review and finalize will", "priority": "medium", "days_from_now": 14},
                {"title": "Arrange execution ceremony", "priority": "medium", "days_from_now": 21}
            ]
        elif matter_type in ["poa_property", "poa_personal_care"]:
            tasks = [
                {"title": "Client intake and conflict check", "priority": "high", "days_from_now": 0},
                {"title": "Assess capacity requirements", "priority": "high", "days_from_now": 2},
                {"title": "Draft POA document", "priority": "high", "days_from_now": 5},
                {"title": "Review powers and limitations", "priority": "medium", "days_from_now": 10},
                {"title": "Arrange execution", "priority": "medium", "days_from_now": 14}
            ]
        elif matter_type == "estate_admin":
            tasks = [
                {"title": "Obtain death certificate", "priority": "high", "days_from_now": 0},
                {"title": "Locate and review will", "priority": "high", "days_from_now": 1},
                {"title": "Apply for probate", "priority": "high", "days_from_now": 14},
                {"title": "Notify beneficiaries", "priority": "medium", "days_from_now": 21},
                {"title": "Prepare estate accounts", "priority": "medium", "days_from_now": 90}
            ]
        
        async with aiosqlite.connect(self.db_path) as db:
            for i, task in enumerate(tasks):
                task_id = f"TSK_{matter_id}_{i+1:03d}"
                due_date = datetime.now() + timedelta(days=task["days_from_now"])
                
                await db.execute("""
                    INSERT INTO tasks (id, matter_id, title, due_date, priority, assigned_to)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    task_id,
                    matter_id,
                    task["title"],
                    due_date,
                    task["priority"],
                    self.lawyer_name
                ))
            
            await db.commit()

    async def add_time_entry(self, time_data: Dict[str, Any]) -> str:
        """Add time entry for billing"""
        try:
            entry_id = f"TIME_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute("""
                    INSERT INTO time_entries (
                        id, matter_id, lawyer_id, date, duration_minutes,
                        description, hourly_rate, billable, activity_type
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    entry_id,
                    time_data.get('matter_id'),
                    time_data.get('lawyer_id', self.lawyer_name),
                    time_data.get('date', datetime.now()),
                    time_data.get('duration_minutes'),
                    time_data.get('description'),
                    time_data.get('hourly_rate'),
                    time_data.get('billable', True),
                    time_data.get('activity_type', 'legal_work')
                ))
                await db.commit()
            
            logger.info(f"Added time entry: {entry_id}")
            return entry_id
            
        except Exception as e:
            logger.error(f"Failed to add time entry: {str(e)}")
            raise

    async def generate_bill(self, matter_id: str, billing_period: Dict[str, Any]) -> Dict[str, Any]:
        """Generate bill for matter"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                # Get matter details
                matter_cursor = await db.execute("""
                    SELECT * FROM matters WHERE id = ?
                """, (matter_id,))
                matter = await matter_cursor.fetchone()
                
                if not matter:
                    raise ValueError(f"Matter {matter_id} not found")
                
                # Get unbilled time entries
                time_cursor = await db.execute("""
                    SELECT * FROM time_entries 
                    WHERE matter_id = ? AND billable = TRUE AND billed = FALSE
                    AND date BETWEEN ? AND ?
                """, (
                    matter_id,
                    billing_period.get('start_date'),
                    billing_period.get('end_date')
                ))
                time_entries = await time_cursor.fetchall()
                
                # Calculate bill
                total_time = sum(entry[5] for entry in time_entries)  # duration_minutes
                total_amount = sum(entry[5] * entry[7] / 60 for entry in time_entries)  # duration * rate
                
                bill_data = {
                    "bill_id": f"BILL_{matter_id}_{datetime.now().strftime('%Y%m%d')}",
                    "matter_id": matter_id,
                    "client_name": matter[2],  # client_name
                    "billing_period": billing_period,
                    "time_entries": time_entries,
                    "total_time_hours": total_time / 60,
                    "total_amount": total_amount,
                    "hst": total_amount * 0.13,  # Ontario HST
                    "total_with_tax": total_amount * 1.13,
                    "generated_date": datetime.now().isoformat()
                }
                
                # Mark time entries as billed
                for entry in time_entries:
                    await db.execute("""
                        UPDATE time_entries SET billed = TRUE WHERE id = ?
                    """, (entry[0],))
                
                await db.commit()
                
                logger.info(f"Generated bill for matter {matter_id}: ${total_amount:.2f}")
                return bill_data
                
        except Exception as e:
            logger.error(f"Failed to generate bill: {str(e)}")
            raise

    async def get_practice_dashboard(self) -> Dict[str, Any]:
        """Get practice management dashboard data"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                # Active matters
                matters_cursor = await db.execute("""
                    SELECT COUNT(*) FROM matters WHERE status = 'open'
                """)
                active_matters = (await matters_cursor.fetchone())[0]
                
                # Total clients
                clients_cursor = await db.execute("""
                    SELECT COUNT(*) FROM clients WHERE status = 'active'  
                """)
                total_clients = (await clients_cursor.fetchone())[0]
                
                # Unbilled time
                unbilled_cursor = await db.execute("""
                    SELECT SUM(duration_minutes * hourly_rate / 60) 
                    FROM time_entries WHERE billable = TRUE AND billed = FALSE
                """)
                unbilled_amount = (await unbilled_cursor.fetchone())[0] or 0
                
                # Overdue tasks
                overdue_cursor = await db.execute("""
                    SELECT COUNT(*) FROM tasks 
                    WHERE status != 'completed' AND due_date < ?
                """, (datetime.now(),))
                overdue_tasks = (await overdue_cursor.fetchone())[0]
                
                # This month's revenue
                month_start = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
                revenue_cursor = await db.execute("""
                    SELECT SUM(duration_minutes * hourly_rate / 60)
                    FROM time_entries 
                    WHERE billable = TRUE AND billed = TRUE AND date >= ?
                """, (month_start,))
                monthly_revenue = (await revenue_cursor.fetchone())[0] or 0
                
                return {
                    "active_matters": active_matters,
                    "total_clients": total_clients,
                    "unbilled_amount": round(unbilled_amount, 2),
                    "overdue_tasks": overdue_tasks,
                    "monthly_revenue": round(monthly_revenue, 2),
                    "lawyer_name": self.lawyer_name,
                    "law_society_number": self.law_society_number,
                    "last_updated": datetime.now().isoformat()
                }
                
        except Exception as e:
            logger.error(f"Failed to get dashboard data: {str(e)}")
            raise

    async def get_client_matters(self, client_id: str) -> List[Dict[str, Any]]:
        """Get all matters for a client"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                cursor = await db.execute("""
                    SELECT * FROM matters WHERE client_id = ? ORDER BY opened_date DESC
                """, (client_id,))
                
                matters = []
                rows = await cursor.fetchall()
                
                for row in rows:
                    matters.append({
                        "id": row[0],
                        "client_name": row[2],
                        "matter_type": row[3],
                        "status": row[4],
                        "opened_date": row[5],
                        "closed_date": row[6],
                        "estimated_value": row[8],
                        "billing_method": row[9],
                        "priority": row[14]
                    })
                
                return matters
                
        except Exception as e:
            logger.error(f"Failed to get client matters: {str(e)}")
            raise

    async def get_matter_tasks(self, matter_id: str) -> List[Dict[str, Any]]:
        """Get all tasks for a matter"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                cursor = await db.execute("""
                    SELECT * FROM tasks WHERE matter_id = ? ORDER BY due_date ASC
                """, (matter_id,))
                
                tasks = []
                rows = await cursor.fetchall()
                
                for row in rows:
                    tasks.append({
                        "id": row[0],
                        "title": row[2],
                        "description": row[3],
                        "due_date": row[4],
                        "priority": row[5],
                        "status": row[6],
                        "assigned_to": row[7],
                        "created_date": row[8],
                        "completed_date": row[9]
                    })
                
                return tasks
                
        except Exception as e:
            logger.error(f"Failed to get matter tasks: {str(e)}")
            raise

    def is_ready(self) -> bool:
        """Check if practice manager is ready"""
        return self.is_initialized

    async def get_billing_summary(self, period: str = "month") -> Dict[str, Any]:
        """Get billing summary for specified period"""
        try:
            # Calculate date range based on period
            now = datetime.now()
            if period == "month":
                start_date = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            elif period == "quarter":
                quarter_start_month = ((now.month - 1) // 3) * 3 + 1
                start_date = now.replace(month=quarter_start_month, day=1, hour=0, minute=0, second=0, microsecond=0)
            elif period == "year":
                start_date = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
            else:
                start_date = now - timedelta(days=30)  # Default to last 30 days
            
            async with aiosqlite.connect(self.db_path) as db:
                # Billed time and revenue
                billed_cursor = await db.execute("""
                    SELECT 
                        SUM(duration_minutes) as total_minutes,
                        SUM(duration_minutes * hourly_rate / 60) as total_revenue,
                        COUNT(*) as entry_count
                    FROM time_entries 
                    WHERE billable = TRUE AND billed = TRUE AND date >= ?
                """, (start_date,))
                billed_data = await billed_cursor.fetchone()
                
                # Unbilled time
                unbilled_cursor = await db.execute("""
                    SELECT 
                        SUM(duration_minutes) as total_minutes,
                        SUM(duration_minutes * hourly_rate / 60) as total_value,
                        COUNT(*) as entry_count
                    FROM time_entries 
                    WHERE billable = TRUE AND billed = FALSE AND date >= ?
                """, (start_date,))
                unbilled_data = await unbilled_cursor.fetchone()
                
                return {
                    "period": period,
                    "start_date": start_date.isoformat(),
                    "end_date": now.isoformat(),
                    "billed": {
                        "hours": round((billed_data[0] or 0) / 60, 2),
                        "revenue": round(billed_data[1] or 0, 2),
                        "entries": billed_data[2] or 0
                    },
                    "unbilled": {
                        "hours": round((unbilled_data[0] or 0) / 60, 2),
                        "value": round(unbilled_data[1] or 0, 2),
                        "entries": unbilled_data[2] or 0
                    },
                    "total_hours": round(((billed_data[0] or 0) + (unbilled_data[0] or 0)) / 60, 2),
                    "total_value": round((billed_data[1] or 0) + (unbilled_data[1] or 0), 2)
                }
                
        except Exception as e:
            logger.error(f"Failed to get billing summary: {str(e)}")
            raise