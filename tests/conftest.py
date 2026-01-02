import pytest
from unittest.mock import MagicMock
import sys

# Mocking streamlit before modules are imported
sys.modules["streamlit"] = MagicMock()
import streamlit as st  # noqa: E402


class SessionState(dict):
    """Custom dictionary that supports dot notation access."""

    def __getattr__(self, item):
        try:
            return self[item]
        except KeyError:
            raise AttributeError(
                f"'SessionState' object has no attribute '{item}'"
            )

    def __setattr__(self, key, value):
        self[key] = value


@pytest.fixture
def mock_streamlit():
    """Mocks streamlit session_state and other common functions."""
    # Setup session state as a mock that supports
    # both dict and attribute access
    st.session_state = SessionState()
    st.error = MagicMock()
    st.warning = MagicMock()
    st.success = MagicMock()
    return st


@pytest.fixture
def mock_auth_token(mock_streamlit):
    """Sets a dummy token in the mocked session/state."""
    mock_streamlit.session_state["token"] = "dummy_token"
    return "dummy_token"
