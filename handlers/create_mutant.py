import json

from utils.db import db
from utils.functions import create_mutant
from utils.custom_exceptions import CustomGeneralException


def handler(event, context):
    try:
        db.begin_transaction()
        body = json.loads(event['body'])
        dna = body.get('dna', None)
        result = create_mutant(dna)
        db.commit()
        if result:
            response = {
                "statusCode": 200,
                "body": "It's Mutant"
            }
        else:
            response = {
                "statusCode": 403
            }
        return response
    except CustomGeneralException as error:
        db.rollback()
        response = {
            "statusCode": error.status_code,
            "body": json.dumps(error.message)
        }
        return response
