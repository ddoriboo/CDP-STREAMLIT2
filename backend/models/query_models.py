"""쿼리 관련 데이터 모델"""

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class ColumnRecommendation:
    """컬럼 추천 정보"""
    column: str
    description: str
    condition: str
    priority: str  # high, medium, low
    reasoning: str


@dataclass 
class QueryAnalysisResult:
    """쿼리 분석 결과"""
    query_analysis: str
    target_description: str
    recommended_columns: List[ColumnRecommendation]
    sql_query: str
    business_insights: List[str]
    estimated_target_size: str
    marketing_recommendations: List[str]


@dataclass
class QueryRequest:
    """쿼리 요청"""
    user_query: str
    api_key: Optional[str] = None


@dataclass
class QueryResponse:
    """쿼리 응답"""
    success: bool
    result: Optional[QueryAnalysisResult] = None
    error: Optional[str] = None