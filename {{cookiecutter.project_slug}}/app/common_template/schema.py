from drf_spectacular.openapi import AutoSchema
from drf_spectacular.utils import OpenApiParameter


class CustomAutoSchema(AutoSchema):
    global_params = [
        OpenApiParameter(
            name="X-Business-Id",
            type=str,
            location=OpenApiParameter.HEADER,
            description="Business ID the user is currently working on/this API request "
            "should be for.",
        ),
    ]

    def get_override_parameters(self):
        params = super().get_override_parameters()
        return params + self.global_params
