"""This is python3.6 program."""

import json
import logging
import urllib.parse

from core.common_response import *
from domains.error.user_errors import UserNotFoundException
from domains.user.user import GetUsers

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    try:
        mode = None
        organization_id = event.get('organization_id')

        if organization_id is not None:
            mode = 'organization'

        assert mode

        last_evaluated_key = event.get('last_evaluated_key')
    except Exception as e:
        logger.exception(str(e))
        raise invalid_request_response(e)

    try:
        if mode == 'organization':
            get_user = GetUsers(search_key=organization_id, last_evaluated_key=last_evaluated_key)
            return get_user.get_by_organization_id()
    except Exception as e:
        logger.exception(str(e))
        if type(e) == UserNotFoundException:
            raise not_found_response(e)
        else:
            raise server_error(e)
