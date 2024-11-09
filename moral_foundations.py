from typing import List, Optional

import ell
from pydantic import BaseModel, Field

from constants import LLM_MODEL, REPEAT_COUNT


class MoralFoundations(BaseModel):
    care: Optional[float] = Field(description="The score for Harm vs Care")
    fairness: Optional[float] = Field(description="The score for Cheating vs Fairness")
    loyalty: Optional[float] = Field(description="The score for Betrayal vs Loyalty")
    authority: Optional[float] = Field(description="The score for Subversion vs Authority")
    sanctity: Optional[float] = Field(description="The score for Degradation vs Sanctity")
    liberty: Optional[float] = Field(description="The score for Oppression vs Liberty")



# @ell.complex(model=LLM_MODEL, response_format=MoralFoundations, n= 10)
# def assess_moral_foundations(message: str) -> List[MoralFoundations]:
@ell.complex(model=LLM_MODEL, response_format=MoralFoundations, n=REPEAT_COUNT)
def assess_moral_foundations(message: str):
    """You are a moral foundations analyzer. Assess the text according to Jonathan Haidt's six moral foundations:
                    - care (max harm being -10 and max care being 10)
                    - fairness (max cheating being -10 and max fairness being 10)
                    - loyalty (max betrayal being -10 and max loyalty being 10)
                    - authority (max Subversion being -10 and max authority being 10)
                    - sanctity (max degradation being -10 and max sanctity being 10)
                    - liberty (max oppression being -10 and max liberty being 10)
                    
                    Rate each foundation on a scale from -10 (strong negative), 
                    through 0 (neutral or no sentiment related to the foundation), to +10 (strong positive). 
                    Use intermediate values (e.g. -5, 2) if needed. 
                    Provide just the result in JSON format, without formatting, no other text."""
    return f"{message}"

def get_list_of_results(message: str) -> List[MoralFoundations]:
    try:
        results = assess_moral_foundations(message)
        print(results)
    except Exception as e:
        print(e)
        return []
    return list(map(lambda result: result.parsed, results))

def process_moral_foundations(message: str)-> List[MoralFoundations]:
    results = get_list_of_results(message)
    if len(results) < REPEAT_COUNT:
        # The engine does not support multiple N, so we need to repeat the request  
        for _ in range(REPEAT_COUNT - len(results)):
            continuation = get_list_of_results(message)
            for result in continuation:
                results.append(result)
            # Check if we have enough results, e.g. when original lack of results was due to the engine
            # not allowing to process the input for some reason
            if len(results) >= REPEAT_COUNT:
                break
                
    return results
