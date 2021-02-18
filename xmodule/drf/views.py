from django.http.response import HttpResponseBase
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.generics import GenericAPIView as DrfGenericAPIView
from rest_framework.response import Response
from rest_framework.views import set_rollback


class GenericAPIView(DrfGenericAPIView):
    def finalize_response(self, request, response, *args, **kwargs):
        if response is None:
            response = Response(status=status.HTTP_204_NO_CONTENT)
        elif not isinstance(response, HttpResponseBase):
            response = Response(response)

        return super(GenericAPIView, self).finalize_response(request, response, *args, **kwargs)

    def handle_exception(self, exc):
        if isinstance(exc, APIException):
            headers = {}
            auth_header = getattr(exc, 'auth_header', None)
            if auth_header:
                headers['WWW-Authenticate'] = auth_header

            wait = getattr(exc, 'wait', None)
            if wait:
                headers['Retry-After'] = '%d' % wait

            data = exc.get_full_details()
            set_rollback()
            return Response(data, status=exc.status_code, headers=headers)

        return super().handle_exception(exc)


class NoRequestEchoMixin:
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({}, status=status.HTTP_201_CREATED)
