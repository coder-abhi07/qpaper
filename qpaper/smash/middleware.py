from django.http import JsonResponse
from django.core.exceptions import PermissionDenied
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render


class CustomMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        response_data = {}
        status_code = None

        # Handle API exceptions
        if hasattr(exception, 'response'):
            response_data = exception.response.data
            status_code = exception.status_code

            # Check for specific error types
            if isinstance(response_data, dict) and 'error' in response_data:
                # Extract the error message
                error_message = response_data['error']
                response_data = {'error': error_message}

        # Handle PermissionDenied exceptions
        elif isinstance(exception, PermissionDenied):
            error_message = str(exception)
            status_code = 403

        # Handle other exceptions
        else:
            error_message = repr(exception)
            status_code = 500

        # Render a custom error page with the appropriate error message
        return render(request, 'error.html', {'error_message': error_message}, status=status_code)
