from rest_framework.exceptions import APIException


class NotFoundError(APIException):
    status_code = 404
    default_detail = "Not found"
    default_code = "not_found"

    def __init__(self, detail=None):
        super().__init__(detail or self.default_detail)


class PermissionDeniedError(APIException):
    status_code = 403
    default_detail = "Permission denied"
    default_code = "permission_denied"

    def __init__(self, detail=None):
        super().__init__(detail or self.default_detail)


class ConflictError(APIException):
    status_code = 409
    default_detail = "Conflict"
    default_code = "conflict"

    def __init__(self, detail=None):
        super().__init__(detail or self.default_detail)


class DomainValidationError(APIException):
    status_code = 400
    default_detail = "Validation error"
    default_code = "validation_error"

    def __init__(self, detail=None):
        super().__init__(detail or self.default_detail)
