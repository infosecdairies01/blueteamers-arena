from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger("apps")


def custom_exception_handler(exc, context):
    """
    Custom DRF exception handler mapping exceptions into standardized error JSON format.
    """
    response = exception_handler(exc, context)

    if response is not None:
        custom_data = {
            "success": False,
            "message": "Validation or execution error occurred.",
            "errors": response.data,
        }
        
        # Standardize detail messages
        if isinstance(response.data, dict) and "detail" in response.data:
            custom_data["message"] = str(response.data["detail"])
            del response.data["detail"]
            custom_data["errors"] = response.data

        response.data = custom_data
    else:
        logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
        response = Response(
            {
                "success": False,
                "message": "An unexpected internal server error occurred.",
                "errors": {"detail": str(exc)},
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return response
