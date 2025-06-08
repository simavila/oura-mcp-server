# troubleshooting guide

## common issues and solutions

### 1. "oura tools not showing up in claude desktop"

**solution:**
1. make sure you've restarted claude desktop after configuration
2. check that the server path in your config is correct
3. verify the server starts without errors:
   ```bash
   python server.py
   ```
4. check claude desktop logs (if available)

### 2. "spawn python ENOENT" or "modulenotfounderror: no module named 'mcp'"

**solution:**
claude desktop can't find python or your dependencies. update your claude config to use the full python path:

```json
{
  "mcpServers": {
    "oura": {
      "command": "/full/path/to/your/venv/bin/python3",
      "args": ["/full/path/to/your/server.py"]
    }
  }
}
```

to find your python path:
```bash
which python3  # or: echo $VIRTUAL_ENV/bin/python3
```

### 3. "authentication failed" or "api token error"

**solution:**
1. verify your token is correct in the `.env` file
2. test the connection:
   ```bash
   python -c "
   import sys, os
   sys.path.insert(0, 'src')
   from oura_mcp.oura_client import OuraClient
   client = OuraClient()
   print('✅ connection works!' if client.test_connection() else '❌ connection failed')
   "
   ```
3. make sure your oura account has api access enabled
4. check if your token has expired

### 4. "module not found" errors

**solution:**
1. make sure you're running from the project root directory
2. check that all dependencies are installed:
   ```bash
   pip install -r requirements.txt
   ```
3. verify python path is correct

### 5. "no data returned" from oura api

**solution:**
1. check that you have data for the requested date range
2. verify your oura ring has been syncing properly
3. try a different date range
4. check oura's api status

### 6. server starts but claude can't connect

**solution:**
1. check that the server path in claude config is absolute (full path)
2. make sure python is in your system path
3. try running the server manually first to check for errors
4. verify the claude desktop config json is valid

## testing your setup

run this command to test everything:
```bash
python setup.py
```

this will check:
- ✅ dependencies installed
- ✅ oura token configured
- ✅ api connection working
- ✅ claude desktop configured

## getting help

if you're still having issues:

1. **check the error logs** - paste them into `error_logs.txt` and share
2. **run the test script** - `python setup.py` and share the output
3. **verify your environment** - python version, os, etc.
4. **check oura api status** - visit oura's developer documentation

## manual testing

you can test individual components:

### test oura api directly:
```bash
curl -h "authorization: bearer your_token_here" \
     "https://api.ouraring.com/v2/usercollection/personal_info"
```

### test the mcp server:
```bash
python server.py
# should start without errors and wait for input
```

### test claude desktop config:
check that your config file exists and is valid json:
- macos: `~/library/application support/claude/claude_desktop_config.json`
- windows: `%appdata%\claude\claude_desktop_config.json` 