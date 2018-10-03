"""This is python3.6 program."""

import os

import boto3
from boto3.dynamodb.conditions import Key

from domains.user.user import GetUsers

DYNAMODB_ENDPOINT = os.getenv('DYNAMODB_ENDPOINT')
NOTE_USER_TABLE_NAME = os.getenv('NOTE_USER_TABLE_NAME')
DYNAMO = boto3.resource('dynamodb', endpoint_url=DYNAMODB_ENDPOINT)
DYNAMODB_TABLE = DYNAMO.Table(NOTE_USER_TABLE_NAME)

USER_LIST_LIMIT = int(os.getenv('USER_LIST_LIMIT'))


def get_users_by_organization_id(request: GetUsers):
    param = {
        'IndexName': 'user_organization_id-index',
        'KeyConditionExpression': Key('organization_id').eq(request.search_key),
        'ScanIndexForward': False,
        'Limit': USER_LIST_LIMIT
    }

    if request.last_evaluated_key is not None:
        param['ExclusiveStartKey'] = request.last_evaluated_key

    return DYNAMODB_TABLE.query(**param)
