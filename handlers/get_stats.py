import json

from utils.functions import get_stats, calculate_ratio


def handler(event, context):
    (count_mutant_dna, count_human_dna) = get_stats()[0]
    response = {
        "statusCode": 200,
        "body": json.dumps({
            "count_mutant_dna": count_mutant_dna if count_mutant_dna is not None else 0,
            "count_human_dna": count_human_dna if count_human_dna is not None else 0,
            "ratio": calculate_ratio(count_mutant_dna, count_human_dna)
        })
    }
    return response
