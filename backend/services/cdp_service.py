"""CDP 관련 비즈니스 로직 서비스"""

from typing import List, Dict, Any, Optional
import json

from ..config.cdp_columns import CDP_COLUMNS, get_all_columns, get_columns_by_category
from ..config.settings import TEAM_SCENARIOS, COMMON_QUESTIONS
from ..models.query_models import QueryRequest, QueryResponse, QueryAnalysisResult
from .ai_service import AIService


class CDPService:
    def __init__(self):
        self.all_columns = get_all_columns()
    
    def get_column_stats(self) -> Dict[str, int]:
        """카테고리별 컬럼 수 반환"""
        return {
            category: len(columns) 
            for category, columns in CDP_COLUMNS.items()
        }
    
    def search_columns(self, query: str, category: Optional[str] = None) -> List[Dict[str, str]]:
        """컬럼 검색"""
        query_lower = query.lower()
        results = []
        
        columns_to_search = (
            get_columns_by_category(category) if category 
            else self.all_columns
        )
        
        for column_name, description in columns_to_search.items():
            if (query_lower in column_name.lower() or 
                query_lower in description.lower()):
                results.append({
                    "column": column_name,
                    "description": description,
                    "category": self._get_column_category(column_name)
                })
        
        return results[:50]  # 최대 50개 결과만 반환
    
    def get_team_scenarios(self, team: str) -> List[str]:
        """팀별 시나리오 반환"""
        return TEAM_SCENARIOS.get(team, [])
    
    def get_common_questions(self) -> List[str]:
        """자주 묻는 질문들 반환"""
        return COMMON_QUESTIONS
    
    def get_relevant_columns(self, query: str) -> List[str]:
        """쿼리와 관련된 컬럼들을 추천"""
        query_lower = query.lower()
        relevant_columns = []
        
        # 키워드 기반 매칭
        keywords_mapping = {
            '골프': ['fa_int_golf', 'fa_ind_golfcourse', 'fa_ind_golfequipmnt', 'sc_int_golf'],
            '반려동물': ['fa_int_householdpet', 'fa_ind_pet', 'fa_ind_pets'],
            '여행': ['fa_int_traveldomestic', 'fa_int_traveloverseas', 'fa_int_travelpackage', 'fa_int_travelasia'],
            '결혼': ['fa_int_wedding', 'fa_ind_weddingsvc', 'sc_int_wedding'],
            '대출': ['fa_int_loan1stfinancial', 'fa_int_loan2ndfinancial', 'fa_int_loanpersonal'],
            '배달': ['fa_int_delivery', 'fa_ind_delivery', 'sc_int_delivery'],
            '피트니스': ['fa_int_gym', 'fa_ind_fitness', 'sc_int_gym'],
            '요가': ['fa_int_pilatesyoga', 'sc_int_pilatesyoga'],
            '필라테스': ['fa_int_pilatesyoga', 'sc_int_pilatesyoga'],
            '뷰티': ['fa_ind_beauty', 'fa_ind_cosmetic'],
            '카페': ['fa_ind_cafe', 'fa_ind_cafetotal', 'fa_ind_studycafe'],
            '음식점': ['fa_ind_restaurant', 'fa_ind_foodbeverage'],
            '온라인쇼핑': ['fa_ind_openmarket', 'fa_ind_complexmall'],
            '20대': ['fi_npay_age20', 'fi_npay_age20_25', 'fi_npay_age25_30'],
            '30대': ['fi_npay_age30', 'fi_npay_age30_35', 'fi_npay_age35_40'],
            '40대': ['fi_npay_age40', 'fi_npay_age40_45', 'fi_npay_age45_50'],
            '50대': ['fi_npay_age50', 'fi_npay_age50_55', 'fi_npay_age55_60'],
            '여성': ['fi_npay_genderf'],
            '남성': ['fi_npay_genderm']
        }
        
        for keyword, columns in keywords_mapping.items():
            if keyword in query_lower:
                relevant_columns.extend(columns)
        
        # 중복 제거 후 실제 존재하는 컬럼만 반환
        unique_columns = list(set(relevant_columns))
        return [col for col in unique_columns if col in self.all_columns]
    
    def process_query(self, request: QueryRequest) -> QueryResponse:
        """쿼리 처리"""
        if not request.api_key:
            return QueryResponse(
                success=False,
                error="API 키가 필요합니다."
            )
        
        try:
            ai_service = AIService(request.api_key)
            result = ai_service.analyze_query(request.user_query)
            
            if result:
                return QueryResponse(success=True, result=result)
            else:
                return QueryResponse(
                    success=False, 
                    error="쿼리 분석에 실패했습니다."
                )
                
        except Exception as e:
            return QueryResponse(
                success=False,
                error=f"처리 중 오류가 발생했습니다: {str(e)}"
            )
    
    def validate_api_key(self, api_key: str) -> tuple[bool, str]:
        """API 키 유효성 검증"""
        if not api_key:
            return False, "API 키를 입력해주세요."
        
        if not api_key.startswith(('sk-', 'sk-proj-')):
            return False, "유효하지 않은 API 키 형식입니다."
        
        try:
            ai_service = AIService(api_key)
            return ai_service.test_api_key()
        except Exception as e:
            return False, f"API 키 검증 중 오류: {str(e)}"
    
    def _get_column_category(self, column_name: str) -> str:
        """컬럼의 카테고리 반환"""
        for category, columns in CDP_COLUMNS.items():
            if column_name in columns:
                return category
        return "unknown"
    
    def format_analysis_results(self, result: QueryAnalysisResult) -> str:
        """분석 결과를 사용자 친화적 형태로 포맷팅"""
        formatted = f"""
## 📊 분석 결과

**질문 분석:** {result.query_analysis}

**타겟 고객:** {result.target_description}

**예상 타겟 규모:** {result.estimated_target_size}

### 🎯 추천 컬럼들

"""
        
        for col in result.recommended_columns:
            priority_emoji = {
                'high': '🔴',
                'medium': '🟡', 
                'low': '🟢'
            }
            
            formatted += f"""
**{priority_emoji.get(col.priority, '⚪')} {col.column}** ({col.priority})
- 설명: {col.description}
- 조건: {col.condition}  
- 선택 이유: {col.reasoning}
"""
        
        formatted += f"""

### 💡 비즈니스 인사이트

"""
        for insight in result.business_insights:
            formatted += f"- {insight}\n"
        
        formatted += f"""

### 🚀 마케팅 추천사항

"""
        for recommendation in result.marketing_recommendations:
            formatted += f"- {recommendation}\n"
        
        formatted += f"""

### 📝 생성된 SQL 쿼리

```sql
{result.sql_query}
```
"""
        
        return formatted