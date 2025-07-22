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
    initial_sidebar_state="collapsed"
)

# 전역 CSS 스타일 - 원래 HTML 디자인 재현
st.markdown("""
<style>
    /* 메인 앱 배경 */
    .stApp {
        background: white;
    }
    
    /* 메인 컨테이너 스타일 */
    .main .block-container {
        max-width: 1200px;
        padding: 40px 20px;
        margin: 0 auto;
        background: #f8f9fa;
        min-height: 100vh;
    }
    
    /* 전체 컨테이너를 흰색 카드로 */
    .stApp > header {
        background-color: transparent !important;
    }
    
    /* 헤더 스타일 */
    .main-header {
        background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
        color: white;
        padding: 40px 30px;
        text-align: center;
        border-radius: 20px 20px 0 0;
        margin: -30px -30px 0 -30px;
    }
    
    .main-header h1 {
        font-size: 2.5em;
        margin-bottom: 10px;
        font-weight: bold;
    }
    
    .main-header p {
        font-size: 1.2em;
        opacity: 0.9;
    }
    
    /* 컨텐츠 영역 */
    .content-wrapper {
        background: white;
        border-radius: 0 0 20px 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        padding: 30px;
        margin: 0 -30px 20px -30px;
        border: 1px solid #e9ecef;
        border-top: none;
    }
    
    /* API 키 섹션 */
    .api-key-section {
        background: #fff3cd;
        border-left: 4px solid #ffc107;
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 20px;
    }
    
    .api-key-section h4 {
        color: #856404;
        margin-bottom: 10px;
    }
    
    /* 탭 스타일 */
    .stTabs [data-baseweb="tab-list"] {
        background: #f8f9fa;
        padding: 0;
        gap: 0;
        border-bottom: 1px solid #e9ecef;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 60px;
        background: transparent;
        border: none;
        padding: 0 30px;
        font-size: 16px;
        font-weight: 500;
        border-bottom: 3px solid transparent;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: #e9ecef;
    }
    
    .stTabs [aria-selected="true"] {
        background: white !important;
        border-bottom-color: #4CAF50 !important;
        color: #4CAF50 !important;
    }
    
    /* 쿼리 입력 스타일 */
    .query-container {
        max-width: 800px;
        margin: 30px auto;
        padding: 0 20px;
    }
    
    /* 컬럼 간격 조정 */
    .stColumns {
        gap: 1rem;
    }
    
    .stColumn {
        padding: 0 0.5rem;
    }
    
    .stTextArea textarea {
        border-radius: 25px !important;
        border: 2px solid #e9ecef !important;
        padding: 20px !important;
        font-size: 18px !important;
    }
    
    .stTextArea textarea:focus {
        border-color: #4CAF50 !important;
        box-shadow: none !important;
    }
    
    /* 버튼 스타일 */
    .stButton > button {
        background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 8px;
        font-size: 14px;
        font-weight: 500;
        transition: all 0.2s ease;
        width: 100%;
        margin: 4px 0;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #45a049 0%, #3d8b40 100%);
        transform: translateY(-1px);
        box-shadow: 0 2px 8px rgba(76, 175, 80, 0.2);
    }
    
    /* 예제 태그 스타일 */
    .example-tag {
        display: inline-block;
        background: white;
        color: #495057;
        padding: 8px 15px;
        margin: 5px;
        border-radius: 20px;
        border: 1px solid #dee2e6;
        cursor: pointer;
        transition: all 0.3s ease;
        font-size: 14px;
    }
    
    .example-tag:hover {
        background: #4CAF50;
        color: white;
        transform: translateY(-2px);
    }
    
    /* 컬럼 카드 스타일 */
    .column-card {
        background: white;
        border: 1px solid #e9ecef;
        border-radius: 15px;
        padding: 20px;
        transition: all 0.3s ease;
        margin-bottom: 15px;
        cursor: pointer;
    }
    
    .column-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        border-color: #4CAF50;
    }
    
    .column-name {
        font-weight: 600;
        color: #2c3e50;
        font-size: 16px;
        margin-bottom: 5px;
    }
    
    .column-category {
        background: #e9ecef;
        color: #6c757d;
        font-size: 12px;
        padding: 4px 8px;
        border-radius: 10px;
        display: inline-block;
    }
    
    .column-description {
        color: #6c757d;
        font-size: 14px;
        margin-top: 10px;
        line-height: 1.4;
    }
    
    /* 팀 카드 스타일 */
    .team-card {
        background: white;
        border: 2px solid #e9ecef;
        border-radius: 15px;
        padding: 20px;
        cursor: pointer;
        transition: all 0.3s ease;
        text-align: left;
    }
    
    .team-card:hover {
        border-color: #4CAF50;
        background: #f8f9fa;
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    }
    
    /* 질문 카드 스타일 */
    .question-card {
        background: white;
        border: 1px solid #e9ecef;
        border-radius: 12px;
        padding: 20px;
        cursor: pointer;
        transition: all 0.3s ease;
        border-left: 4px solid #4CAF50;
        margin-bottom: 15px;
    }
    
    .question-card:hover {
        background: #f8f9fa;
        border-color: #4CAF50;
        transform: translateX(5px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    
    /* 결과 섹션 스타일 */
    .result-section {
        background: #f8f9fa;
        border-radius: 15px;
        padding: 25px;
        margin-top: 20px;
    }
    
    /* SQL 코드 블록 */
    .stCodeBlock {
        border-radius: 10px !important;
    }
    
    /* 메트릭 카드 */
    [data-testid="metric-container"] {
        background-color: white;
        border: 1px solid #e9ecef;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    /* 숨기기: Streamlit 기본 요소들 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* 사이드바 스타일 */
    section[data-testid="stSidebar"] {
        background-color: #f8f9fa;
        border-right: 1px solid #e9ecef;
    }
    
    /* 검색 박스 스타일 */
    .stTextInput input {
        border-radius: 10px !important;
        border: 2px solid #e9ecef !important;
        padding: 15px 20px !important;
        font-size: 16px !important;
    }
    
    .stTextInput input:focus {
        border-color: #4CAF50 !important;
        box-shadow: none !important;
    }
    
    /* 셀렉트박스 스타일 */
    .stSelectbox > div > div {
        border-radius: 10px !important;
        border: 2px solid #e9ecef !important;
    }
    
    /* 경고 메시지 */
    .stAlert {
        border-radius: 10px;
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
    
    if 'show_api_key' not in st.session_state:
        st.session_state.show_api_key = True
    
    if 'selected_team' not in st.session_state:
        st.session_state.selected_team = None


def render_header():
    """헤더 렌더링"""
    st.markdown("""
    <div class="main-header">
        <h1>🎯 CDP AI 자연어 쿼리 플랫폼</h1>
        <p>자연어로 질문하면, AI가 최적의 고객 세그먼테이션 전략을 제공합니다</p>
    </div>
    """, unsafe_allow_html=True)


def render_api_key_section():
    """API 키 섹션 렌더링"""
    with st.container():
        col1, col2 = st.columns([20, 1])
        
        with col1:
            st.markdown("""
            <div class="api-key-section">
                <h4>🔑 OpenAI API 키 설정</h4>
            </div>
            """, unsafe_allow_html=True)
        
        # API 키 입력 영역
        if st.session_state.show_api_key:
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                api_key = st.text_input(
                    "API 키",
                    value=st.session_state.api_key,
                    type="password",
                    placeholder="sk-...",
                    label_visibility="collapsed"
                )
                
                if api_key != st.session_state.api_key:
                    st.session_state.api_key = api_key
                    st.session_state.api_key_validated = False
            
            with col2:
                if st.button("저장", use_container_width=True):
                    if api_key:
                        with st.spinner("API 키 검증 중..."):
                            is_valid, message = st.session_state.cdp_service.validate_api_key(api_key)
                            
                            if is_valid:
                                st.session_state.api_key_validated = True
                                st.success(message)
                            else:
                                st.error(message)
                    else:
                        st.error("API 키를 입력해주세요.")
            
            with col3:
                if st.button("접기", use_container_width=True):
                    st.session_state.show_api_key = False
                    st.rerun()
            
            # API 키 상태 표시
            if st.session_state.api_key_validated:
                st.success("✅ API 키가 검증되었습니다. 서비스를 이용할 수 있습니다.")
            elif st.session_state.api_key:
                st.warning("⚠️ API 키 검증이 필요합니다. '저장' 버튼을 클릭해주세요.")
            else:
                st.info("ℹ️ OpenAI API 키를 입력해주세요. [API 키 발급하기](https://platform.openai.com/api-keys)")
        else:
            if st.button("🔽 API 키 설정 펼치기"):
                st.session_state.show_api_key = True
                st.rerun()
            
            if st.session_state.api_key_validated:
                st.success("✅ API 키가 설정되어 있습니다.")


def render_query_tab():
    """쿼리 분석 탭"""
    st.markdown('<div class="query-container">', unsafe_allow_html=True)
    
    # 자주 묻는 질문들
    st.markdown("### 💡 예제 질문들")
    
    common_questions = st.session_state.cdp_service.get_common_questions()
    
    # 3개씩 한 줄로 표시
    for i in range(0, len(common_questions), 3):
        cols = st.columns(3)
        for j, col in enumerate(cols):
            if i + j < len(common_questions):
                with col:
                    if st.button(
                        common_questions[i + j],
                        key=f"example_{i+j}",
                        use_container_width=True
                    ):
                        st.session_state.main_query = common_questions[i + j]
    
    st.markdown("### 🔍 자연어 쿼리")
    
    # 쿼리 입력
    query = st.text_area(
        "질문을 자연어로 입력해주세요",
        value=st.session_state.get('main_query', ''),
        height=100,
        placeholder="예: 20-30대 여성 고객 중에서 온라인 쇼핑을 자주 하는 고객들을 찾고 싶습니다.",
        label_visibility="collapsed",
        key='main_query'
    )
    
    # 분석 버튼
    col1, col2, col3 = st.columns([1, 1, 3])
    
    with col1:
        if st.button(
            "🚀 분석하기",
            type="primary",
            disabled=not st.session_state.api_key_validated,
            use_container_width=True
        ):
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
                            st.balloons()
                        else:
                            st.error(f"분석 실패: {response.error}")
                    
                    except Exception as e:
                        st.error(f"오류가 발생했습니다: {str(e)}")
    
    with col2:
        if st.button("🔄 초기화", use_container_width=True):
            st.session_state.main_query = ""
            st.session_state.analysis_result = None
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 분석 결과 표시
    if st.session_state.analysis_result:
        render_analysis_results_inline()


def render_column_browser_tab():
    """컬럼 브라우저 탭"""
    st.markdown("### 🔍 CDP 컬럼 탐색")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        search_query = st.text_input(
            "컬럼 검색",
            placeholder="검색어를 입력하세요 (예: 골프, 여행, 대출)",
            label_visibility="collapsed"
        )
    
    with col2:
        category_filter = st.selectbox(
            "카테고리",
            ["전체"] + list(st.session_state.cdp_service.get_column_stats().keys()),
            label_visibility="collapsed"
        )
    
    # 카테고리별 통계
    st.markdown("### 📊 카테고리별 컬럼 수")
    column_stats = st.session_state.cdp_service.get_column_stats()
    
    cols = st.columns(len(column_stats))
    for i, (category, count) in enumerate(column_stats.items()):
        with cols[i]:
            color = get_category_color(category)
            st.markdown(f"""
            <div style="text-align: center; padding: 15px; background: {color}; color: white; border-radius: 10px;">
                <h3 style="margin: 0;">{count}</h3>
                <p style="margin: 0; font-size: 14px;">{category.title()}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # 검색 결과
    if search_query:
        st.markdown("### 🔎 검색 결과")
        
        category = None if category_filter == "전체" else category_filter
        results = st.session_state.cdp_service.search_columns(search_query, category)
        
        if results:
            # 3열 그리드로 표시
            for i in range(0, len(results), 3):
                cols = st.columns(3)
                for j, col in enumerate(cols):
                    if i + j < len(results):
                        result = results[i + j]
                        with col:
                            st.markdown(f"""
                            <div class="column-card">
                                <div class="column-name">{result['column']}</div>
                                <span class="column-category">{result['category']}</span>
                                <div class="column-description">{result['description']}</div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            if st.button("쿼리에 추가", key=f"add_{result['column']}"):
                                current_query = st.session_state.get('main_query', '')
                                if current_query:
                                    st.session_state.main_query = f"{current_query}, {result['column']} 관련"
                                else:
                                    st.session_state.main_query = f"{result['column']} 관련 고객을 찾아주세요"
                                st.info(f"'{result['column']}'이(가) 쿼리에 추가되었습니다.")
        else:
            st.info("검색 결과가 없습니다.")


def render_team_scenarios_tab():
    """팀별 추천 탭"""
    st.markdown("### 👥 팀별 시나리오")
    
    # 팀 선택 버튼들
    teams = [
        {"id": "marketing", "name": "마케팅팀", "desc": "고객 세그먼트 기반 타겟 마케팅"},
        {"id": "finance", "name": "금융팀", "desc": "금융 상품 추천 및 리스크 분석"},
        {"id": "retail", "name": "리테일팀", "desc": "구매 패턴 분석 및 상품 추천"}
    ]
    
    cols = st.columns(3)
    for i, team in enumerate(teams):
        with cols[i]:
            st.markdown(f"""
            <div class="team-card">
                <h4>{team['name']}</h4>
                <p style="color: #6c757d; font-size: 14px;">{team['desc']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"선택", key=f"team_{team['id']}", use_container_width=True):
                st.session_state.selected_team = team['id']
    
    # 선택된 팀의 시나리오 표시
    if st.session_state.selected_team:
        st.markdown(f"### 💡 {st.session_state.selected_team.title()}팀 추천 시나리오")
        
        scenarios = st.session_state.cdp_service.get_team_scenarios(st.session_state.selected_team)
        
        for i, scenario in enumerate(scenarios):
            st.markdown(f"""
            <div class="question-card">
                <div style="font-weight: 600; margin-bottom: 5px;">시나리오 {i+1}</div>
                <div>{scenario}</div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"이 시나리오 사용하기", key=f"use_scenario_{i}"):
                st.session_state.main_query = scenario
                st.success("시나리오가 쿼리 분석 탭에 입력되었습니다. '쿼리 분석' 탭으로 이동해주세요.")


def render_analysis_results_inline():
    """분석 결과를 같은 탭에서 표시"""
    result = st.session_state.analysis_result
    
    st.markdown("---")
    st.markdown("## 📊 분석 결과")
    
    # 요약 메트릭
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("추천 컬럼 수", len(result.recommended_columns))
    
    with col2:
        st.metric("예상 타겟 규모", result.estimated_target_size)
    
    with col3:
        high_priority_cols = [col for col in result.recommended_columns if col.priority == 'high']
        st.metric("핵심 컬럼 수", len(high_priority_cols))
    
    # 분석 내용
    with st.container():
        st.markdown('<div class="result-section">', unsafe_allow_html=True)
        
        st.markdown("### 📝 질문 분석")
        st.write(result.query_analysis)
        
        st.markdown("### 🎯 타겟 고객")
        st.write(result.target_description)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 추천 컬럼들
    st.markdown("### 📋 추천 컬럼들")
    
    # 우선순위별로 그룹화
    priority_groups = {'high': [], 'medium': [], 'low': []}
    for col in result.recommended_columns:
        priority_groups[col.priority].append(col)
    
    for priority, columns in priority_groups.items():
        if columns:
            priority_label = {'high': '🔴 핵심', 'medium': '🟡 보조', 'low': '🟢 참고'}
            st.markdown(f"#### {priority_label[priority]} 우선순위")
            
            for col in columns:
                with st.expander(f"**{col.column}**"):
                    st.write(f"**설명:** {col.description}")
                    st.write(f"**조건:** `{col.condition}`")
                    st.write(f"**선택 이유:** {col.reasoning}")
    
    # SQL 쿼리
    st.markdown("### 🔍 생성된 SQL 쿼리")
    st.code(result.sql_query, language='sql')
    
    # 인사이트와 추천사항
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 💡 비즈니스 인사이트")
        for i, insight in enumerate(result.business_insights, 1):
            st.write(f"{i}. {insight}")
    
    with col2:
        st.markdown("### 🚀 마케팅 추천사항")
        for i, recommendation in enumerate(result.marketing_recommendations, 1):
            st.write(f"{i}. {recommendation}")
    
    # 결과 다운로드
    st.markdown("### 📥 결과 다운로드")
    formatted_result = st.session_state.cdp_service.format_analysis_results(result)
    
    st.download_button(
        label="📄 분석 결과 다운로드 (Markdown)",
        data=formatted_result,
        file_name="cdp_analysis_result.md",
        mime="text/markdown"
    )


def main():
    """메인 함수"""
    initialize_session_state()
    
    # 전체를 하나의 컨테이너로 감싸기
    st.markdown('<div class="content-wrapper">', unsafe_allow_html=True)
    
    render_header()
    
    # API 키 섹션
    render_api_key_section()
    
    # 메인 탭
    tab1, tab2, tab3 = st.tabs(["🎯 쿼리 분석", "🔍 컬럼 브라우저", "👥 팀별 추천"])
    
    with tab1:
        render_query_tab()
    
    with tab2:
        render_column_browser_tab()
    
    with tab3:
        render_team_scenarios_tab()
    
    st.markdown('</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()