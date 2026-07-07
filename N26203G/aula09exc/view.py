import json

def render_json(handler, status_code, data):
    """
    Renders a JSON response, setting all appropriate CORS
    and Content-Type headers, and writing the serialized JSON data.
    """
    # Convert data to JSON string encoded in UTF-8
    response_body = json.dumps(data, ensure_ascii=False).encode('utf-8')
    
    handler.send_response(status_code)
    handler.send_header('Content-Type', 'application/json; charset=utf-8')
    handler.send_header('Access-Control-Allow-Origin', '*')
    handler.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
    handler.send_header('Access-Control-Allow-Headers', 'Content-Type')
    handler.send_header('Content-Length', str(len(response_body)))
    handler.end_headers()
    
    handler.wfile.write(response_body)

def render_cors_preflight(handler):
    """
    Handles CORS preflight (OPTIONS) requests, returning 204 No Content
    with permissions for cross-origin POST and GET requests.
    """
    handler.send_response(204)
    handler.send_header('Access-Control-Allow-Origin', '*')
    handler.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
    handler.send_header('Access-Control-Allow-Headers', 'Content-Type')
    handler.end_headers()

def render_error(handler, status_code, message):
    """
    Convenience method for formatting and rendering error responses.
    """
    render_json(handler, status_code, {"error": message})
