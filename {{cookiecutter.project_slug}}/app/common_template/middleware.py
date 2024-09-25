# ruff: noqa: RET503
from django.http import HttpResponse
from django.http import HttpResponseForbidden
from django.utils.deprecation import MiddlewareMixin


class HealthCheckMiddleware(MiddlewareMixin):
    # This must be done as a middleware because it must be done before the Host header
    # is checked (ECS sets the host headers to the IP address of the ELB)
    def process_request(self, request):
        if request.META["PATH_INFO"][:13] == "/health-check":
            return HttpResponse("I'm alive!")


class InjectBusinessMiddleware(MiddlewareMixin):
    def process_request(self, request):
        header_business_id = request.headers.get("x-business-id", None)
        if header_business_id:
            request.business_id = header_business_id
        elif (
            request.META["PATH_INFO"][:4] == "/api"
            and request.META["PATH_INFO"][:15] != "/api/v1/schema/"
            and request.META["PATH_INFO"][:11] != "/api/schema"
            and request.META["PATH_INFO"][:9] != "/api/docs"
        ):
            return HttpResponseForbidden(
                "X-Business-Id header value is required for API calls",
            )
