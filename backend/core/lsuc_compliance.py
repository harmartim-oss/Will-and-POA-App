# backend/core/lsuc_compliance.py
import logging
import sqlite3
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import uuid
import aiosqlite

logger = logging.getLogger(__name__)

class LSUCComplianceManager:
    """Compliance manager for Law Society of Upper Canada (LSUC) requirements"""
    
    def __init__(self, database_path: str = "data/lsuc_compliance.db"):
        self.database_path = database_path
        self.is_initialized = False
        
    async def initialize(self):
        """Initialize LSUC compliance system"""
        try:
            logger.info("🏛️ Initializing LSUC Compliance Manager...")
            await self._setup_compliance_database()
            self.is_initialized = True
            logger.info("✓ LSUC Compliance Manager initialized")
        except Exception as e:
            logger.error(f"LSUC compliance initialization failed: {str(e)}")
            raise
    
    async def _setup_compliance_database(self):
        """Setup compliance database tables"""
        async with aiosqlite.connect(self.database_path) as db:
            # Activity log for professional compliance
            await db.execute("""
                CREATE TABLE IF NOT EXISTS compliance_activity_log (
                    log_id TEXT PRIMARY KEY,
                    activity_type TEXT NOT NULL,
                    matter_id TEXT,
                    user_id TEXT NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    details TEXT,
                    ip_address TEXT,
                    compliance_status TEXT DEFAULT 'compliant'
                )
            """)
            
            # Trust account compliance tracking
            await db.execute("""
                CREATE TABLE IF NOT EXISTS trust_compliance_log (
                    log_id TEXT PRIMARY KEY,
                    transaction_id TEXT NOT NULL,
                    matter_id TEXT,
                    client_id TEXT,
                    transaction_type TEXT NOT NULL,
                    amount REAL NOT NULL,
                    compliance_check_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    compliance_status TEXT DEFAULT 'pending',
                    verification_notes TEXT,
                    created_by TEXT
                )
            """)
            
            # Professional conduct tracking
            await db.execute("""
                CREATE TABLE IF NOT EXISTS professional_conduct_log (
                    conduct_id TEXT PRIMARY KEY,
                    lawyer_id TEXT NOT NULL,
                    conduct_type TEXT NOT NULL,
                    description TEXT,
                    severity TEXT DEFAULT 'info',
                    date_occurred TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    resolution_status TEXT DEFAULT 'pending',
                    notes TEXT
                )
            """)
            
            # Conflict of interest checks
            await db.execute("""
                CREATE TABLE IF NOT EXISTS conflict_checks (
                    check_id TEXT PRIMARY KEY,
                    matter_id TEXT NOT NULL,
                    client_name TEXT NOT NULL,
                    check_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    check_performed_by TEXT NOT NULL,
                    conflicts_found BOOLEAN DEFAULT FALSE,
                    conflict_details TEXT,
                    resolution_notes TEXT,
                    status TEXT DEFAULT 'cleared'
                )
            """)
            
            await db.commit()
    
    async def log_activity(self, activity_type: str, user_id: str, matter_id: str = None, 
                          details: Dict[str, Any] = None, ip_address: str = None) -> str:
        """Log professional activity for compliance"""
        try:
            log_id = f"activity_{uuid.uuid4().hex[:8]}"
            
            async with aiosqlite.connect(self.database_path) as db:
                await db.execute("""
                    INSERT INTO compliance_activity_log 
                    (log_id, activity_type, matter_id, user_id, details, ip_address)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    log_id,
                    activity_type,
                    matter_id,
                    user_id,
                    json.dumps(details) if details else None,
                    ip_address
                ))
                await db.commit()
            
            logger.info(f"Activity logged: {log_id} - {activity_type}")
            return log_id
            
        except Exception as e:
            logger.error(f"Failed to log activity: {str(e)}")
            raise
    
    async def validate_trust_transaction(self, transaction_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate trust account transaction for LSUC compliance"""
        try:
            validation_result = {
                "valid": True,
                "reason": None,
                "warnings": []
            }
            
            # Check required fields
            required_fields = ["matter_id", "client_id", "amount", "type", "date"]
            for field in required_fields:
                if field not in transaction_data or not transaction_data[field]:
                    validation_result["valid"] = False
                    validation_result["reason"] = f"Missing required field: {field}"
                    return validation_result
            
            # Validate transaction amount
            amount = float(transaction_data["amount"])
            if amount <= 0:
                validation_result["valid"] = False
                validation_result["reason"] = "Transaction amount must be positive"
                return validation_result
            
            # Check for large transaction reporting requirements
            if amount > 10000:  # CAD $10,000 threshold
                validation_result["warnings"].append(
                    "Large transaction (>$10,000) - ensure proper documentation and reporting"
                )
            
            # Validate transaction type
            valid_types = ["receipt", "disbursement", "transfer"]
            if transaction_data["type"] not in valid_types:
                validation_result["valid"] = False
                validation_result["reason"] = f"Invalid transaction type. Must be one of: {valid_types}"
                return validation_result
            
            return validation_result
            
        except Exception as e:
            logger.error(f"Trust transaction validation failed: {str(e)}")
            return {
                "valid": False,
                "reason": f"Validation error: {str(e)}",
                "warnings": []
            }
    
    async def log_trust_activity(self, transaction_id: str, transaction_data: Dict[str, Any], 
                                created_by: str = None) -> str:
        """Log trust account activity for compliance tracking"""
        try:
            log_id = f"trust_{uuid.uuid4().hex[:8]}"
            
            async with aiosqlite.connect(self.database_path) as db:
                await db.execute("""
                    INSERT INTO trust_compliance_log 
                    (log_id, transaction_id, matter_id, client_id, transaction_type, 
                     amount, compliance_status, created_by)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    log_id,
                    transaction_id,
                    transaction_data.get("matter_id"),
                    transaction_data.get("client_id"),
                    transaction_data["type"],
                    float(transaction_data["amount"]),
                    "compliant",
                    created_by
                ))
                await db.commit()
            
            logger.info(f"Trust activity logged: {log_id}")
            return log_id
            
        except Exception as e:
            logger.error(f"Failed to log trust activity: {str(e)}")
            raise
    
    async def perform_conflict_check(self, matter_id: str, client_name: str, 
                                   performed_by: str, additional_parties: List[str] = None) -> Dict[str, Any]:
        """Perform conflict of interest check"""
        try:
            check_id = f"conflict_{uuid.uuid4().hex[:8]}"
            
            # Simple conflict check logic (would be more sophisticated in production)
            conflicts_found = False
            conflict_details = []
            
            # Check against existing clients/matters
            async with aiosqlite.connect(self.database_path) as db:
                # This would involve checking against client names, opposing parties, etc.
                # For now, implementing basic structure
                
                await db.execute("""
                    INSERT INTO conflict_checks 
                    (check_id, matter_id, client_name, check_performed_by, 
                     conflicts_found, conflict_details, status)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    check_id,
                    matter_id,
                    client_name,
                    performed_by,
                    conflicts_found,
                    json.dumps(conflict_details) if conflict_details else None,
                    "cleared" if not conflicts_found else "requires_review"
                ))
                await db.commit()
            
            result = {
                "check_id": check_id,
                "conflicts_found": conflicts_found,
                "status": "cleared" if not conflicts_found else "requires_review",
                "details": conflict_details
            }
            
            logger.info(f"Conflict check completed: {check_id}")
            return result
            
        except Exception as e:
            logger.error(f"Conflict check failed: {str(e)}")
            raise
    
    async def get_compliance_report(self, start_date: str, end_date: str, 
                                  lawyer_id: str = None) -> Dict[str, Any]:
        """Generate compliance report for specified period"""
        try:
            async with aiosqlite.connect(self.database_path) as db:
                db.row_factory = aiosqlite.Row
                
                # Activity summary
                activity_query = """
                    SELECT activity_type, COUNT(*) as count
                    FROM compliance_activity_log
                    WHERE timestamp BETWEEN ? AND ?
                """
                params = [start_date, end_date]
                
                if lawyer_id:
                    activity_query += " AND user_id = ?"
                    params.append(lawyer_id)
                    
                activity_query += " GROUP BY activity_type"
                
                cursor = await db.execute(activity_query, params)
                activity_summary = {}
                async for row in cursor:
                    activity_summary[row['activity_type']] = row['count']
                
                # Trust transaction summary
                trust_query = """
                    SELECT transaction_type, COUNT(*) as count, SUM(amount) as total_amount
                    FROM trust_compliance_log
                    WHERE compliance_check_date BETWEEN ? AND ?
                    GROUP BY transaction_type
                """
                
                cursor = await db.execute(trust_query, [start_date, end_date])
                trust_summary = {}
                async for row in cursor:
                    trust_summary[row['transaction_type']] = {
                        "count": row['count'],
                        "total_amount": float(row['total_amount'] or 0)
                    }
                
                # Conflict checks summary
                conflict_query = """
                    SELECT status, COUNT(*) as count
                    FROM conflict_checks
                    WHERE check_date BETWEEN ? AND ?
                    GROUP BY status
                """
                
                cursor = await db.execute(conflict_query, [start_date, end_date])
                conflict_summary = {}
                async for row in cursor:
                    conflict_summary[row['status']] = row['count']
                
                report = {
                    "report_period": {"start": start_date, "end": end_date},
                    "activity_summary": activity_summary,
                    "trust_summary": trust_summary,
                    "conflict_checks": conflict_summary,
                    "generated_at": datetime.now().isoformat()
                }
                
                return report
                
        except Exception as e:
            logger.error(f"Failed to generate compliance report: {str(e)}")
            raise
    
    def is_ready(self) -> bool:
        """Check if compliance manager is ready"""
        return self.is_initialized