import json

from utils.functions import get_stats


def handler(event, context):
    (count_mutant_dna, count_human_dna) = get_stats()[0]
    response = {
        "statusCode": 200,
        "body": json.dumps({
            "count_mutant_dna": count_mutant_dna,
            "count_human_dna": count_human_dna,
            "ratio": count_mutant_dna / count_human_dna
        })
    }
    return response
