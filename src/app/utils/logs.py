
def log_http_response(request_id, formatted_process_time, status_code):
    log = {"request_id": request_id, "completed_in_ms": formatted_process_time, "status_code": status_code}
    return log
