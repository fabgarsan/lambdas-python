import json

from utils.db import db
from utils.functions import create_mutant


def handler(event, context):
    body = json.loads(event['body'])
    dna = body.get('dna', None)
    result = create_mutant(dna)
    if result:
        response = {
            "statusCode": 200,
            "body": "It's Mutant"
        }
    else:
        response = {
            "statusCode": 403
        }

    db.begin_transaction()
    db.commit()
    return response
