"""
Enhanced Legal Research Service for Power of Attorney
Specialized research capabilities for POA cases, legislation, and precedents
"""

import requests
import json
import logging
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import re
from urllib.parse import quote, urljoin
import time
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class LegalCase:
    """Represents a legal case result"""
    title: str
    citation: str
    court: str
    date: str
    url: str
    summary: str
    relevance_score: float
    key_points: List[str]
    legal_principles: List[str]
    case_type: str  # 'poa_property', 'poa_care', 'capacity', 'general'

@dataclass
class Legislation:
    """Represents legislation or statute"""
    title: str
    jurisdiction: str
    section: Optional[str]
    url: str
    content: str
    last_updated: str
    relevance_score: float
    related_sections: List[str]

@dataclass
class LegalPrecedent:
    """Represents a legal precedent or principle"""
    principle: str
    source_case: str
    description: str
    application: str
    jurisdiction: str
    strength: str  # 'binding', 'persuasive', 'informative'

@dataclass
class ResearchResult:
    """Comprehensive research results"""
    query: str
    cases: List[LegalCase]
    legislation: List[Legislation]
    precedents: List[LegalPrecedent]
    summary: str
    recommendations: List[str]
    search_metadata: Dict[str, Any]

class EnhancedLegalResearchService:
    """
    Enhanced legal research service with specialized POA research capabilities
    """
    
    def __init__(self):
        self.canlii_base_url = "https://api.canlii.org/v1"
        self.canlii_api_key = None  # To be set via environment variable
        self.ontario_courts = [
            "onca", "onsc", "oncj", "onscdc", "onfst", "onlat", "onlrb"
        ]
        self.poa_keywords = self._load_poa_keywords()
        self.ontario_legislation = self._load_ontario_legislation()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Ontario-Wills-POA-Research-Service/1.0'
        })
    
    def _load_poa_keywords(self) -> Dict[str, List[str]]:
        """Load Power of Attorney specific keywords and phrases"""
        return {
            "property_poa": [
                "power of attorney for property",
                "continuing power of attorney",
                "attorney for property",
                "property management",
                "financial decisions",
                "substitute decisions act",
                "incapacity",
                "mental capacity",
                "property attorney",
                "financial attorney"
            ],
            "personal_care_poa": [
                "power of attorney for personal care",
                "attorney for personal care",
                "personal care decisions",
                "health care consent",
                "substitute decision maker",
                "personal care attorney",
                "health care decisions",
                "consent to treatment",
                "personal care",
                "health care proxy"
            ],
            "capacity_issues": [
                "mental capacity",
                "capacity assessment",
                "incapacity",
                "cognitive impairment",
                "dementia",
                "alzheimer",
                "capacity evaluation",
                "mental competence",
                "decision-making capacity",
                "capacity determination"
            ],
            "legal_principles": [
                "fiduciary duty",
                "best interests",
                "substitute judgment",
                "prior capable wishes",
                "duty of care",
                "conflict of interest",
                "undue influence",
                "abuse of power",
                "breach of trust",
                "negligence"
            ]
        }
    
    def _load_ontario_legislation(self) -> Dict[str, Dict[str, Any]]:
        """Load Ontario legislation relevant to POAs"""
        return {
            "substitute_decisions_act": {
                "title": "Substitute Decisions Act, 1992",
                "citation": "S.O. 1992, c. 30",
                "url": "https://www.ontario.ca/laws/statute/92s30",
                "key_sections": {
                    "7": "Power of attorney for property - general",
                    "8": "Continuing power of attorney for property",
                    "9": "Execution of power of attorney for property",
                    "10": "When power of attorney for property effective",
                    "45": "Power of attorney for personal care",
                    "46": "Execution of power of attorney for personal care",
                    "47": "When power of attorney for personal care effective"
                }
            },
            "health_care_consent_act": {
                "title": "Health Care Consent Act, 1996",
                "citation": "S.O. 1996, c. 2, Sched. A",
                "url": "https://www.ontario.ca/laws/statute/96h02",
                "key_sections": {
                    "20": "Substitute decision-makers for treatment",
                    "21": "Hierarchy of substitute decision-makers",
                    "22": "Principles for giving or refusing consent"
                }
            },
            "succession_law_reform_act": {
                "title": "Succession Law Reform Act",
                "citation": "R.S.O. 1990, c. S.26",
                "url": "https://www.ontario.ca/laws/statute/90s26",
                "key_sections": {
                    "1": "Definitions",
                    "3": "Formal validity of wills",
                    "4": "Testamentary capacity"
                }
            }
        }
    
    def research_poa_topic(self, query: str, poa_type: str = "all", 
                          include_cases: bool = True, 
                          include_legislation: bool = True,
                          max_results: int = 20) -> ResearchResult:
        """
        Comprehensive research on POA-related topics
        
        Args:
            query: Research query
            poa_type: 'property', 'personal_care', or 'all'
            include_cases: Whether to search for cases
            include_legislation: Whether to search for legislation
            max_results: Maximum number of results per category
            
        Returns:
            ResearchResult with comprehensive findings
        """
        try:
            start_time = datetime.now()
            
            # Enhance query with POA-specific terms
            enhanced_query = self._enhance_query_for_poa(query, poa_type)
            
            cases = []
            legislation = []
            precedents = []
            
            # Search for cases
            if include_cases:
                cases = self._search_poa_cases(enhanced_query, poa_type, max_results)
                precedents = self._extract_precedents_from_cases(cases)
            
            # Search for legislation
            if include_legislation:
                legislation = self._search_poa_legislation(enhanced_query, poa_type)
            
            # Generate summary and recommendations
            summary = self._generate_research_summary(query, cases, legislation, precedents)
            recommendations = self._generate_recommendations(query, cases, legislation, poa_type)
            
            # Compile metadata
            search_metadata = {
                "original_query": query,
                "enhanced_query": enhanced_query,
                "poa_type": poa_type,
                "search_duration": (datetime.now() - start_time).total_seconds(),
                "results_count": {
                    "cases": len(cases),
                    "legislation": len(legislation),
                    "precedents": len(precedents)
                },
                "timestamp": datetime.now().isoformat()
            }
            
            return ResearchResult(
                query=query,
                cases=cases,
                legislation=legislation,
                precedents=precedents,
                summary=summary,
                recommendations=recommendations,
                search_metadata=search_metadata
            )
            
        except Exception as e:
            logger.error(f"Error in POA research: {e}")
            raise
    
    def _enhance_query_for_poa(self, query: str, poa_type: str) -> str:
        """Enhance query with POA-specific terms"""
        enhanced_terms = []
        
        # Add base query
        enhanced_terms.append(query)
        
        # Add POA-specific terms based on type
        if poa_type == "property" or poa_type == "all":
            enhanced_terms.extend(self.poa_keywords["property_poa"][:3])
        
        if poa_type == "personal_care" or poa_type == "all":
            enhanced_terms.extend(self.poa_keywords["personal_care_poa"][:3])
        
        # Add Ontario-specific terms
        enhanced_terms.extend(["Ontario", "Substitute Decisions Act"])
        
        return " OR ".join(f'"{term}"' for term in enhanced_terms)
    
    def _search_poa_cases(self, query: str, poa_type: str, max_results: int) -> List[LegalCase]:
        """Search for POA-related cases using CanLII API and web scraping"""
        cases = []
        
        try:
            # Try CanLII API first
            if self.canlii_api_key:
                api_cases = self._search_canlii_api(query, max_results // 2)
                cases.extend(api_cases)
            
            # Supplement with web scraping
            web_cases = self._search_canlii_web(query, poa_type, max_results - len(cases))
            cases.extend(web_cases)
            
            # Sort by relevance and limit results
            cases.sort(key=lambda x: x.relevance_score, reverse=True)
            return cases[:max_results]
            
        except Exception as e:
            logger.error(f"Error searching POA cases: {e}")
            return []
    
    def _search_canlii_api(self, query: str, max_results: int) -> List[LegalCase]:
        """Search using CanLII API (if API key available)"""
        if not self.canlii_api_key:
            return []
        
        try:
            # CanLII API search endpoint
            url = f"{self.canlii_base_url}/caseBrowse/en"
            params = {
                'api_key': self.canlii_api_key,
                'search': query,
                'jurisdiction': 'on',  # Ontario
                'resultCount': max_results
            }
            
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            cases = []
            
            for case_data in data.get('cases', []):
                case = LegalCase(
                    title=case_data.get('title', ''),
                    citation=case_data.get('citation', ''),
                    court=case_data.get('databaseId', ''),
                    date=case_data.get('decisionDate', ''),
                    url=case_data.get('url', ''),
                    summary=case_data.get('summary', ''),
                    relevance_score=self._calculate_poa_relevance(case_data.get('title', '') + ' ' + case_data.get('summary', '')),
                    key_points=[],
                    legal_principles=[],
                    case_type=self._classify_case_type(case_data.get('title', '') + ' ' + case_data.get('summary', ''))
                )
                cases.append(case)
            
            return cases
            
        except Exception as e:
            logger.error(f"Error with CanLII API search: {e}")
            return []
    
    def _search_canlii_web(self, query: str, poa_type: str, max_results: int) -> List[LegalCase]:
        """Search CanLII website directly"""
        cases = []
        
        try:
            # CanLII search URL
            search_url = "https://www.canlii.org/en/on/onca/search/"
            params = {
                'text': query,
                'type': 'decision',
                'ccId': 'onca'  # Start with Ontario Court of Appeal
            }
            
            response = self.session.get(search_url, params=params, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Parse search results
            result_items = soup.find_all('div', class_='result-item')[:max_results]
            
            for item in result_items:
                try:
                    title_elem = item.find('a', class_='result-title')
                    if not title_elem:
                        continue
                    
                    title = title_elem.get_text(strip=True)
                    url = urljoin("https://www.canlii.org", title_elem.get('href', ''))
                    
                    # Extract citation and court info
                    citation_elem = item.find('div', class_='result-citation')
                    citation = citation_elem.get_text(strip=True) if citation_elem else ''
                    
                    # Extract date
                    date_elem = item.find('span', class_='result-date')
                    date = date_elem.get_text(strip=True) if date_elem else ''
                    
                    # Extract summary
                    summary_elem = item.find('div', class_='result-summary')
                    summary = summary_elem.get_text(strip=True) if summary_elem else ''
                    
                    # Calculate relevance
                    full_text = f"{title} {citation} {summary}"
                    relevance_score = self._calculate_poa_relevance(full_text)
                    
                    case = LegalCase(
                        title=title,
                        citation=citation,
                        court=self._extract_court_from_citation(citation),
                        date=date,
                        url=url,
                        summary=summary,
                        relevance_score=relevance_score,
                        key_points=self._extract_key_points(summary),
                        legal_principles=self._extract_legal_principles(full_text),
                        case_type=self._classify_case_type(full_text)
                    )
                    
                    cases.append(case)
                    
                except Exception as e:
                    logger.warning(f"Error parsing case result: {e}")
                    continue
            
            return cases
            
        except Exception as e:
            logger.error(f"Error with CanLII web search: {e}")
            return []
    
    def _search_poa_legislation(self, query: str, poa_type: str) -> List[Legislation]:
        """Search for relevant POA legislation"""
        legislation = []
        
        try:
            # Search Ontario legislation
            for act_key, act_info in self.ontario_legislation.items():
                if self._is_legislation_relevant(query, poa_type, act_info):
                    # Get detailed content for relevant sections
                    relevant_sections = self._find_relevant_sections(query, poa_type, act_info)
                    
                    for section_num, section_title in relevant_sections.items():
                        leg = Legislation(
                            title=f"{act_info['title']} - Section {section_num}",
                            jurisdiction="Ontario",
                            section=section_num,
                            url=f"{act_info['url']}#{section_num}",
                            content=f"{section_title}\n\n[Full section content would be retrieved from Ontario.ca]",
                            last_updated="2024",  # Would be retrieved from source
                            relevance_score=self._calculate_legislation_relevance(query, section_title),
                            related_sections=list(relevant_sections.keys())
                        )
                        legislation.append(leg)
            
            # Sort by relevance
            legislation.sort(key=lambda x: x.relevance_score, reverse=True)
            return legislation[:10]  # Limit to top 10 most relevant
            
        except Exception as e:
            logger.error(f"Error searching POA legislation: {e}")
            return []
    
    def _calculate_poa_relevance(self, text: str) -> float:
        """Calculate relevance score for POA-related content"""
        text_lower = text.lower()
        score = 0.0
        
        # Base POA terms
        poa_terms = ["power of attorney", "poa", "attorney for property", "attorney for personal care"]
        for term in poa_terms:
            if term in text_lower:
                score += 0.3
        
        # Specific POA keywords
        for category, keywords in self.poa_keywords.items():
            for keyword in keywords:
                if keyword.lower() in text_lower:
                    score += 0.1
        
        # Ontario-specific terms
        ontario_terms = ["ontario", "substitute decisions act", "health care consent act"]
        for term in ontario_terms:
            if term in text_lower:
                score += 0.2
        
        # Legal principles
        legal_terms = ["fiduciary", "capacity", "incapacity", "best interests", "substitute judgment"]
        for term in legal_terms:
            if term in text_lower:
                score += 0.15
        
        return min(1.0, score)
    
    def _classify_case_type(self, text: str) -> str:
        """Classify case type based on content"""
        text_lower = text.lower()
        
        if any(term in text_lower for term in self.poa_keywords["property_poa"]):
            return "poa_property"
        elif any(term in text_lower for term in self.poa_keywords["personal_care_poa"]):
            return "poa_care"
        elif any(term in text_lower for term in self.poa_keywords["capacity_issues"]):
            return "capacity"
        else:
            return "general"
    
    def _extract_court_from_citation(self, citation: str) -> str:
        """Extract court name from citation"""
        court_mappings = {
            "ONCA": "Ontario Court of Appeal",
            "ONSC": "Ontario Superior Court of Justice",
            "ONCJ": "Ontario Court of Justice",
            "ONSCDC": "Ontario Superior Court of Justice - Divisional Court"
        }
        
        for abbrev, full_name in court_mappings.items():
            if abbrev in citation.upper():
                return full_name
        
        return "Ontario Court"
    
    def _extract_key_points(self, text: str) -> List[str]:
        """Extract key points from case summary"""
        if not text:
            return []
        
        # Simple extraction based on sentence structure
        sentences = re.split(r'[.!?]+', text)
        key_points = []
        
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 20 and any(keyword in sentence.lower() for keyword in 
                                        ["held", "found", "decided", "ruled", "concluded"]):
                key_points.append(sentence)
        
        return key_points[:3]  # Limit to top 3 key points
    
    def _extract_legal_principles(self, text: str) -> List[str]:
        """Extract legal principles from text"""
        principles = []
        text_lower = text.lower()
        
        principle_indicators = {
            "fiduciary duty": "Fiduciary duty and obligations",
            "best interests": "Best interests standard",
            "substitute judgment": "Substitute judgment principle",
            "undue influence": "Undue influence considerations",
            "capacity": "Mental capacity requirements",
            "prior capable wishes": "Prior capable wishes doctrine"
        }
        
        for indicator, principle in principle_indicators.items():
            if indicator in text_lower:
                principles.append(principle)
        
        return principles
    
    def _extract_precedents_from_cases(self, cases: List[LegalCase]) -> List[LegalPrecedent]:
        """Extract legal precedents from cases"""
        precedents = []
        
        for case in cases:
            for principle in case.legal_principles:
                precedent = LegalPrecedent(
                    principle=principle,
                    source_case=case.title,
                    description=case.summary[:200] + "..." if len(case.summary) > 200 else case.summary,
                    application=f"Applied in {case.case_type} cases",
                    jurisdiction="Ontario",
                    strength="binding" if "ONCA" in case.citation else "persuasive"
                )
                precedents.append(precedent)
        
        return precedents
    
    def _is_legislation_relevant(self, query: str, poa_type: str, act_info: Dict[str, Any]) -> bool:
        """Check if legislation is relevant to the query"""
        query_lower = query.lower()
        title_lower = act_info["title"].lower()
        
        # Direct title match
        if any(word in title_lower for word in query_lower.split()):
            return True
        
        # POA type specific relevance
        if poa_type == "property" and "substitute decisions" in title_lower:
            return True
        elif poa_type == "personal_care" and ("health care consent" in title_lower or "substitute decisions" in title_lower):
            return True
        
        return False
    
    def _find_relevant_sections(self, query: str, poa_type: str, act_info: Dict[str, Any]) -> Dict[str, str]:
        """Find relevant sections within legislation"""
        relevant_sections = {}
        
        if "key_sections" in act_info:
            for section_num, section_title in act_info["key_sections"].items():
                if self._is_section_relevant(query, poa_type, section_title):
                    relevant_sections[section_num] = section_title
        
        return relevant_sections
    
    def _is_section_relevant(self, query: str, poa_type: str, section_title: str) -> bool:
        """Check if a specific section is relevant"""
        query_lower = query.lower()
        title_lower = section_title.lower()
        
        # Direct query match
        if any(word in title_lower for word in query_lower.split() if len(word) > 3):
            return True
        
        # POA type specific
        if poa_type == "property" and "property" in title_lower:
            return True
        elif poa_type == "personal_care" and ("personal care" in title_lower or "treatment" in title_lower):
            return True
        
        return False
    
    def _calculate_legislation_relevance(self, query: str, section_title: str) -> float:
        """Calculate relevance score for legislation section"""
        query_words = set(query.lower().split())
        title_words = set(section_title.lower().split())
        
        # Calculate word overlap
        overlap = len(query_words.intersection(title_words))
        total_words = len(query_words.union(title_words))
        
        if total_words == 0:
            return 0.0
        
        return overlap / total_words
    
    def _generate_research_summary(self, query: str, cases: List[LegalCase], 
                                 legislation: List[Legislation], 
                                 precedents: List[LegalPrecedent]) -> str:
        """Generate a comprehensive research summary"""
        summary_parts = []
        
        summary_parts.append(f"Research Summary for: '{query}'")
        summary_parts.append("=" * 50)
        
        # Cases summary
        if cases:
            summary_parts.append(f"\nFound {len(cases)} relevant cases:")
            for case in cases[:3]:  # Top 3 cases
                summary_parts.append(f"• {case.title} ({case.date}) - {case.court}")
                if case.summary:
                    summary_parts.append(f"  Summary: {case.summary[:150]}...")
        
        # Legislation summary
        if legislation:
            summary_parts.append(f"\nRelevant legislation ({len(legislation)} sections):")
            for leg in legislation[:3]:  # Top 3 sections
                summary_parts.append(f"• {leg.title}")
        
        # Precedents summary
        if precedents:
            summary_parts.append(f"\nKey legal principles ({len(precedents)} identified):")
            unique_principles = list(set(p.principle for p in precedents))
            for principle in unique_principles[:5]:  # Top 5 principles
                summary_parts.append(f"• {principle}")
        
        return "\n".join(summary_parts)
    
    def _generate_recommendations(self, query: str, cases: List[LegalCase], 
                                legislation: List[Legislation], poa_type: str) -> List[str]:
        """Generate practical recommendations based on research"""
        recommendations = []
        
        # General recommendations
        recommendations.append("Ensure compliance with Ontario Substitute Decisions Act requirements")
        
        if poa_type == "property" or poa_type == "all":
            recommendations.append("Specify whether the Power of Attorney for Property is continuing or non-continuing")
            recommendations.append("Include clear powers and any restrictions on the attorney's authority")
            recommendations.append("Ensure proper witness requirements are met (2 witnesses, not the attorney or their spouse)")
        
        if poa_type == "personal_care" or poa_type == "all":
            recommendations.append("Include specific instructions for personal care decisions")
            recommendations.append("Consider including wishes regarding medical treatment and end-of-life care")
            recommendations.append("Ensure the attorney understands their fiduciary duties")
        
        # Case-based recommendations
        if cases:
            high_relevance_cases = [c for c in cases if c.relevance_score > 0.7]
            if high_relevance_cases:
                recommendations.append(f"Review recent case law, particularly {high_relevance_cases[0].title}")
        
        # Legislation-based recommendations
        if legislation:
            recommendations.append("Review current Ontario legislation to ensure compliance with recent amendments")
        
        return recommendations
    
    def search_specific_poa_issue(self, issue: str, poa_type: str) -> Dict[str, Any]:
        """Search for specific POA issues (e.g., capacity challenges, attorney duties)"""
        try:
            # Enhanced query for specific issues
            issue_queries = {
                "capacity": "mental capacity assessment power of attorney challenge",
                "attorney_duties": "attorney duties obligations fiduciary power of attorney",
                "revocation": "revocation power of attorney termination",
                "abuse": "abuse power of attorney undue influence",
                "conflicts": "conflict of interest attorney power of attorney"
            }
            
            query = issue_queries.get(issue, issue)
            
            # Perform targeted research
            result = self.research_poa_topic(query, poa_type, max_results=15)
            
            # Add issue-specific analysis
            result.search_metadata["issue_type"] = issue
            result.search_metadata["specialized_search"] = True
            
            return asdict(result)
            
        except Exception as e:
            logger.error(f"Error in specific POA issue search: {e}")
            return {"error": str(e)}
    
    def get_poa_legislation_updates(self, since_date: str = None) -> List[Dict[str, Any]]:
        """Get recent updates to POA-related legislation"""
        try:
            updates = []
            
            # This would typically query government websites for recent amendments
            # For now, return structured information about key legislation
            
            for act_key, act_info in self.ontario_legislation.items():
                update = {
                    "legislation": act_info["title"],
                    "citation": act_info["citation"],
                    "url": act_info["url"],
                    "last_checked": datetime.now().isoformat(),
                    "status": "current",
                    "key_sections": act_info.get("key_sections", {})
                }
                updates.append(update)
            
            return updates
            
        except Exception as e:
            logger.error(f"Error getting legislation updates: {e}")
            return []

# Initialize global enhanced legal research service
enhanced_legal_research_service = EnhancedLegalResearchService()

def get_enhanced_legal_research_service() -> EnhancedLegalResearchService:
    """Get the global enhanced legal research service instance"""
    return enhanced_legal_research_service

