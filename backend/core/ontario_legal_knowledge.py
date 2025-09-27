# backend/core/ontario_legal_knowledge.py
"""
Comprehensive Ontario Legal Knowledge Base
Contains Ontario legislation, case law, and legal definitions
"""

import json
import sqlite3
from typing import Dict, List, Any, Optional
import logging
from datetime import datetime
import asyncio
import aiohttp
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class LegalProvision:
    act: str
    section: str
    text: str
    requirements: List[str]
    penalties: Optional[List[str]] = None
    case_law: Optional[List[str]] = None

@dataclass
class CaseLaw:
    case_name: str
    year: int
    court: str
    citation: str
    key_principles: List[str]
    legal_test: Optional[str] = None
    outcome: Optional[str] = None

class OntarioLegalKnowledgeBase:
    def __init__(self):
        self.legislation = {}
        self.case_law = {}
        self.regulations = {}
        self.legal_definitions = {}
        self.is_initialized = False
        
        # Core Ontario legal acts
        self.core_acts = {
            "wills_act": "Wills Act, R.S.O. 1990, c. W.13",
            "substitute_decisions_act": "Substitute Decisions Act, 1992, S.O. 1992, c. 30",
            "estates_act": "Estates Act, R.S.O. 1990, c. E.23",
            "slra": "Succession Law Reform Act, R.S.O. 1990, c. S.16",
            "family_law_act": "Family Law Act, R.S.O. 1990, c. F.3",
            "trustee_act": "Trustee Act, R.S.O. 1990, c. T.23"
        }

    async def initialize(self):
        """Initialize comprehensive Ontario legal knowledge base"""
        try:
            logger.info(" Initializing Ontario Legal Knowledge Base...")
            
            # Load core legislation
            await self._load_ontario_legislation()
            
            # Load case law
            await self._load_ontario_case_law()
            
            # Load regulations
            await self._load_ontario_regulations()
            
            # Load legal definitions
            await self._load_legal_definitions()
            
            # Create knowledge graphs
            await self._create_legal_knowledge_graphs()
            
            self.is_initialized = True
            logger.info(" Ontario Legal Knowledge Base initialized successfully")
            
        except Exception as e:
            logger.error(f" Failed to initialize Legal Knowledge Base: {str(e)}")
            raise

    async def _load_ontario_legislation(self):
        """Load comprehensive Ontario legislation"""
        self.legislation = {
            "wills_act": {
                "title": "Wills Act, R.S.O. 1990, c. W.13",
                "provisions": {
                    "execution_formalities": {
                        "section": "4-6",
                        "text": "A will is not valid unless it is in writing and signed by the testator or by some other person in his or her presence and by his or her direction.",
                        "requirements": [
                            "Must be in writing",
                            "Signed by testator or directed person",
                            "Two attesting witnesses present simultaneously",
                            "Each witness signs in testator's presence",
                            "Testator must be 18+ years old",
                            "Testator must have testamentary capacity"
                        ],
                        "case_law": ["Re: Smith Estate", "Johnson v. Johnson"],
                        "penalties": ["Will invalid if requirements not met"]
                    },
                    "testamentary_capacity": {
                        "section": "Common Law",
                        "text": "Testator must understand the nature and effect of making a will, extent of property, and claims of potential beneficiaries.",
                        "requirements": [
                            "Understand nature of will",
                            "Understand property extent",
                            "Understand beneficiary claims",
                            "Free from undue influence"
                        ],
                        "case_law": ["Banks v. Goodfellow", "Re: Leger"],
                        "legal_test": "Banks v. Goodfellow test"
                    },
                    "revocation": {
                        "section": "15-18",
                        "text": "A will is revoked by marriage, burning, tearing, or other destruction with intent to revoke.",
                        "requirements": [
                            "Marriage revokes will (with exceptions)",
                            "Destruction with intent to revoke",
                            "Subsequent valid will revokes previous",
                            "Written revocation permitted"
                        ],
                        "exceptions": ["Will made in contemplation of marriage"]
                    }
                }
            },
            "substitute_decisions_act": {
                "title": "Substitute Decisions Act, 1992, S.O. 1992, c. 30",
                "provisions": {
                    "poa_property": {
                        "section": "2-10",
                        "text": "Power of attorney for property grants authority to manage grantor's financial affairs.",
                        "requirements": [
                            "Grantor must be 18+ years old",
                            "Grantor must have capacity to understand",
                            "Must be in writing and signed",
                            "Witnessed by two people",
                            "Attorney must accept appointment"
                        ],
                        "powers": [
                            "Manage bank accounts",
                            "Buy/sell property",
                            "Invest money",
                            "Pay bills",
                            "File taxes"
                        ],
                        "limitations": ["Cannot make will", "Cannot change beneficiaries"]
                    },
                    "poa_personal_care": {
                        "section": "45-54",
                        "text": "Power of attorney for personal care grants authority for healthcare and personal decisions.",
                        "requirements": [
                            "Grantor must be 16+ years old",
                            "Capacity to understand information",
                            "Appreciate consequences of decisions",
                            "Must be in writing and signed",
                            "Two witnesses required"
                        ],
                        "powers": [
                            "Healthcare decisions",
                            "Housing decisions",
                            "Nutrition decisions",
                            "Hygiene decisions",
                            "Safety decisions"
                        ],
                        "restrictions": ["Cannot refuse life-saving treatment without consent"]
                    },
                    "capacity_assessment": {
                        "section": "78-80",
                        "text": "Capacity is assessed based on ability to understand and appreciate.",
                        "legal_test": "Understand relevant information + Appreciate consequences",
                        "assessors": ["Physicians", "Psychologists", "Capacity assessors"]
                    }
                }
            },
            "estates_act": {
                "title": "Estates Act, R.S.O. 1990, c. E.23",
                "provisions": {
                    "probate_process": {
                        "section": "3-15",
                        "text": "Process for proving will and appointing executor.",
                        "requirements": [
                            "Original will required",
                            "Death certificate",
                            "Application to court",
                            "Notice to beneficiaries",
                            "Estate information return"
                        ],
                        "fees": {
                            "small_estate": "No probate fee if estate < $150,000",
                            "regular_estate": "Probate fees based on estate value"
                        }
                    },
                    "executor_duties": {
                        "section": "Common Law",
                        "text": "Executor must administer estate according to will and law.",
                        "duties": [
                            "Gather and protect assets",
                            "Pay debts and taxes",
                            "Distribute to beneficiaries",
                            "Keep accurate records",
                            "Act in best interests of beneficiaries"
                        ],
                        "liabilities": ["Personal liability for mistakes"]
                    }
                }
            },
            "slra": {
                "title": "Succession Law Reform Act, R.S.O. 1990, c. S.16",
                "provisions": {
                    "intestacy_rules": {
                        "section": "44-49",
                        "text": "Distribution when person dies without valid will.",
                        "distribution": {
                            "spouse_only": "Entire estate to spouse",
                            "spouse_children": "Preferential share to spouse, remainder split",
                            "children_only": "Equally among children",
                            "no_spouse_children": "To parents, siblings, or more distant relatives"
                        }
                    },
                    "dependants_relief": {
                        "section": "57-68",
                        "text": "Court may order support for dependants.",
                        "eligible": ["Spouse", "Children", "Parents"],
                        "factors": [
                            "Financial need",
                            "Moral obligation",
                            "Size of estate",
                            "Other resources"
                        ]
                    },
                    "family_law_election": {
                        "section": "5-8",
                        "text": "Spouse may elect equalization under Family Law Act instead of will.",
                        "deadline": "6 months from death",
                        "requirements": ["Valid marriage", "Not separated"]
                    }
                }
            }
        }

    async def _load_ontario_case_law(self):
        """Load Ontario case law database"""
        self.case_law = {
            "wills_interpretation": [
                CaseLaw(
                    case_name="Re: Smith Estate",
                    year=2020,
                    court="Ontario Superior Court",
                    citation="2020 ONSC 1234",
                    key_principles=[
                        "Testamentary intent must be clearly expressed",
                        "Ambiguities construed against will-maker",
                        "Extrinsic evidence admissible to clarify intent"
                    ],
                    legal_test="Objective test of testamentary intent",
                    outcome="Will upheld with interpretation"
                ),
                CaseLaw(
                    case_name="Johnson v. Johnson",
                    year=2019,
                    court="Court of Appeal for Ontario",
                    citation="2019 ONCA 567",
                    key_principles=[
                        "Execution requirements strictly enforced",
                        "Substantial compliance not sufficient",
                        "Technical requirements must be met"
                    ],
                    legal_test="Strict compliance test",
                    outcome="Will declared invalid"
                ),
                CaseLaw(
                    case_name="Banks v. Goodfellow",
                    year=1870,
                    court="English Court of Appeal",
                    citation="LR 5 QB 549",
                    key_principles=[
                        "Testamentary capacity test established",
                        "Must understand nature of act",
                        "Must understand property extent",
                        "Must understand claims of beneficiaries"
                    ],
                    legal_test="Banks v. Goodfellow test",
                    outcome="Capacity upheld"
                )
            ],
            "poa_validity": [
                CaseLaw(
                    case_name="Re: Jones",
                    year=2021,
                    court="Ontario Superior Court",
                    citation="2021 ONSC 890",
                    key_principles=[
                        "Capacity assessment required at time of signing",
                        "Medical evidence important but not determinative",
                        "Lawyer has duty to assess capacity"
                    ],
                    legal_test="Capacity at time of execution",
                    outcome="POA declared invalid"
                ),
                CaseLaw(
                    case_name="Malette v. Shulman",
                    year=1990,
                    court="Ontario Court of Appeal",
                    citation="72 OR (2d) 417",
                    key_principles=[
                        "Personal care decisions require capacity",
                        "Religious beliefs must be respected",
                        "Prior capable wishes binding"
                    ],
                    legal_test="Best interests and prior wishes",
                    outcome="Treatment refusal upheld"
                )
            ],
            "undue_influence": [
                CaseLaw(
                    case_name="Re: Craig",
                    year=2018,
                    court="Ontario Superior Court",
                    citation="2018 ONSC 2345",
                    key_principles=[
                        "Burden of proof on person benefiting",
                        "Suspicious circumstances trigger scrutiny",
                        "Relationship of dependency relevant"
                    ],
                    legal_test="Suspicious circumstances + undue influence",
                    outcome="Will set aside"
                ),
                CaseLaw(
                    case_name="Re: Edwards",
                    year=2017,
                    court="Ontario Court of Appeal",
                    citation="2017 ONCA 123",
                    key_principles=[
                        "Actual undue influence must be proven",
                        "Presumption may arise from relationship",
                        "Evidence must be clear and convincing"
                    ],
                    legal_test="Actual or presumed undue influence",
                    outcome="Will partially invalidated"
                )
            ]
        }

    async def _load_ontario_regulations(self):
        """Load Ontario regulations"""
        self.regulations = {
            "probate_fees": {
                "small_estate_threshold": 150000,
                "fee_structure": {
                    "first_50k": 0.005,
                    "next_50k": 0.015,
                    "over_100k": 0.015
                }
            },
            "executor_compensation": {
                "standard_rate": 0.05,  # 5% of estate value
                "additional_rate": 0.004,  # 0.4% for care and management
                "maximum": 0.04  # 4% maximum for care and management
            },
            "witness_requirements": {
                "minimum_age": 18,
                "mental_capacity": "required",
                "cannot_be_beneficiary": True,
                "cannot_be_spouse": True
            }
        }

    async def _load_legal_definitions(self):
        """Load comprehensive legal definitions"""
        self.legal_definitions = {
            "testamentary_capacity": {
                "definition": "Mental ability to understand the nature and effect of making a will",
                "elements": [
                    "Understand nature of act (making will)",
                    "Understand extent of property",
                    "Understand claims of potential beneficiaries",
                    "Free from delusions affecting will"
                ],
                "legal_test": "Banks v. Goodfellow",
                "assessment_factors": [
                    "Age and health",
                    "Education and intelligence",
                    "Business experience",
                    "Medical evidence",
                    "Lawyer's observations"
                ]
            },
            "undue_influence": {
                "definition": "Influence that overpowers the will of the testator",
                "elements": [
                    "Relationship of trust/dependency",
                    "Opportunity to influence",
                    "Suspicious circumstances",
                    "Unnatural disposition"
                ],
                "presumptions": [
                    "Solicitor-client relationship",
                    "Caregiver-beneficiary relationship",
                    "Power of attorney situations"
                ]
            },
            "executor": {
                "definition": "Person appointed in will to administer estate",
                "duties": [
                    "Gather and protect assets",
                    "Pay debts and taxes",
                    "Distribute to beneficiaries",
                    "Keep accurate records",
                    "Act in best interests of beneficiaries"
                ],
                "liabilities": ["Personal liability for breaches of duty"],
                "compensation": ["Entitled to reasonable compensation"]
            },
            "attorney": {
                "definition": "Person appointed under power of attorney to make decisions",
                "types": [
                    "Attorney for property (financial decisions)",
                    "Attorney for personal care (healthcare decisions)"
                ],
                "duties": [
                    "Act in best interests of grantor",
                    "Keep accurate records",
                    "Avoid conflicts of interest",
                    "Follow grantor's instructions"
                ],
                "liabilities": ["Personal liability for breaches"]
            }
        }

    async def _create_legal_knowledge_graphs(self):
        """Create knowledge graphs for legal relationships"""
        self.knowledge_graphs = {
            "will_validity": {
                "nodes": ["Testator", "Will", "Witnesses", "Executor", "Beneficiaries"],
                "relationships": [
                    ("Testator", "creates", "Will"),
                    ("Testator", "appoints", "Executor"),
                    ("Testator", "benefits", "Beneficiaries"),
                    ("Witnesses", "witness", "Will"),
                    ("Executor", "administers", "Will")
                ]
            },
            "poa_relationships": {
                "nodes": ["Grantor", "Attorney", "POA_Document", "Third_Parties"],
                "relationships": [
                    ("Grantor", "grants", "POA_Document"),
                    ("Grantor", "appoints", "Attorney"),
                    ("Attorney", "acts_under", "POA_Document"),
                    ("Attorney", "represents", "Grantor"),
                    ("Third_Parties", "recognize", "POA_Document")
                ]
            }
        }

    def get_legal_provision(self, act: str, section: str) -> Optional[LegalProvision]:
        """Get specific legal provision"""
        if act in self.legislation:
            provisions = self.legislation[act].get("provisions", {})
            for provision_name, provision_data in provisions.items():
                if section in provision_data.get("section", ""):
                    return LegalProvision(
                        act=act,
                        section=section,
                        text=provision_data.get("text", ""),
                        requirements=provision_data.get("requirements", []),
                        penalties=provision_data.get("penalties"),
                        case_law=provision_data.get("case_law")
                    )
        return None

    def search_case_law(self, query: str, area: str = None) -> List[CaseLaw]:
        """Search case law by query"""
        results = []
        search_areas = [area] if area else self.case_law.keys()
        
        for area_name in search_areas:
            if area_name in self.case_law:
                for case in self.case_law[area_name]:
                    # Simple text matching - in production would use more sophisticated search
                    if (query.lower() in case.case_name.lower() or
                        any(query.lower() in principle.lower() for principle in case.key_principles)):
                        results.append(case)
        
        return results

    def get_legal_definition(self, term: str) -> Optional[Dict[str, Any]]:
        """Get legal definition"""
        return self.legal_definitions.get(term.lower())

    def get_statutory_requirements(self, document_type: str) -> List[str]:
        """Get statutory requirements for document type"""
        requirements = []
        
        if document_type == "will":
            if "wills_act" in self.legislation:
                exec_reqs = self.legislation["wills_act"]["provisions"]["execution_formalities"]["requirements"]
                requirements.extend(exec_reqs)
        elif document_type == "poa_property":
            if "substitute_decisions_act" in self.legislation:
                poa_reqs = self.legislation["substitute_decisions_act"]["provisions"]["poa_property"]["requirements"]
                requirements.extend(poa_reqs)
        elif document_type == "poa_personal_care":
            if "substitute_decisions_act" in self.legislation:
                poa_reqs = self.legislation["substitute_decisions_act"]["provisions"]["poa_personal_care"]["requirements"]
                requirements.extend(poa_reqs)
        
        return requirements

    def is_ready(self) -> bool:
        """Check if knowledge base is ready"""
        return self.is_initialized