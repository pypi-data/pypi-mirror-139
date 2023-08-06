class BGExceptions:
    def prepare_error_message(msg: str, status_code: int):
        return {
            "code": int(status_code),
            "message": msg,
        }


class TelegramExceptions:
    pass
