#!/usr/bin/env python3
"""MCP server for Oura Ring data access - Version 3 with proper initialization."""

import asyncio
import os
import sys
from typing import Any, Dict, List

# Add the src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
import mcp.server.stdio

from oura_mcp.oura_client import OuraClient

server = Server("oura-mcp-server")

# Global client instance
oura_client = None

def get_client():
    """Get or create the Oura client."""
    global oura_client
    if oura_client is None:
        oura_client = OuraClient()
    return oura_client

def format_sleep_summary(sleep_data: List[Dict[str, Any]]) -> str:
    """Format sleep data into a readable summary."""
    if not sleep_data:
        return "No sleep data found for the specified date range."
    
    summaries = []
    for session in sleep_data:
        day = session.get('day', 'Unknown date')
        total_sleep = session.get('total_sleep_duration', 0) / 3600
        rem_sleep = session.get('rem_sleep_duration', 0) / 3600
        deep_sleep = session.get('deep_sleep_duration', 0) / 3600
        light_sleep = session.get('light_sleep_duration', 0) / 3600
        efficiency = session.get('sleep_efficiency', 0)
        
        summary = f"""
Date: {day}
Total Sleep: {total_sleep:.1f} hours
Sleep Efficiency: {efficiency}%
Sleep Stages:
  - REM: {rem_sleep:.1f} hours
  - Deep: {deep_sleep:.1f} hours
  - Light: {light_sleep:.1f} hours
"""
        summaries.append(summary)
    
    return "\n---\n".join(summaries)

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List available tools."""
    return [
        types.Tool(
            name="get_oura_status",
            description="Check if Oura token is configured and test connection",
            inputSchema={
                "type": "object",
                "properties": {},
                "additionalProperties": False
            },
        ),
        types.Tool(
            name="get_sleep_data",
            description="Get sleep data from Oura for a date range",
            inputSchema={
                "type": "object",
                "properties": {
                    "start_date": {
                        "type": "string",
                        "description": "Start date in YYYY-MM-DD format"
                    },
                    "end_date": {
                        "type": "string",
                        "description": "End date in YYYY-MM-DD format"
                    }
                },
                "required": ["start_date", "end_date"],
                "additionalProperties": False
            },
        ),
        types.Tool(
            name="get_activity_data",
            description="Get daily activity data from Oura",
            inputSchema={
                "type": "object",
                "properties": {
                    "start_date": {
                        "type": "string",
                        "description": "Start date in YYYY-MM-DD format"
                    },
                    "end_date": {
                        "type": "string",
                        "description": "End date in YYYY-MM-DD format"
                    }
                },
                "required": ["start_date", "end_date"],
                "additionalProperties": False
            },
        ),
        types.Tool(
            name="get_readiness_data",
            description="Get readiness scores from Oura",
            inputSchema={
                "type": "object",
                "properties": {
                    "start_date": {
                        "type": "string",
                        "description": "Start date in YYYY-MM-DD format"
                    },
                    "end_date": {
                        "type": "string",
                        "description": "End date in YYYY-MM-DD format"
                    }
                },
                "required": ["start_date", "end_date"],
                "additionalProperties": False
            },
        ),
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict | None) -> list[types.TextContent]:
    """Handle tool calls."""
    if arguments is None:
        arguments = {}

    try:
        client = get_client()
        
        if name == "get_oura_status":
            if client.test_connection():
                return [
                    types.TextContent(
                        type="text",
                        text="✅ Oura connection successful! Your API token is configured correctly."
                    )
                ]
            else:
                return [
                    types.TextContent(
                        type="text",
                        text="❌ Could not connect to Oura. Please check your API token in the .env file."
                    )
                ]
        
        elif name == "get_sleep_data":
            start_date = arguments.get("start_date")
            end_date = arguments.get("end_date")
            
            if not start_date or not end_date:
                return [
                    types.TextContent(
                        type="text",
                        text="❌ Please provide both start_date and end_date in YYYY-MM-DD format."
                    )
                ]
            
            sleep_data = client.get_sleep_data(start_date, end_date)
            summary = format_sleep_summary(sleep_data)
            
            return [
                types.TextContent(
                    type="text",
                    text=f"Sleep data from {start_date} to {end_date}:\n\n{summary}"
                )
            ]
        
        elif name == "get_activity_data":
            start_date = arguments.get("start_date")
            end_date = arguments.get("end_date")
            
            if not start_date or not end_date:
                return [
                    types.TextContent(
                        type="text",
                        text="❌ Please provide both start_date and end_date in YYYY-MM-DD format."
                    )
                ]
            
            activity_data = client.get_activity_data(start_date, end_date)
            
            if not activity_data:
                return [
                    types.TextContent(
                        type="text",
                        text=f"No activity data found from {start_date} to {end_date}."
                    )
                ]
            
            summaries = []
            for day_data in activity_data:
                day = day_data.get('day', 'Unknown')
                steps = day_data.get('steps', 0)
                active_calories = day_data.get('active_calories', 0)
                total_calories = day_data.get('total_calories', 0)
                
                summary = f"Date: {day}\nSteps: {steps:,}\nActive Calories: {active_calories}\nTotal Calories: {total_calories}"
                summaries.append(summary)
            
            return [
                types.TextContent(
                    type="text",
                    text=f"Activity data from {start_date} to {end_date}:\n\n" + "\n\n---\n\n".join(summaries)
                )
            ]
        
        elif name == "get_readiness_data":
            start_date = arguments.get("start_date")
            end_date = arguments.get("end_date")
            
            if not start_date or not end_date:
                return [
                    types.TextContent(
                        type="text",
                        text="❌ Please provide both start_date and end_date in YYYY-MM-DD format."
                    )
                ]
            
            readiness_data = client.get_readiness_data(start_date, end_date)
            
            if not readiness_data:
                return [
                    types.TextContent(
                        type="text",
                        text=f"No readiness data found from {start_date} to {end_date}."
                    )
                ]
            
            summaries = []
            for day_data in readiness_data:
                day = day_data.get('day', 'Unknown')
                score = day_data.get('score', 0)
                temperature_deviation = day_data.get('temperature_deviation', 0)
                
                summary = f"Date: {day}\nReadiness Score: {score}/100\nTemperature Deviation: {temperature_deviation:.2f}°C"
                summaries.append(summary)
            
            return [
                types.TextContent(
                    type="text",
                    text=f"Readiness data from {start_date} to {end_date}:\n\n" + "\n\n---\n\n".join(summaries)
                )
            ]
        
        else:
            return [
                types.TextContent(
                    type="text",
                    text=f"Unknown tool: {name}"
                )
            ]
            
    except Exception as e:
        return [
            types.TextContent(
                type="text",
                text=f"Error: {str(e)}"
            )
        ]

async def main():
    # Run the server using stdin/stdout streams
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="oura-mcp-server",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main()) 