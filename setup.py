#!/usr/bin/env python3
"""Setup script for Oura MCP Server."""

import os
import sys
import subprocess
import shutil
import json
from pathlib import Path

def install_dependencies():
    """Install required dependencies."""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False
    return True

def check_oura_token():
    """Check if Oura API token is configured."""
    from dotenv import load_dotenv
    load_dotenv()
    
    token = os.getenv("OURA_API_TOKEN")
    if not token:
        print("❌ OURA_API_TOKEN not found in .env file")
        print("   Please add your Oura API token to the .env file:")
        print("   OURA_API_TOKEN=your_token_here")
        return False
    
    print("✅ Oura API token found")
    return True

def test_oura_connection():
    """Test Oura API connection."""
    print("🔍 Testing Oura API connection...")
    
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
    
    try:
        from oura_mcp.oura_client import OuraClient
        client = OuraClient()
        
        if client.test_connection():
            print("✅ Oura API connection successful")
            return True
        else:
            print("❌ Oura API connection failed")
            return False
    except Exception as e:
        print(f"❌ Error testing connection: {e}")
        return False

def get_claude_config_path():
    """Get Claude Desktop config path based on OS."""
    home = Path.home()
    
    if sys.platform == "darwin":  # macOS
        return home / "Library" / "Application Support" / "Claude" / "claude_desktop_config.json"
    elif sys.platform == "win32":  # Windows
        return home / "AppData" / "Roaming" / "Claude" / "claude_desktop_config.json"
    else:  # Linux
        return home / ".config" / "Claude" / "claude_desktop_config.json"

def update_claude_config():
    """Update Claude Desktop configuration."""
    config_path = get_claude_config_path()
    server_path = os.path.abspath("server.py")
    
    # Find the correct python path (prefer venv if available)
    python_cmd = sys.executable
    if not python_cmd or python_cmd == sys.executable:
        # Try common locations
        for cmd in ["python3", "python"]:
            try:
                result = subprocess.run(["which", cmd], capture_output=True, text=True)
                if result.returncode == 0:
                    python_cmd = result.stdout.strip()
                    break
            except:
                continue
    
    print(f"📝 Claude config location: {config_path}")
    print(f"📝 Server script: {server_path}")
    print(f"📝 Python command: {python_cmd}")
    
    # Create the config directory if it doesn't exist
    config_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Load existing config or create new one
    if config_path.exists():
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
        except json.JSONDecodeError:
            config = {}
    else:
        config = {}
    
    # Ensure mcpServers exists
    if "mcpServers" not in config:
        config["mcpServers"] = {}
    
    # Add our server with full python path
    config["mcpServers"]["oura"] = {
        "command": python_cmd,
        "args": [server_path]
    }
    
    # Write the updated config
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    print("✅ Claude Desktop configuration updated")
    print(f"   Added 'oura' server pointing to: {server_path}")
    print(f"   Using python: {python_cmd}")
    print("\n🔄 Please restart Claude Desktop to load the new server")

def main():
    """Main setup function."""
    print("🚀 Setting up Oura MCP Server")
    print("=" * 40)
    
    # Install dependencies
    if not install_dependencies():
        return
    
    # Check Oura token
    if not check_oura_token():
        return
    
    # Test connection
    if not test_oura_connection():
        return
    
    # Update Claude config
    try:
        update_claude_config()
    except Exception as e:
        print(f"⚠️  Could not automatically update Claude config: {e}")
        print("\nManual setup required:")
        print("Add this to your Claude Desktop config:")
        print(f"""
{{
  "mcpServers": {{
    "oura": {{
      "command": "python",
      "args": ["{os.path.abspath('server.py')}"]
    }}
  }}
}}
""")
    
    print("\n🎉 Setup complete!")
    print("   Restart Claude Desktop and you should see Oura tools available")

if __name__ == "__main__":
    main() 