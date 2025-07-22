"""CDP AI 자연어 쿼리 플랫폼 - Streamlit Frontend"""

import streamlit as st
from typing import Optional

# Backend 서비스 imports
from backend.services.cdp_service import CDPService
from backend.services.ai_service import AIService
from backend.models.query_models import QueryRequest
from backend.utils.helpers import format_priority, get_category_color, copy_to_clipboard_button


# 페이지 설정
st.set_page_config(
    page_title="CDP AI 자연어 쿼리 플랫폼",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 전역 CSS 스타일
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
        color: white;
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .category-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        color: white;
        font-size: 0.8rem;
        margin: 0.1rem;
    }
    
    .column-card {
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        background: #f9f9f9;
    }
    
    .priority-high { border-left: 4px solid #ff4444; }
    .priority-medium { border-left: 4px solid #ffaa00; }
    .priority-low { border-left: 4px solid #00aa00; }
    
    .sql-container {
        background: #f0f2f6;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """세션 상태 초기화"""
    if 'cdp_service' not in st.session_state:
        st.session_state.cdp_service = CDPService()
    
    if 'api_key' not in st.session_state:
        st.session_state.api_key = ""
    
    if 'api_key_validated' not in st.session_state:
        st.session_state.api_key_validated = False
    
    if 'analysis_result' not in st.session_state:
        st.session_state.analysis_result = None


def render_header():
    """헤더 렌더링"""
    st.markdown("""
    <div class="main-header">
        <h1>🎯 CDP AI 자연어 쿼리 플랫폼</h1>
        <p>자연어로 질문하면, AI가 최적의 고객 세그먼테이션 전략을 제공합니다</p>
    </div>
    """, unsafe_allow_html=True)


def render_sidebar():
    """사이드바 렌더링"""
    with st.sidebar:
        st.header("🔧 설정")
        
        # API 키 입력
        api_key = st.text_input(
            "OpenAI API 키",
            value=st.session_state.api_key,
            type="password",
            help="OpenAI API 키를 입력해주세요"
        )
        
        if api_key != st.session_state.api_key:
            st.session_state.api_key = api_key
            st.session_state.api_key_validated = False
        
        # API 키 검증
        if api_key and not st.session_state.api_key_validated:
            if st.button("API 키 검증"):
                with st.spinner("API 키 검증 중..."):
                    is_valid, message = st.session_state.cdp_service.validate_api_key(api_key)
                    
                    if is_valid:
                        st.session_state.api_key_validated = True
                        st.success(message)
                    else:
                        st.error(message)
        
        elif st.session_state.api_key_validated:
            st.success("✅ API 키가 검증되었습니다")
        
        st.divider()
        
        # CDP 컬럼 통계
        st.header("📊 CDP 컬럼 현황")
        column_stats = st.session_state.cdp_service.get_column_stats()
        
        for category, count in column_stats.items():
            color = get_category_color(category)
            st.markdown(f"""
            <div style="background: {color}; color: white; padding: 0.5rem; border-radius: 5px; margin: 0.2rem 0;">
                <strong>{category.title()}</strong>: {count}개
            </div>
            """, unsafe_allow_html=True)
        
        st.divider()
        
        # 팀별 시나리오
        st.header("👥 팀별 예제 시나리오")
        team = st.selectbox("팀 선택", ["marketing", "finance", "retail"])
        
        scenarios = st.session_state.cdp_service.get_team_scenarios(team)
        for i, scenario in enumerate(scenarios):
            if st.button(f"예제 {i+1}", key=f"scenario_{team}_{i}"):
                st.session_state.example_query = scenario


def render_column_explorer():
    """컬럼 탐색기 렌더링"""
    st.header("🔍 CDP 컬럼 탐색기")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        search_query = st.text_input("컬럼 검색", placeholder="검색어를 입력하세요...")
    
    with col2:
        category_filter = st.selectbox(
            "카테고리 필터",
            ["전체"] + list(st.session_state.cdp_service.get_column_stats().keys())
        )
    
    if search_query:
        category = None if category_filter == "전체" else category_filter
        results = st.session_state.cdp_service.search_columns(search_query, category)
        
        if results:
            st.write(f"**검색 결과: {len(results)}개**")
            
            for result in results[:20]:  # 최대 20개만 표시
                color = get_category_color(result['category'])
                
                with st.container():
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.markdown(f"""
                        <div class="column-card">
                            <strong>{result['column']}</strong>
                            <span class="category-badge" style="background-color: {color}">
                                {result['category']}
                            </span>
                            <br><small>{result['description']}</small>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col2:
                        if st.button("쿼리에 추가", key=f"add_{result['column']}"):
                            current_query = st.session_state.get('main_query', '')
                            if current_query:
                                st.session_state.main_query = f"{current_query}, {result['column']} 관련"
                            else:
                                st.session_state.main_query = f"{result['column']} 관련 고객"
        else:
            st.info("검색 결과가 없습니다.")


def render_query_interface():
    """쿼리 인터페이스 렌더링"""
    st.header("💬 자연어 쿼리")
    
    # 자주 묻는 질문들
    st.subheader("🔥 자주 묻는 질문들")
    common_questions = st.session_state.cdp_service.get_common_questions()
    
    cols = st.columns(min(len(common_questions), 3))
    for i, question in enumerate(common_questions[:6]):  # 최대 6개
        with cols[i % 3]:
            if st.button(f"💡 예제 {i+1}", key=f"common_q_{i}"):
                st.session_state.main_query = question
    
    # 메인 쿼리 입력
    query = st.text_area(
        "질문을 자연어로 입력해주세요",
        value=st.session_state.get('main_query', ''),
        height=100,
        placeholder="예: 20-30대 여성 고객 중에서 온라인 쇼핑을 자주 하는 고객들을 찾고 싶습니다.",
        key='main_query'
    )
    
    # 분석 실행
    col1, col2 = st.columns([1, 4])
    
    with col1:
        if st.button("🚀 분석 실행", type="primary", disabled=not st.session_state.api_key_validated):
            if not query.strip():
                st.error("질문을 입력해주세요.")
            else:
                with st.spinner("AI가 분석 중입니다..."):
                    try:
                        request = QueryRequest(
                            user_query=query,
                            api_key=st.session_state.api_key
                        )
                        
                        response = st.session_state.cdp_service.process_query(request)
                        
                        if response.success:
                            st.session_state.analysis_result = response.result
                            st.success("분석이 완료되었습니다!")
                        else:
                            st.error(f"분석 실패: {response.error}")
                    
                    except Exception as e:
                        st.error(f"오류가 발생했습니다: {str(e)}")
    
    with col2:
        if st.button("🔄 초기화"):
            st.session_state.main_query = ""
            st.session_state.analysis_result = None
            st.rerun()


def render_analysis_results():
    """분석 결과 렌더링"""
    if not st.session_state.analysis_result:
        return
    
    result = st.session_state.analysis_result
    
    st.header("📊 분석 결과")
    
    # 요약 정보
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("추천 컬럼 수", len(result.recommended_columns))
    
    with col2:
        st.metric("예상 타겟 규모", result.estimated_target_size)
    
    with col3:
        high_priority_cols = [col for col in result.recommended_columns if col.priority == 'high']
        st.metric("핵심 컬럼 수", len(high_priority_cols))
    
    st.divider()
    
    # 분석 내용
    st.subheader("📝 질문 분석")
    st.write(result.query_analysis)
    
    st.subheader("🎯 타겟 고객 설명")
    st.write(result.target_description)
    
    # 추천 컬럼들
    st.subheader("📋 추천 컬럼들")
    
    # 우선순위별로 그룹화
    priority_groups = {'high': [], 'medium': [], 'low': []}
    for col in result.recommended_columns:
        priority_groups[col.priority].append(col)
    
    for priority, columns in priority_groups.items():
        if columns:
            st.write(f"**{format_priority(priority)} 우선순위**")
            
            for col in columns:
                with st.container():
                    st.markdown(f"""
                    <div class="column-card priority-{priority}">
                        <strong>{col.column}</strong><br>
                        <small><strong>설명:</strong> {col.description}</small><br>
                        <small><strong>조건:</strong> {col.condition}</small><br>
                        <small><strong>선택 이유:</strong> {col.reasoning}</small>
                    </div>
                    """, unsafe_allow_html=True)
    
    # SQL 쿼리
    st.subheader("🔍 생성된 SQL 쿼리")
    st.code(result.sql_query, language='sql')
    
    copy_to_clipboard_button(result.sql_query, "SQL 복사")
    
    # 비즈니스 인사이트
    st.subheader("💡 비즈니스 인사이트")
    for i, insight in enumerate(result.business_insights, 1):
        st.write(f"{i}. {insight}")
    
    # 마케팅 추천사항
    st.subheader("🚀 마케팅 추천사항")
    for i, recommendation in enumerate(result.marketing_recommendations, 1):
        st.write(f"{i}. {recommendation}")
    
    # 결과 다운로드
    st.subheader("📥 결과 다운로드")
    formatted_result = st.session_state.cdp_service.format_analysis_results(result)
    
    st.download_button(
        label="📄 분석 결과 다운로드 (MD)",
        data=formatted_result,
        file_name="cdp_analysis_result.md",
        mime="text/markdown"
    )


def main():
    """메인 함수"""
    initialize_session_state()
    render_header()
    
    # 탭 구성
    tab1, tab2, tab3 = st.tabs(["🎯 쿼리 분석", "🔍 컬럼 탐색기", "📊 결과"])
    
    with tab1:
        render_sidebar()
        render_query_interface()
    
    with tab2:
        render_column_explorer()
    
    with tab3:
        render_analysis_results()


if __name__ == "__main__":
    main()