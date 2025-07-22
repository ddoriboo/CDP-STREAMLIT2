"""애플리케이션 설정"""

import os

# OpenAI 설정
OPENAI_MODEL = "gpt-4o-2024-11-20"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# CDP 데이터베이스 설정
CDP_TABLE_NAME = "fsight__db_cp.mart_latest"

# 시스템 프롬프트
SYSTEM_PROMPT = """당신은 CDP(Customer Data Platform) 전문가입니다. 사용자의 자연어 질문을 분석하여 최적의 고객 세그먼테이션 전략을 제공합니다.

컬럼 선택 가이드라인:
1. 핵심 지표 (high priority): 질문의 핵심 요구사항과 직접적으로 관련된 컬럼 (최대 3-4개)
2. 보조 지표 (medium priority): 타겟 고객을 더 세밀하게 정의하는 데 도움이 되는 컬럼 (최대 2-3개)
3. 참고 지표 (low priority): 추가적인 인사이트를 제공할 수 있는 선택적 컬럼 (최대 1-2개)
4. 전체 컬럼 수는 일반적으로 5-8개가 적절하며, 너무 많은 컬럼은 타겟을 지나치게 좁힐 수 있음
5. 업종별 결제 관련 질문의 경우 fa_ind_* 컬럼 중심으로 선택
6. 관심사/행동 패턴 관련 질문의 경우 fa_int_* 및 sc_int_* 컬럼 중심으로 선택
7. 인구통계학적 세분화가 필요한 경우 fi_npay_age*, fi_npay_gender* 컬럼 활용

중요: 모든 SQL 쿼리의 FROM 절에는 반드시 fsight__db_cp.mart_latest 테이블을 사용하세요.

응답은 반드시 다음 JSON 형식으로만 제공해주세요. 다른 텍스트는 포함하지 마세요:
{
    "query_analysis": "사용자 질문 분석 내용",
    "target_description": "타겟 고객군 설명",
    "recommended_columns": [
        {
            "column": "컬럼명",
            "description": "컬럼 설명",
            "condition": "추천 조건 (예: > 0.7, IS NOT NULL 등)",
            "priority": "high|medium|low",
            "reasoning": "선택 이유"
        }
    ],
    "sql_query": "SELECT 문으로 된 쿼리 (FROM fsight__db_cp.mart_latest 사용)",
    "business_insights": [
        "비즈니스 인사이트 1",
        "비즈니스 인사이트 2"
    ],
    "estimated_target_size": "예상 타겟 규모 (%)",
    "marketing_recommendations": [
        "마케팅 추천사항 1",
        "마케팅 추천사항 2"
    ]
}"""

# 팀 시나리오
TEAM_SCENARIOS = {
    "marketing": [
        "20-30대 온라인 쇼핑 활발 고객을 타겟으로 한 신제품 마케팅 전략을 세우고 싶습니다.",
        "최근 해외직구를 많이 하는 고객들에게 국내 대안 상품을 추천하고 싶습니다.",
        "골프에 관심이 많은 고객들을 대상으로 한 프리미엄 상품 마케팅을 기획하고 있습니다."
    ],
    "finance": [
        "최근 대출을 받은 고객들의 패턴을 분석하여 추가 금융 상품을 제안하고 싶습니다.",
        "예적금 개설 고객들의 특성을 파악하여 맞춤형 투자 상품을 추천하고 싶습니다.",
        "카드 사용 패턴이 활발한 고객들에게 프리미엄 카드를 제안하고 싶습니다."
    ],
    "retail": [
        "배달 음식을 자주 시키는 고객들에게 간편식 상품을 추천하고 싶습니다.",
        "반려동물 관련 상품을 구매하는 고객들의 추가 구매 패턴을 분석하고 싶습니다.",
        "인테리어에 관심이 많은 고객들을 대상으로 한 홈 데코 상품을 마케팅하고 싶습니다."
    ]
}

# 자주 사용되는 질문들
COMMON_QUESTIONS = [
    "20-30대 여성 고객 중에서 온라인 쇼핑을 자주 하는 고객들을 찾고 싶습니다.",
    "최근에 결혼 준비를 하고 있는 고객들을 타겟으로 하고 싶습니다.",
    "골프에 관심이 많고 고소득층인 고객들을 찾아주세요.",
    "반려동물을 키우는 가구의 고객들을 분석하고 싶습니다.",
    "최근에 대출을 받은 고객들의 특성을 파악하고 싶습니다."
]