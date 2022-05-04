class BaseError:
    __abstract__ = True
    errors = None
    message = "Success"
    status = 200

    def __init__(self, **kwargs):
        self.errors = None
        self.error = None

        for (key, value) in kwargs.items():
            self.__setattr__(key, value)

    def __call__(self, *args, **kwargs):
        self.errors = None

        for (key, value) in kwargs.items():
            self.__setattr__(key, value)

        response = {}

        if self.error is not None:
            response['error'] = self.error

        if self.errors is not None:
            response['errors'] = self.errors

        if self.errors is not None:
            response["message"] = self.message

        return response,  self.status

    def __del__(self):
        self.data = None
        self.message = 'Success'
        self.error = None
        self.errors = None
        self.status = 200


class SuccessResponse:
    status = 200
    data = None
    message = 'Success'

    def __init__(self, **kwargs):
        for (key, value) in kwargs.items():
            self.__setattr__(key, value)

    def __call__(self, **kwargs):
        self.errors = None
        self.data = None

        for (key, value) in kwargs.items():
            self.__setattr__(key, value)

        if not self.data:
            return {"message": self.message}, self.status

        return self.data, self.status

    def __del__(self):
        self.data = None
        self.message = 'Success'


class UnprocessableEntityError(BaseError):
    message = 'Unprocessable entity'
    status = 422


class NotFoundError(BaseError):
    errors = None
    message = "Not found"
    status = 404


class UnauthorizedError(BaseError):
    errors = None
    message = "Unauthorized"
    status = 401


class ForbiddenError(BaseError):
    errors = None
    message = "Forbidden"
    status = 403


class BadRequestError(BaseError):
    errors = None
    message = "Bad request"
    status = 400


class InternalServerError(BaseError):
    error = None
    message = "Internal server error"
    status = 500


UnprocessableEntity = UnprocessableEntityError()
NotFound = NotFoundError()
InternalServerError = InternalServerError()
Forbidden = ForbiddenError()
BadRequest = BadRequestError()
Unauthorized = UnauthorizedError()
Success = SuccessResponse()
