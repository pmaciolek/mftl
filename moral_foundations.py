from typing import List, Optional

import ell
from pydantic import BaseModel, Field

from constants import DEFAULT_LLM_MODEL, REPEAT_COUNT


class MoralFoundations(BaseModel):
    care: Optional[float] = Field(description="The score for Harm vs Care")
    fairness: Optional[float] = Field(description="The score for Cheating vs Fairness")
    loyalty: Optional[float] = Field(description="The score for Betrayal vs Loyalty")
    authority: Optional[float] = Field(description="The score for Subversion vs Authority")
    sanctity: Optional[float] = Field(description="The score for Degradation vs Sanctity")
    liberty: Optional[float] = Field(description="The score for Oppression vs Liberty")



@ell.complex(model=DEFAULT_LLM_MODEL, n=REPEAT_COUNT)
def assess_moral_foundations(message: str):
    """You are a Moral Foundations Theory analyzer. You are given an X (formerly, Twitter) post to judge. 
       Measure how author of the text is using the Jonathan Haidt's six moral foundations:
                    - care (max harm being -10 and max care being 10)
                    - fairness (max cheating being -10 and max fairness being 10)
                    - loyalty (max betrayal being -10 and max loyalty being 10)
                    - authority (max Subversion being -10 and max authority being 10)
                    - sanctity (max degradation being -10 and max sanctity being 10)
                    - liberty (max oppression being -10 and max liberty being 10)
                    
                    Rate each foundation on a scale from -10 (strong negative), 
                    through 0 (neutral or no sentiment related to the foundation), to +10 (strong positive). 
                    Use intermediate values (e.g. -5, 2) if needed. 
                    You must absolutely respond in JSON format with no exceptions. Do not add formatting or newline characters, no other text. 
                    Do not use plus (+) signs in the JSON result
                    """
                    # You must absolutely respond in this format with no exceptions {MoralFoundations.model_json_schema()}
    return f"Measure the moral foundations of the following text: {message}"

def parse_response(response: str) -> MoralFoundations:
    try:
        # Fix simple errors made by some lLMs
        response = response.replace(" \"", "\"").replace("\" ", "\"").lower()
        return MoralFoundations.model_validate_json(response)
    except Exception as e:
        print(f"Error parsing response: {response} due to {e}")
        return None

def get_list_of_results(model: str, message: str) -> List[MoralFoundations]:
    try:
        results = assess_moral_foundations(message, api_params=(dict(model=model)))

        # When "n" was supported
        parsed_results = []
        if isinstance(results, list):
            parsed_results =list(map(lambda result: parse_response(result.text), results))
        else:
            parsed_results.append(parse_response(results.text))

        # Filter out None values            
        return [result for result in parsed_results if result is not None]
    except Exception as e:
        print(e)
        return []

def process_moral_foundations(model, message: str)-> List[MoralFoundations]:
    results = get_list_of_results(model, message)
    if len(results) < REPEAT_COUNT:
        # The engine does not support multiple N, so we need to repeat the request  
        for _ in range(REPEAT_COUNT - len(results)):
            continuation = get_list_of_results(model, message)
            for result in continuation:
                results.append(result)
            # Check if we have enough results, e.g. when original lack of results was due to the engine
            # not allowing to process the input for some reason
            if len(results) >= REPEAT_COUNT:
                break
                
    print(results)
    return results
