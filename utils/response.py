from rest_framework.response import Response


class CustomResponse:
    @staticmethod
    def success(data=None, message="Success", status_code=200):
        return Response({
            "success": True,
            "message": message,
            "data": data
        }, status=status_code)

    @staticmethod
    def error(message="Error", errors=None, status_code=400):
        return Response({
            "success": False,
            "message": message,
            "data": {"errors": errors}
        }, status=status_code)
