def success_response(data=None, message="Success", status_code=200):
    body = {"success": True, "message": message}
    if data is not None:
        body["data"] = data
    return body, status_code


def error_response(message="Error", errors=None, status_code=400):
    body = {"success": False, "message": message}
    if errors is not None:
        body["errors"] = errors
    return body, status_code
