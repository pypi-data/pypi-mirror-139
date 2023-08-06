import requests
import json


class CustomResponse:

    def __init__(self):
        pass

    def __str__(self):
        return f"Response ===> #todo"

    class ChatException(Exception):
        def __init__(self, status_code=None, reason=None):
            self.status_code = status_code
            self.reason = reason

    @staticmethod
    def _response_schema(status_code: int, response: str):
        _response_dict = {
            'status': status_code,
            'message': json.loads(response)
        }
        return _response_dict

    @staticmethod
    def parse_response(_response: requests.Response, raise_exception: bool):
        if not _response:
            return {
                "status": 999,
                "message": "Timeout Handled by pygooglechat"
            }
        status_code = _response.status_code
        content = _response.content

        if status_code != requests.codes.ok:
            if raise_exception:
                raise CustomResponse.ChatException(status_code=status_code, reason=content)
            return CustomResponse._response_schema(status_code=status_code, response=content)
        return CustomResponse._response_schema(status_code=status_code, response=content)
