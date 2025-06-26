#!/usr/bin/env python3
"""
Test script for the news_analyst agent.
This script tests the news analyst functionality without requiring real API calls.
"""

from unittest.mock import patch

# Import the news_analyst agent
from manager.specialist.news_analyst.agent import news_analyst


def test_news_analyst_without_api() -> None:
    """Test the news analyst with mocked Google Search responses."""

    print("Testing News Analyst Agent")
    print("=" * 40)

    # Mock successful Google Search response
    mock_search_results: list[dict[str, str]] = [
        {
            "title": "AI Breakthrough: New Model Surpasses Human Performance",
            "link": "https://example.com/ai-news-1",
            "snippet": "Researchers have developed a new AI model that outperforms humans in complex reasoning tasks.",
        },
        {
            "title": "Tech Companies Invest Billions in AI Research",
            "link": "https://example.com/ai-news-2",
            "snippet": "Major tech companies announced increased funding for artificial intelligence research and development.",
        },
    ]

    # Test with mocked Google Search
    print("\n1. Testing with mocked successful Google Search response:")
    with patch("google.adk.tools.google_search") as mock_search:
        mock_search.return_value = mock_search_results

        # Can't directly test the agent's response since it uses an LLM,
        # but can verify that the tool would be called correctly
        print(f"Mock search would return {len(mock_search_results)} results")
        print(f"First result title: {mock_search_results[0]['title']}")
        print(f"First result snippet: {mock_search_results[0]['snippet']}")

        # Verify the agent has the correct configuration
        assert news_analyst.name == "news_analyst"
        assert "google_search" in [
            getattr(tool, "name", getattr(tool, "tool_name", tool.__class__.__name__))
            for tool in news_analyst.tools
        ]
        assert "analyze news" in news_analyst.instruction.lower()

    # Test with empty search results
    print("\n2. Testing with empty search results:")
    with patch("google.adk.tools.google_search") as mock_search:
        mock_search.return_value = []

        print("Mock search would return empty results")
        # In a real scenario, the agent should handle this gracefully

    # Test with error in search
    print("\n3. Testing with search error:")
    with patch("google.adk.tools.google_search") as mock_search:
        mock_search.side_effect = Exception("API connection error")

        print("Mock search would raise an exception")
        # In a real scenario, the agent should handle this gracefully

    print("\n" + "=" * 40)
    print("All tests completed! ✅")


if __name__ == "__main__":
    test_news_analyst_without_api()
