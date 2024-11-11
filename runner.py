import csv

from constants import ANONYMIZE, LLM_MODELS
import ell
import polars as pl

from anonymizer import anonymize_message
from moral_foundations import (
    MoralFoundations,
    assess_moral_foundations,
    process_moral_foundations,
)

# If we want to log the calls
# ell.init(store='./logdir', autocommit=True)


def main():
    for model in LLM_MODELS:
        build_for_model(model)


def build_for_model(model: str):
    
    dfs = []
    model_name = model.split(":")[0]

    with open('trump-tweets-filtered-sampled.csv', 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            author = row['author']
            source = row['source'] 
            quote = row['quote']
            direct_foundations = process_moral_foundations(model, quote)

            # Convert single row to DataFrame and append
            for foundations in direct_foundations:
                dfs.append(pl.DataFrame([get_dict_from_foundations(model_name, author, source, quote, foundations)]))
 
            if ANONYMIZE:
                anonymized = anonymize_message(quote,api_params=(dict(model=model)))                
                anonymized_foundations = process_moral_foundations(model, anonymized)
                for foundations in anonymized_foundations:
                    dfs.append(pl.DataFrame([get_dict_from_foundations(model_name, f"{author}-anon", source, anonymized, foundations)]))

    df = pl.concat(dfs)
    df.write_parquet(f'trump-{model_name}.parquet')


def append_to_df(df: pl.DataFrame, dict: dict):
    df.extend(pl.DataFrame([dict]))

def get_dict_from_foundations(model, author, source, quote, foundations: MoralFoundations):    
    # Create a dictionary with all data for one row
    #print(foundations)
    row_dict = {
        'model': model,
        'author': author,
        'source': source, 
        'quote': quote,
        'care': foundations.care,
        'fairness': foundations.fairness,
        'loyalty': foundations.loyalty,
        'authority': foundations.authority,
        'sanctity': foundations.sanctity,
        'liberty': foundations.liberty
    }
    return row_dict


if __name__ == "__main__":
    main()    

