import os

from django.test.runner import DiscoverRunner
from moto import mock_aws


class CustomDiscoverRunner(DiscoverRunner):
    def setup_test_environment(self, **kwargs):
        super().setup_test_environment(**kwargs)

        from django.test.utils import _TestState

        saved_data = _TestState.saved_data  # noqa: F841

        # TODO: Use to mock out other services
        # saved_data.embeddings_api_class = settings.EMBEDDINGS_API_CLASS  # noqa: ERA001, E501
        # settings.EMBEDDINGS_API_CLASS = "services.gcloud_vertext.TestEmbeddingsApi"  # noqa: ERA001, E501

        self.mock_aws = mock_aws()
        self.mock_aws.start()
        """Mocked AWS Credentials for moto."""
        os.environ["AWS_ACCESS_KEY_ID"] = "testing"
        os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"  # noqa: S105
        os.environ["AWS_SECURITY_TOKEN"] = "testing"  # noqa: S105
        os.environ["AWS_SESSION_TOKEN"] = "testing"  # noqa: S105
        os.environ["AWS_DEFAULT_REGION"] = "us-east-1"

    def teardown_test_environment(self, **kwargs):
        from django.test.utils import _TestState

        saved_data = _TestState.saved_data  # noqa: F841

        # TODO: Use to un-mock out other services
        # settings.EMBEDDINGS_API_CLASS = saved_data.embeddings_api_class  # noqa: ERA001, E501

        self.mock_aws.stop()

        super().teardown_test_environment(
            **kwargs,
        )  # Must come last; deletes the saved_data object
