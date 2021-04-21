import json
import sys
import uuid
from typing import Optional

from loguru import logger
from enum import Enum

from .singleton import SingletonMeta


class LogType(str, Enum):
    HTTP_REQUEST = "HTTP_REQUEST"
    HTTP_RESPONSE = "HTTP_RESPONSE"
    SQL = "SQL"
    FUNC = "FUNC"


class LogLevel(str, Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARN = "WARN"
    ERROR = "ERROR"


class RestLogger(metaclass=SingletonMeta):
    def __init__(self):
        self._request_id = None

    @classmethod
    def init_logger(cls):
        logger.remove()
        logger.add(sys.stdout, colorize=True, format="{message}")

    @classmethod
    def log_it(cls, level: LogLevel, log_item: dict):
        if level == LogLevel.DEBUG:
            logger.debug(json.dumps(log_item))
        if level == LogLevel.INFO:
            logger.info(json.dumps(log_item))
        if level == LogLevel.WARN:
            logger.warning(json.dumps(log_item))
        if level == LogLevel.ERROR:
            logger.error(json.dumps(log_item))

    @property
    def request_id(self):
        if not self._request_id:
            return None
        return str(self._request_id)

    @request_id.setter
    def request_id(self, request_id):
        try:
            self._request_id = uuid.UUID(str(request_id))
        except ValueError:
            raise ValueError("request id must be a UUID string")

    def log_http_response(self, formatted_process_time, status_code, headers, level: LogLevel = LogLevel.INFO):
        headers_dict = {item[0]: item[1] for item in headers.items()}
        log = {"request_id": self.request_id,
               "log_type": LogType.HTTP_RESPONSE,
               "log_level": level,
               "completed_in_ms": formatted_process_time,
               "status_code": status_code,
               "headers": headers_dict}
        RestLogger.log_it(level, log)

    def log_http_request(self, route, method, headers, queryparams=None, level: LogLevel = LogLevel.INFO):
        headers_dict = {item[0]: item[1] for item in headers.items()}
        log = {"request_id": self.request_id,
               "log_type": LogType.HTTP_REQUEST,
               "log_level": level,
               "url": str(route),
               "method": method,
               "headers": headers_dict}
        if queryparams:
            log["queryparams"] = str(queryparams)
        RestLogger.log_it(level, log)

    def log_sql_query(self, sql_query: str, record_num: Optional[int] = None, level: LogLevel = LogLevel.INFO):
        log = {"request_id": self.request_id, "log_type": LogType.SQL, "log_level": level, "query": str(sql_query)}
        if record_num:
            log["record_found"] = record_num
        RestLogger.log_it(level, log)

    def log_function(self, module_name: str, function_name: str, message: str, line_no: int,
                     level: LogLevel = LogLevel.INFO):
        log = {"request_id": self.request_id,
               "log_type": LogType.FUNC,
               "log_level": level,
               "module_name": module_name,
               "function_name": function_name,
               "message": message,
               "lineno": line_no}
        RestLogger.log_it(level, log)


log_http_request = RestLogger.instance.log_http_request
log_http_response = RestLogger.instance.log_http_response
log_sql_query = RestLogger.instance.log_sql_query
log_function = RestLogger.instance.log_function
