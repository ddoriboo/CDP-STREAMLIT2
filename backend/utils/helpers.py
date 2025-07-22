"""유틸리티 함수들"""

import json
import streamlit as st
from typing import Any, Dict


def safe_json_loads(json_str: str) -> Dict[str, Any]:
    """안전한 JSON 파싱"""
    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        st.error(f"JSON 파싱 오류: {e}")
        return {}


def copy_to_clipboard_button(text: str, label: str = "복사"):
    """클립보드 복사 버튼"""
    if st.button(label):
        st.code(text)
        st.success("클립보드에 복사되었습니다!")


def format_priority(priority: str) -> str:
    """우선순위를 이모지와 함께 포맷팅"""
    priority_map = {
        'high': '🔴 높음',
        'medium': '🟡 보통', 
        'low': '🟢 낮음'
    }
    return priority_map.get(priority, f'⚪ {priority}')


def get_category_color(category: str) -> str:
    """카테고리별 색상 반환"""
    color_map = {
        'interests': '#FF6B6B',    # 빨간색
        'industries': '#4ECDC4',   # 청록색
        'scores': '#45B7D1',       # 파란색
        'demographics': '#96CEB4', # 초록색
        'basic': '#FFEAA7'         # 노란색
    }
    return color_map.get(category, '#DDD')


def validate_sql_query(sql: str) -> tuple[bool, str]:
    """SQL 쿼리 기본 유효성 검사"""
    if not sql.strip():
        return False, "SQL 쿼리가 비어있습니다."
    
    sql_lower = sql.lower().strip()
    
    if not sql_lower.startswith('select'):
        return False, "SELECT 문만 허용됩니다."
    
    if 'fsight__db_cp.mart_latest' not in sql_lower:
        return False, "올바른 테이블명(fsight__db_cp.mart_latest)을 사용해야 합니다."
    
    # 위험한 키워드 체크
    dangerous_keywords = ['drop', 'delete', 'update', 'insert', 'truncate', 'alter']
    for keyword in dangerous_keywords:
        if keyword in sql_lower:
            return False, f"'{keyword}' 키워드는 허용되지 않습니다."
    
    return True, "유효한 SQL 쿼리입니다."


def format_number(num: Any) -> str:
    """숫자를 읽기 쉬운 형태로 포맷팅"""
    try:
        if isinstance(num, str):
            # 숫자가 포함된 문자열에서 숫자만 추출 시도
            import re
            numbers = re.findall(r'\d+', str(num))
            if numbers:
                num = int(numbers[0])
            else:
                return str(num)
        
        if num >= 1_000_000:
            return f"{num / 1_000_000:.1f}M"
        elif num >= 1_000:
            return f"{num / 1_000:.1f}K"
        else:
            return str(num)
    except:
        return str(num)


def create_download_button(data: str, filename: str, label: str = "다운로드"):
    """다운로드 버튼 생성"""
    st.download_button(
        label=label,
        data=data,
        file_name=filename,
        mime='text/plain'
    )