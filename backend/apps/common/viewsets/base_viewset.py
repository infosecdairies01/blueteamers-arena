from rest_framework import viewsets, status
from rest_framework.response import Response
from apps.common.utils.response import success_response, error_response


class BaseAPIViewSet(viewsets.ViewSet):
    """
    Base ViewSet providing helper methods for standard JSON responses.
    """
    def success(self, data=None, message="Success", status_code=status.HTTP_200_OK) -> Response:
        return success_response(data=data, message=message, status_code=status_code)

    def error(self, message="An error occurred", errors=None, status_code=status.HTTP_400_BAD_REQUEST) -> Response:
        return error_response(message=message, errors=errors, status_code=status_code)


class BaseGenericModelViewSet(viewsets.ModelViewSet):
    """
    Base ModelViewSet integrating unified success responses.
    """
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return success_response(data=response.data, message=f"{self.basename.capitalize()} items retrieved successfully.")

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return success_response(data=response.data, message=f"{self.basename.capitalize()} retrieved successfully.")

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return success_response(data=response.data, message=f"{self.basename.capitalize()} created successfully.", status_code=status.HTTP_201_CREATED)
