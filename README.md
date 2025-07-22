# CDP AI 자연어 쿼리 플랫폼

네이버 CDP (Customer Data Platform) 데이터를 기반으로 자연어 질문을 통해 고객 세그먼테이션 전략을 제공하는 AI 플랫폼입니다.

## 🏗️ 아키텍처

### Backend-Frontend 분리 구조
```
├── app.py (Streamlit Frontend)
├── backend/
│   ├── services/ (비즈니스 로직)
│   │   ├── ai_service.py (OpenAI API 통신)
│   │   └── cdp_service.py (CDP 관련 로직)
│   ├── models/ (데이터 모델)
│   ├── config/ (설정 및 CDP 컬럼 정의)
│   └── utils/ (유틸리티)
```

### 주요 특징
- **Frontend**: Streamlit으로 UI만 담당
- **Backend**: Python으로 비즈니스 로직 구현
- **AI 통합**: OpenAI GPT-4o를 활용한 자연어 쿼리 분석
- **CDP 데이터**: 네이버 CDP 컬럼 정의 및 추천 시스템

## 🚀 실행 방법

1. 필요한 패키지 설치:
```bash
pip install -r requirements.txt
```

2. Streamlit 앱 실행:
```bash
streamlit run app.py
```

3. 브라우저에서 `http://localhost:8501` 접속

## 🔧 설정

- OpenAI API 키가 필요합니다
- 사이드바에서 API 키를 입력하고 검증하세요

## 📊 주요 기능

1. **자연어 쿼리**: 일반 언어로 고객 세그먼트 질문
2. **AI 분석**: GPT-4o가 최적의 CDP 컬럼 추천
3. **컬럼 탐색기**: CDP 컬럼 검색 및 탐색
4. **팀별 시나리오**: 마케팅, 금융, 리테일 팀별 예제 제공
5. **결과 다운로드**: 분석 결과를 Markdown 형태로 다운로드

## 🎯 사용 예시

**질문**: "20-30대 여성 고객 중에서 온라인 쇼핑을 자주 하는 고객들을 찾고 싶습니다."

**AI 분석 결과**:
- 추천 컬럼들 (우선순위별)
- SQL 쿼리 생성
- 비즈니스 인사이트
- 마케팅 추천사항

## 🔄 변경사항

**Before**: HTML/JavaScript로 모든 로직 구현
**After**: Python Backend + Streamlit Frontend 분리

- 모든 비즈니스 로직을 Python으로 이전
- OpenAI API 통신을 Backend에서 처리
- Streamlit은 순수 UI만 담당