# Oura mcp Server

An mcp server that enables Claude desktop to access and analyze your Oura Ring data.

## Background

I tried looking for existing Oura libraries to analyze my data but couldn't find any good options, so I decided to create this MCP server to bridge that gap.

## Features

- Access sleep data and trends
- View activity metrics
- Check readiness scores
- Custom date range queries
- Connection status checking

## Prerequisites

- Python 3.10 or higher
- An Oura Ring and active Oura account
- Oura API Personal Access Token
- Claude Desktop

## Quick Setup

1. Clone this repository:
```bash
git clone https://github.com/yourusername/oura-mcp-server.git
cd oura-mcp-server
```

2. Get your Oura API token:
   - Log in to [Oura Cloud](https://cloud.ouraring.com)
   - Go to Account > Personal Access Tokens
   - Click "Create New Personal Access Token"
   - Copy the token

3. Add your token to the `.env` file:
```bash
echo "OURA_API_TOKEN=your_actual_token_here" > .env
```

4. Run the automated setup:
```bash
python setup.py
```

5. Restart Claude Desktop

That's it! The setup script will automatically:
- Install all dependencies
- Test your Oura API connection
- Configure Claude Desktop
- Verify everything is working

## Manual Setup (if needed)

If the automated setup doesn't work, you can configure manually:

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Configure Claude Desktop

The server script is located at: `/path/to/oura-mcp-server/server.py`

#### macOS
Edit `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "oura": {
      "command": "python",
      "args": ["/full/path/to/oura-mcp-server/server.py"]
    }
  }
}
```

#### Windows
Edit `%APPDATA%\Claude\claude_desktop_config.json` with the same configuration.

## Usage

Once configured, you can ask Claude to analyze and plot your data.

- "How did I sleep last night?"
- "Show me my sleep data for the past week"
- "Analyze my sleep patterns this month"
- "Compare my activity levels between last week and this week"


Claude Desktop is great for running basic analysis and getting quick insights from your Oura data. However, for more advanced statistical analysis, machine learning, or complex data science tasks, I recommend exporting your data as a CSV and using [julius.ai](https://julius.ai) to analyze it. Julius.ai provides powerful data analysis capabilities that can handle more sophisticated analytical workflows.

## Privacy & Security

- Your Oura API token is stored locally in your `.env` file
- No health data is cached or stored by this server
- All data is fetched fresh from Oura's API for each request
- The server only logs errors, never personal health information

## Contributing

Contributions are welcome and appreciated.

## License

MIT License - see LICENSE file for details