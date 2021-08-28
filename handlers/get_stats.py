import json

from utils.functions import get_stats, calculate_ratio


def handler(event, context):
    (count_mutant_dna, count_human_dna) = get_stats()[0]
    response = {
        "statusCode": 200,
        "body": json.dumps({
            "count_mutant_dna": count_mutant_dna,
            "count_human_dna": count_human_dna,
            "ratio": calculate_ratio(count_mutant_dna, count_human_dna)
        })
    }
    return response
