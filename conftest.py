
import pytest

import os
import sys



# Put global pytest fixtures here
@pytest.fixture
def client(request):
    """Django Rest Framework APIClient"""
    from rest_framework.test import APIClient

    return APIClient()
