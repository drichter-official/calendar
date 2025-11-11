# Deployment Notes

## Puzzle Generation on Digital Ocean

### Issue
When deploying to Digital Ocean, the "Generate New Puzzle" button may fail with an error:
```
✗ Error: Unexpected token '<', " <"... is not valid JSON
```

### Cause
This error occurs when the Flask server returns an HTML error page instead of JSON. Common causes:

1. **File Permissions**: The web server may not have write permissions to the `custom_sudoku_generator/sudoku_*_rule/` folders
2. **Path Issues**: The relative paths may be different in the production environment
3. **Module Import Errors**: The Python generator module may not be properly accessible

### Solution
The updated code now includes:

1. **Permission Checks**: Tests write access before attempting generation
2. **Better Error Handling**: Returns proper JSON errors instead of HTML error pages
3. **Detailed Error Messages**: Provides specific information about what went wrong
4. **Global Error Handler**: Ensures all exceptions on `/generate/` routes return JSON

### Changes Made

#### app.py
- Added error handler to ensure JSON responses on generate routes
- Added permission checks before attempting to generate puzzles
- Added detailed error logging and messages
- Added import error handling

#### door1.html
- Improved JavaScript error handling to show detailed error messages
- Added check for JSON content type in response
- Added console logging for debugging

### Setting File Permissions on Digital Ocean

If you get a "No write permission" error, SSH into your Digital Ocean droplet and run:

```bash
# Navigate to your app directory
cd /path/to/advent_calendar

# Give write permissions to the sudoku rule folders
chmod -R 755 custom_sudoku_generator/

# If using gunicorn with a specific user, change ownership:
chown -R $USER:$USER custom_sudoku_generator/

# Or if using nginx with www-data user:
chown -R www-data:www-data custom_sudoku_generator/

# Verify permissions
ls -la custom_sudoku_generator/sudoku_knights_rule/
```

### Troubleshooting on Digital Ocean

#### 1. Check Application Logs
```bash
# If using gunicorn
journalctl -u your-app-name -n 50

# Or check error logs
tail -f /var/log/your-app-name/error.log
```

#### 2. Test the Endpoint Directly
```bash
# SSH into your droplet and run:
curl -i http://localhost:8000/generate/1

# Should return JSON like:
# {"success": true, "message": "New puzzle generated successfully!"}
# 
# Or:
# {"success": false, "message": "No write permission in rule folder..."}
```

#### 3. Check Python Environment
```bash
# Ensure all dependencies are installed
cd /path/to/advent_calendar
source venv/bin/activate  # or wherever your virtualenv is
pip install -r requirements.txt

# Test import manually
python -c "from custom_sudoku_generator.run import generate_sudoku_for_rule; print('OK')"
```

#### 4. Verify File Structure
```bash
# Ensure the generator folder is deployed correctly
ls -R custom_sudoku_generator/ | grep -E "rule.py|sudoku.txt|solution.txt"
```

### Alternative: Read-Only Deployment

If you prefer not to allow file writes in production, you can:

1. Pre-generate multiple puzzles locally
2. Store them in a database
3. Modify the generate endpoint to cycle through pre-generated puzzles instead of creating new ones

Example modification:
```python
# Store multiple puzzle versions
PUZZLE_VERSIONS = {
    1: ['v1', 'v2', 'v3'],  # Door 1 has 3 pre-generated versions
}

@app.route('/generate/<int:door_number>')
def generate_puzzle(door_number):
    # Cycle through pre-generated puzzles instead
    versions = PUZZLE_VERSIONS.get(door_number, [])
    # Pick a random version
    # Load from database or different files
    pass
```

### Testing Generation Locally

Test the generation endpoint locally:

```bash
# Method 1: Using the test script
cd /path/to/advent_calendar
python test_generate.py

# Method 2: Using curl with local server
# In one terminal, start the server
cd website
python app.py

# In another terminal, test the endpoint
curl http://localhost:5000/generate/1
```

You should get a JSON response like:
```json
{"success": true, "message": "New puzzle generated successfully!"}
```

Or an error like:
```json
{"success": false, "message": "No write permission in rule folder. Please check file permissions on the server."}
```

### Deployment Checklist

- [ ] Deploy updated `app.py` with error handling
- [ ] Deploy updated `door1.html` with improved error handling
- [ ] Set proper file permissions on sudoku rule folders
- [ ] Test the generate endpoint with curl
- [ ] Check application logs for any errors
- [ ] Verify puzzles are being saved correctly
- [ ] Test the frontend button in the browser

### Need Help?

If you continue to have issues:
1. Check the browser console (F12) for JavaScript errors
2. Check the Flask application logs for Python errors
3. Verify the exact error message returned by the endpoint
4. Ensure the file paths are correct for your deployment environment

