"""
test_app.py — Unit Tests for Election Buddy
=============================================
Tests core utility functions and mocks the Gemini API to verify
chat behaviour without making real API calls.

Run:
    pytest tests/test_app.py -v
"""

from unittest.mock import MagicMock, patch
import pytest

from utils.election_data import (
    get_election_key_dates,
    get_voting_systems_info,
    get_quick_facts,
    format_dates_for_display,
)


# ──────────────────────────────────────────────────────────────────────────────
# Test 1: Data formatting — format_dates_for_display
# ──────────────────────────────────────────────────────────────────────────────

class TestFormatDatesForDisplay:
    """Tests for the Markdown table formatter."""

    def test_formats_dates_into_markdown_table(self):
        """Verify that election dates are formatted as a valid Markdown table."""
        dates = [
            {
                "event": "Test Election",
                "date": "January 1, 2030",
                "description": "A test election event.",
            }
        ]
        result = format_dates_for_display(dates)

        # Should contain table structure
        assert "| Event | Date | Description |" in result
        assert "|---|---|---|" in result
        # Should contain the test data
        assert "Test Election" in result
        assert "January 1, 2030" in result
        assert "A test election event." in result

    def test_returns_fallback_for_empty_list(self):
        """Verify graceful handling of empty date lists."""
        result = format_dates_for_display([])
        assert "No election dates available" in result

    def test_multiple_dates_all_present(self):
        """Verify all entries appear when multiple dates are provided."""
        dates = get_election_key_dates()
        result = format_dates_for_display(dates)
        for d in dates:
            assert d["event"] in result


# ──────────────────────────────────────────────────────────────────────────────
# Test 2: Mock Gemini API — send_message
# ──────────────────────────────────────────────────────────────────────────────

class TestGeminiAPIIntegration:
    """Tests that mock the Gemini API to verify chat flow."""

    @patch("utils.gemini_helper.genai")
    def test_send_message_returns_model_response(self, mock_genai):
        """Verify that send_message correctly returns the model's text."""
        from utils.gemini_helper import send_message

        # Create a mock chat session
        mock_chat = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "Elections are the cornerstone of democracy."
        mock_chat.send_message.return_value = mock_response

        # Call send_message with the mock
        result = send_message(mock_chat, "What are elections?")

        # Assertions
        assert result == "Elections are the cornerstone of democracy."
        mock_chat.send_message.assert_called_once_with("What are elections?")

    @patch("utils.gemini_helper.genai")
    def test_send_message_raises_on_api_error(self, mock_genai):
        """Verify that API errors are wrapped in RuntimeError."""
        from utils.gemini_helper import send_message

        mock_chat = MagicMock()
        mock_chat.send_message.side_effect = Exception("Network timeout")

        with pytest.raises(RuntimeError, match="Gemini API error"):
            send_message(mock_chat, "Tell me about voting")


# ──────────────────────────────────────────────────────────────────────────────
# Test 3: Static data integrity
# ──────────────────────────────────────────────────────────────────────────────

class TestStaticDataIntegrity:
    """Ensure static data modules return well-structured data."""

    def test_election_dates_have_required_keys(self):
        """Each date entry must have event, date, and description keys."""
        dates = get_election_key_dates()
        assert len(dates) > 0, "Should return at least one election date"
        for entry in dates:
            assert "event" in entry
            assert "date" in entry
            assert "description" in entry

    def test_voting_systems_have_required_keys(self):
        """Each voting system entry must have system, description, used_in."""
        systems = get_voting_systems_info()
        assert len(systems) > 0, "Should return at least one voting system"
        for entry in systems:
            assert "system" in entry
            assert "description" in entry
            assert "used_in" in entry

    def test_quick_facts_are_non_empty_strings(self):
        """Quick facts should be a list of non-empty strings."""
        facts = get_quick_facts()
        assert len(facts) > 0, "Should return at least one fact"
        for fact in facts:
            assert isinstance(fact, str)
            assert len(fact) > 0
