import os
import asyncio
from typing import Dict, Any
import openai

class OpenAIAdapter:
    def __init__(self, team_name: str, perspective: str):
        self.team_name = team_name
        self.perspective = perspective
        self.client = openai.AsyncOpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
        )
        self.model = "gpt-4"

    async def generate_response(self, prompt: str) -> str:
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": f"당신은 {self.team_name}입니다. {self.perspective}에서 답변해주세요."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"[ERROR] OpenAI API 호출 실패: {str(e)}"

    async def conduct_team_discussion(self, question: str) -> Dict[str, Any]:
        """팀 토론을 진행하고 각 역할별 의견을 수집"""
        
        # Leader 역할
        leader_prompt = f"""
        질문: {question}
        
        당신은 팀 리더입니다. 이 주제에 대해 전체적인 방향성과 핵심 포인트를 제시해주세요.
        3-4개의 주요 관점을 간결하게 정리해주세요.
        """
        
        # Blue Hat (긍정적 관점)
        blue_prompt = f"""
        질문: {question}
        
        당신은 Blue Hat 역할입니다. 이 주제의 긍정적인 측면과 기회요소를 분석해주세요.
        실현 가능한 장점들을 구체적으로 제시해주세요.
        """
        
        # Research/Alternative (대안 제시)
        research_prompt = f"""
        질문: {question}
        
        당신은 연구자 역할입니다. 이 주제에 대한 대안적 접근방법이나 혁신적인 아이디어를 제시해주세요.
        기존과 다른 관점에서의 해결책을 제안해주세요.
        """
        
        # Red Hat (위험 분석)
        red_prompt = f"""
        질문: {question}
        
        당신은 Red Hat 역할입니다. 이 주제의 위험요소와 우려사항을 분석해주세요.
        잠재적 문제점들을 구체적으로 지적해주세요.
        """

        try:
            # 각 역할별로 동시에 API 호출
            tasks = [
                self.generate_response(leader_prompt),
                self.generate_response(blue_prompt),
                self.generate_response(research_prompt),
                self.generate_response(red_prompt)
            ]
            
            leader, blue, research, red = await asyncio.gather(*tasks)
            
            # 최종 요약 생성
            summary_prompt = f"""
            다음은 우리 팀의 토론 결과입니다:
            
            리더 의견: {leader}
            긍정적 관점: {blue}
            대안 제시: {research}
            위험 분석: {red}
            
            이를 종합하여 {question}에 대한 최종 결론을 3-4문장으로 요약해주세요.
            """
            
            summary = await self.generate_response(summary_prompt)
            
            return {
                "leader": leader,
                "blue": blue,
                "alternative": research,
                "red": red,
                "final_solution": summary
            }
            
        except Exception as e:
            return {
                "leader": f"[ERROR] 리더 의견 생성 실패: {str(e)}",
                "blue": f"[ERROR] Blue Hat 분석 실패: {str(e)}",
                "alternative": f"[ERROR] 대안 제시 실패: {str(e)}",
                "red": f"[ERROR] Red Hat 분석 실패: {str(e)}",
                "final_solution": f"[ERROR] 최종 요약 생성 실패: {str(e)}"
            }

