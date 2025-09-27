# backend/core/blockchain_authenticator.py
"""
Blockchain Authenticator for Ontario Legal Documents
Provides document verification and tamper-proof record keeping
"""

import hashlib
import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
import asyncio

logger = logging.getLogger(__name__)

class BlockchainAuthenticator:
    """Blockchain-based document authentication and verification system"""
    
    def __init__(self):
        self.blockchain_records = {}
        self.transaction_history = []
        self.is_initialized = False
        
    async def initialize(self):
        """Initialize blockchain authenticator"""
        try:
            logger.info("Initializing Blockchain Authenticator...")
            
            # Initialize blockchain storage
            await self._setup_blockchain_storage()
            
            # Load existing records
            await self._load_existing_records()
            
            self.is_initialized = True
            logger.info("✓ Blockchain Authenticator initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Blockchain Authenticator: {str(e)}")
            raise
    
    async def _setup_blockchain_storage(self):
        """Setup blockchain storage system"""
        # In production, this would connect to actual blockchain network
        # For this implementation, we use local secure storage with cryptographic hashing
        self.blockchain_records = {}
        self.transaction_history = []
        logger.info("✓ Blockchain storage initialized")
    
    async def _load_existing_records(self):
        """Load existing blockchain records"""
        # In production, this would sync with blockchain network
        logger.info("✓ Existing blockchain records loaded")
    
    async def store_document_hash(self, document_id: str, document_content: str) -> str:
        """Store document hash on blockchain"""
        try:
            # Generate document hash
            document_hash = self._generate_document_hash(document_content)
            
            # Create blockchain transaction
            transaction = {
                "transaction_id": f"tx_{document_id}_{datetime.now().timestamp()}",
                "document_id": document_id,
                "document_hash": document_hash,
                "timestamp": datetime.now().isoformat(),
                "block_number": len(self.transaction_history) + 1,
                "previous_hash": self._get_previous_hash(),
                "merkle_root": self._calculate_merkle_root([document_hash])
            }
            
            # Add transaction hash
            transaction["transaction_hash"] = self._generate_transaction_hash(transaction)
            
            # Store in blockchain
            self.blockchain_records[document_id] = transaction
            self.transaction_history.append(transaction)
            
            logger.info(f"Document {document_id} stored on blockchain with hash {document_hash}")
            return transaction["transaction_hash"]
            
        except Exception as e:
            logger.error(f"Failed to store document on blockchain: {str(e)}")
            raise
    
    async def verify_document(self, document_id: str, document_content: str) -> Dict[str, Any]:
        """Verify document integrity using blockchain"""
        try:
            if document_id not in self.blockchain_records:
                return {
                    "verified": False,
                    "error": "Document not found on blockchain"
                }
            
            # Get blockchain record
            blockchain_record = self.blockchain_records[document_id]
            
            # Generate current document hash
            current_hash = self._generate_document_hash(document_content)
            
            # Compare with blockchain hash
            stored_hash = blockchain_record["document_hash"]
            
            verification_result = {
                "verified": current_hash == stored_hash,
                "document_id": document_id,
                "blockchain_hash": stored_hash,
                "current_hash": current_hash,
                "transaction_id": blockchain_record["transaction_id"],
                "timestamp": blockchain_record["timestamp"],
                "block_number": blockchain_record["block_number"]
            }
            
            if verification_result["verified"]:
                logger.info(f"Document {document_id} verification successful")
            else:
                logger.warning(f"Document {document_id} verification failed - content modified")
            
            return verification_result
            
        except Exception as e:
            logger.error(f"Document verification failed: {str(e)}")
            return {
                "verified": False,
                "error": str(e)
            }
    
    async def get_document_history(self, document_id: str) -> List[Dict[str, Any]]:
        """Get complete blockchain history for document"""
        try:
            history = []
            
            for transaction in self.transaction_history:
                if transaction["document_id"] == document_id:
                    history.append({
                        "transaction_id": transaction["transaction_id"],
                        "timestamp": transaction["timestamp"],
                        "block_number": transaction["block_number"],
                        "transaction_hash": transaction["transaction_hash"],
                        "action": "document_created"
                    })
            
            return history
            
        except Exception as e:
            logger.error(f"Failed to get document history: {str(e)}")
            return []
    
    async def get_blockchain_stats(self) -> Dict[str, Any]:
        """Get blockchain statistics"""
        return {
            "total_documents": len(self.blockchain_records),
            "total_transactions": len(self.transaction_history),
            "latest_block": len(self.transaction_history),
            "blockchain_integrity": await self._verify_blockchain_integrity()
        }
    
    def _generate_document_hash(self, content: str) -> str:
        """Generate SHA-256 hash of document content"""
        return hashlib.sha256(content.encode('utf-8')).hexdigest()
    
    def _generate_transaction_hash(self, transaction: Dict[str, Any]) -> str:
        """Generate hash for blockchain transaction"""
        # Create deterministic string from transaction data
        transaction_string = (
            f"{transaction['document_id']}"
            f"{transaction['document_hash']}"
            f"{transaction['timestamp']}"
            f"{transaction['block_number']}"
            f"{transaction.get('previous_hash', '')}"
        )
        return hashlib.sha256(transaction_string.encode('utf-8')).hexdigest()
    
    def _get_previous_hash(self) -> str:
        """Get hash of previous block"""
        if not self.transaction_history:
            return "0" * 64  # Genesis block
        return self.transaction_history[-1]["transaction_hash"]
    
    def _calculate_merkle_root(self, hashes: List[str]) -> str:
        """Calculate Merkle root of document hashes"""
        if not hashes:
            return "0" * 64
        
        if len(hashes) == 1:
            return hashes[0]
        
        # Pair up hashes and combine them
        next_level = []
        for i in range(0, len(hashes), 2):
            if i + 1 < len(hashes):
                combined = hashes[i] + hashes[i + 1]
            else:
                combined = hashes[i] + hashes[i]  # Duplicate if odd number
            
            next_level.append(hashlib.sha256(combined.encode('utf-8')).hexdigest())
        
        return self._calculate_merkle_root(next_level)
    
    async def _verify_blockchain_integrity(self) -> bool:
        """Verify integrity of entire blockchain"""
        try:
            for i, transaction in enumerate(self.transaction_history):
                # Verify transaction hash
                expected_hash = self._generate_transaction_hash(transaction)
                if transaction["transaction_hash"] != expected_hash:
                    logger.error(f"Transaction hash mismatch at block {i}")
                    return False
                
                # Verify previous hash linkage
                if i > 0:
                    expected_previous = self.transaction_history[i-1]["transaction_hash"]
                    if transaction["previous_hash"] != expected_previous:
                        logger.error(f"Previous hash mismatch at block {i}")
                        return False
            
            return True
            
        except Exception as e:
            logger.error(f"Blockchain integrity check failed: {str(e)}")
            return False
    
    async def export_proof_of_authenticity(self, document_id: str) -> Optional[Dict[str, Any]]:
        """Export cryptographic proof of document authenticity"""
        try:
            if document_id not in self.blockchain_records:
                return None
            
            record = self.blockchain_records[document_id]
            
            proof = {
                "document_id": document_id,
                "blockchain_record": {
                    "transaction_id": record["transaction_id"],
                    "document_hash": record["document_hash"],
                    "timestamp": record["timestamp"],
                    "block_number": record["block_number"],
                    "transaction_hash": record["transaction_hash"]
                },
                "verification_instructions": {
                    "how_to_verify": "Hash the document content using SHA-256 and compare with blockchain_record.document_hash",
                    "blockchain_verification": "Verify transaction_hash by hashing the concatenation of document_id, document_hash, timestamp, and block_number"
                },
                "generated_at": datetime.now().isoformat(),
                "blockchain_integrity_verified": await self._verify_blockchain_integrity()
            }
            
            return proof
            
        except Exception as e:
            logger.error(f"Failed to export proof of authenticity: {str(e)}")
            return None
    
    def is_ready(self) -> bool:
        """Check if blockchain authenticator is ready"""
        return self.is_initialized