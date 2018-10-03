def invalid_request_response(error) -> Exception:
    return Exception(f'[InvalidRequest] {str(error)}')


def not_found_response(error) -> Exception:
    return Exception(f'[NotFound] {str(error)}')


def conflict_response(error) -> Exception:
    return Exception(f'[Conflict] {str(error)}')


def server_error(error) -> Exception:
    return Exception(f'[InternalServerError] {str(error)}')


def maintenance_response(error) -> Exception:
    return Exception(f'[Unavailable] {str(error)}')
