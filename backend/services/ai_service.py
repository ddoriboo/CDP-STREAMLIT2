"""OpenAI API 통신 서비스"""

import json
import openai
from typing import Optional

from ..config.settings import OPENAI_MODEL, SYSTEM_PROMPT
from ..config.cdp_columns import CDP_COLUMNS
from ..models.query_models import QueryAnalysisResult, ColumnRecommendation


class AIService:
    def __init__(self, api_key: str):
        self.client = openai.OpenAI(api_key=api_key)
    
    def analyze_query(self, user_query: str) -> Optional[QueryAnalysisResult]:
        """사용자 쿼리를 분석하여 CDP 추천을 제공"""
        try:
            # CDP 컬럼 정보를 포함한 시스템 프롬프트 생성
            system_prompt_with_columns = f"""{SYSTEM_PROMPT}

다음 CDP 컬럼들을 활용하여 분석해주세요:
{json.dumps(CDP_COLUMNS, ensure_ascii=False, indent=2)}"""

            response = self.client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt_with_columns
                    },
                    {
                        "role": "user",
                        "content": user_query
                    }
                ],
                temperature=0.1
            )
            
            # AI 응답 파싱
            response_content = response.choices[0].message.content.strip()
            
            # JSON 파싱
            try:
                result_data = json.loads(response_content)
            except json.JSONDecodeError:
                # JSON 파싱 실패시 응답 내용에서 JSON 부분만 추출 시도
                start_idx = response_content.find('{')
                end_idx = response_content.rfind('}') + 1
                if start_idx >= 0 and end_idx > start_idx:
                    json_content = response_content[start_idx:end_idx]
                    result_data = json.loads(json_content)
                else:
                    raise ValueError("유효한 JSON 응답을 찾을 수 없습니다.")
            
            # ColumnRecommendation 객체들 생성
            column_recommendations = [
                ColumnRecommendation(
                    column=col["column"],
                    description=col["description"], 
                    condition=col["condition"],
                    priority=col["priority"],
                    reasoning=col["reasoning"]
                )
                for col in result_data["recommended_columns"]
            ]
            
            # QueryAnalysisResult 객체 생성
            return QueryAnalysisResult(
                query_analysis=result_data["query_analysis"],
                target_description=result_data["target_description"],
                recommended_columns=column_recommendations,
                sql_query=result_data["sql_query"],
                business_insights=result_data["business_insights"],
                estimated_target_size=result_data["estimated_target_size"],
                marketing_recommendations=result_data["marketing_recommendations"]
            )
            
        except Exception as e:
            print(f"AI 분석 중 오류 발생: {e}")
            return None
    
    def test_api_key(self) -> tuple[bool, str]:
        """API 키 유효성 테스트"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": "Hello"}
                ],
                max_tokens=5
            )
            return True, "API 키가 유효합니다."
        except openai.AuthenticationError:
            return False, "API 키가 유효하지 않습니다."
        except openai.RateLimitError:
            return False, "API 호출 한도를 초과했습니다."
        except openai.APIError as e:
            return False, f"OpenAI API 오류: {e}"
        except Exception as e:
            return False, f"예상치 못한 오류: {e}"