class ErrorConfigBase(Exception):
    def __init__(self, message, error_config, status_code=None) -> None:
        super().__init__()
        self.message = message
        self.error_config = error_config
        self.status_code = status_code

    def to_dict(self):
        return {
            'href': self.error_config['reference'],
            'title': self.message,
            'translation': self.error_config['translation'],
            'type': self.error_config['type']
        }


class CompanyCodeInvalid(ErrorConfigBase):
    status_code = 400

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        status_code = kwargs.get('status_code')
        self.status_code = status_code or CompanyCodeInvalid.status_code


class ActionInvalid(ErrorConfigBase):
    status_code = 501

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        status_code = kwargs.get('status_code')
        self.status_code = status_code or ActionInvalid.status_code


class MandateDataInvalid(ErrorConfigBase):
    status_code = 400

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        status_code = kwargs.get('status_code')
        self.status_code = status_code or MandateDataInvalid.status_code


class MandateSubdelegateDataInvalid(ErrorConfigBase):
    status_code = 400

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        status_code = kwargs.get('status_code')
        self.status_code = status_code or MandateSubdelegateDataInvalid.status_code


class MandateNotFound(ErrorConfigBase):
    status_code = 404

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        status_code = kwargs.get('status_code')
        self.status_code = status_code or MandateNotFound.status_code


class UnprocessableRequestError(ErrorConfigBase):
    status_code = 422

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        status_code = kwargs.get('status_code')
        self.status_code = status_code or UnprocessableRequestError.status_code