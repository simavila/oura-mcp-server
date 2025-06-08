"""Oura API client for fetching ring data."""

import os
from datetime import datetime, date
from typing import Dict, Any, Optional, List
import requests
from dotenv import load_dotenv

class OuraClient:
    """Client for interacting with the Oura API."""
    
    BASE_URL = "https://api.ouraring.com/v2/usercollection"
    
    def __init__(self, api_token: Optional[str] = None):
        """Initialize the Oura client.
        
        Args:
            api_token: Oura API personal access token. If not provided,
                      will try to load from OURA_API_TOKEN environment variable.
        """
        # Load environment variables only when needed
        load_dotenv()
        
        self.api_token = api_token or os.getenv("OURA_API_TOKEN")
        if not self.api_token:
            raise ValueError(
                "Oura API token not found. Please set OURA_API_TOKEN in your .env file "
                "or pass it directly to OuraClient."
            )
        
        self.headers = {
            "Authorization": f"Bearer {self.api_token}"
        }
    
    def _make_request(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a request to the Oura API.
        
        Args:
            endpoint: API endpoint (e.g., "sleep", "activity")
            params: Query parameters
            
        Returns:
            JSON response from the API
            
        Raises:
            requests.HTTPError: If the API request fails
        """
        url = f"{self.BASE_URL}/{endpoint}"
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                raise ValueError(
                    "Authentication failed. Please check your Oura API token."
                ) from e
            elif e.response.status_code == 429:
                raise ValueError(
                    "Rate limit exceeded. Please try again later."
                ) from e
            else:
                raise ValueError(
                    f"API request failed: {e.response.status_code} - {e.response.text}"
                ) from e
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Network error: {str(e)}") from e
    
    def test_connection(self) -> bool:
        """Test if the API connection works.
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            # Try to fetch personal info to test the connection
            response = requests.get(
                "https://api.ouraring.com/v2/usercollection/personal_info",
                headers=self.headers
            )
            response.raise_for_status()
            return True
        except Exception:
            return False
    
    def get_sleep_data(self, start_date: str, end_date: str) -> List[Dict[str, Any]]:
        """Fetch sleep data for a date range.
        
        Args:
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            
        Returns:
            List of sleep sessions
        """
        params = {
            "start_date": start_date,
            "end_date": end_date
        }
        response = self._make_request("sleep", params)
        return response.get("data", [])
    
    def get_activity_data(self, start_date: str, end_date: str) -> List[Dict[str, Any]]:
        """Fetch activity data for a date range.
        
        Args:
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            
        Returns:
            List of daily activity data
        """
        params = {
            "start_date": start_date,
            "end_date": end_date
        }
        response = self._make_request("daily_activity", params)
        return response.get("data", [])
    
    def get_readiness_data(self, start_date: str, end_date: str) -> List[Dict[str, Any]]:
        """Fetch readiness data for a date range.
        
        Args:
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            
        Returns:
            List of daily readiness scores
        """
        params = {
            "start_date": start_date,
            "end_date": end_date
        }
        response = self._make_request("daily_readiness", params)
        return response.get("data", [])
    
    def get_heart_rate_data(self, start_date: str, end_date: str) -> List[Dict[str, Any]]:
        """Fetch heart rate data for a date range.
        
        Args:
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            
        Returns:
            List of heart rate data points
        """
        params = {
            "start_date": start_date,
            "end_date": end_date
        }
        response = self._make_request("heartrate", params)
        return response.get("data", [])