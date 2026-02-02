"""
MoMo Transaction API Server
This is our REST API for managing mobile money transactions.
We're using plain Python's http.server module (no Flask or Django).
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import sys
import os
from urllib.parse import urlparse, parse_qs

# Add parent directory to path to import other modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dsa.parser import parse_xml_to_json, create_transaction_dictionary
from api.auth import authenticate_request, get_auth_error_response


# Store transactions in memory (resets when server restarts)
# TODO: Maybe add database later?
transactions_list = []  # list of all transactions
transactions_dict = {}  # for faster lookup by ID
next_id = 1


def initialize_data():
    """Load transactions from the XML file"""
    global transactions_list, transactions_dict, next_id
    
    # figure out where the XML file is
    current_dir = os.path.dirname(os.path.abspath(__file__))
    xml_path = os.path.join(os.path.dirname(current_dir), 'data', 'modified_sms_v2.xml')
    
    # Parse XML data
    transactions_list = parse_xml_to_json(xml_path)
    transactions_dict = create_transaction_dictionary(transactions_list)
    
    # Set next_id to one more than the highest existing ID
    if transactions_list:
        next_id = max(t['id'] for t in transactions_list) + 1
    
    print(f"Initialized with {len(transactions_list)} transactions")


class TransactionAPIHandler(BaseHTTPRequestHandler):
    """
    HTTP Request Handler for Transaction API
    Implements CRUD operations with authentication
    """
    
    def _set_headers(self, status_code=200, content_type='application/json'):
        """Set HTTP response headers."""
        self.send_response(status_code)
        self.send_header('Content-Type', content_type)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
    
    def _authenticate(self):
        """
        Authenticate the request using Authorization header.
        Returns True if authenticated, False otherwise.
        """
        auth_header = self.headers.get('Authorization')
        return authenticate_request(auth_header)
    
    def _send_json_response(self, data, status_code=200):
        """Send JSON response."""
        self._set_headers(status_code)
        self.wfile.write(json.dumps(data, indent=2).encode('utf-8'))
    
    def _send_error_response(self, message, status_code=400):
        """Send error response."""
        error_data = {
            'error': True,
            'message': message,
            'status': status_code
        }
        self._send_json_response(error_data, status_code)
    
    def _get_request_body(self):
        """Read and parse JSON request body."""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            return json.loads(body.decode('utf-8'))
        except Exception as e:
            return None
    
    def _parse_path(self):
        """
        Parse the request path to extract endpoint and ID.
        Returns: (endpoint, transaction_id)
        """
        parsed = urlparse(self.path)
        path_parts = parsed.path.strip('/').split('/')
        
        endpoint = path_parts[0] if path_parts else ''
        transaction_id = None
        
        if len(path_parts) > 1 and path_parts[1].isdigit():
            transaction_id = int(path_parts[1])
        
        return endpoint, transaction_id
    
    # ============================================================
    # GET ENDPOINTS (Author: Chely Kelvin Sheja)
    # ============================================================
    
    def do_GET(self):
        """
        Handle GET requests.
        GET /transactions -> List all transactions
        GET /transactions/{id} -> Get specific transaction
        """
        # Check authentication
        if not self._authenticate():
            self._send_json_response(get_auth_error_response(), 401)
            return
        
        endpoint, transaction_id = self._parse_path()
        
        if endpoint != 'transactions':
            self._send_error_response('Invalid endpoint', 404)
            return
        
        # GET /transactions/{id} - Get single transaction
        if transaction_id is not None:
            if transaction_id in transactions_dict:
                self._send_json_response({
                    'success': True,
                    'data': transactions_dict[transaction_id]
                })
            else:
                self._send_error_response(f'Transaction with ID {transaction_id} not found', 404)
        
        # GET /transactions - List all transactions
        else:
            self._send_json_response({
                'success': True,
                'count': len(transactions_list),
                'data': transactions_list
            })
    
    # ============================================================
    # POST ENDPOINT (Author: Chely Kelvin Sheja)
    # ============================================================
    
    def do_POST(self):
        """
        Handle POST requests.
        POST /transactions -> Create new transaction
        """
        global next_id
        
        # Check authentication
        if not self._authenticate():
            self._send_json_response(get_auth_error_response(), 401)
            return
        
        endpoint, _ = self._parse_path()
        
        if endpoint != 'transactions':
            self._send_error_response('Invalid endpoint', 404)
            return
        
        # Parse request body
        new_transaction_data = self._get_request_body()
        
        if not new_transaction_data:
            self._send_error_response('Invalid JSON in request body', 400)
            return
        
        # Validate required fields
        required_fields = ['type', 'amount', 'sender', 'receiver']
        missing_fields = [field for field in required_fields if field not in new_transaction_data]
        
        if missing_fields:
            self._send_error_response(f'Missing required fields: {", ".join(missing_fields)}', 400)
            return
        
        # Create new transaction
        new_transaction = {
            'id': next_id,
            'type': new_transaction_data['type'],
            'amount': float(new_transaction_data['amount']),
            'sender': new_transaction_data['sender'],
            'receiver': new_transaction_data['receiver'],
            'timestamp': new_transaction_data.get('timestamp', ''),
            'status': new_transaction_data.get('status', 'pending')
        }
        
        # Add to storage
        transactions_list.append(new_transaction)
        transactions_dict[next_id] = new_transaction
        next_id += 1
        
        # Return created transaction
        self._send_json_response({
            'success': True,
            'message': 'Transaction created successfully',
            'data': new_transaction
        }, 201)
    
    # ============================================================
    # PUT ENDPOINT (Author: Darlene Ayinkamiye - Team Leader)
    # ============================================================
    
    def do_PUT(self):
        """
        Handle PUT requests.
        PUT /transactions/{id} -> Update existing transaction
        """
        # Check authentication
        if not self._authenticate():
            self._send_json_response(get_auth_error_response(), 401)
            return
        
        endpoint, transaction_id = self._parse_path()
        
        if endpoint != 'transactions':
            self._send_error_response('Invalid endpoint', 404)
            return
        
        if transaction_id is None:
            self._send_error_response('Transaction ID is required for PUT request', 400)
            return
        
        # Check if transaction exists
        if transaction_id not in transactions_dict:
            self._send_error_response(f'Transaction with ID {transaction_id} not found', 404)
            return
        
        # Parse request body
        update_data = self._get_request_body()
        
        if not update_data:
            self._send_error_response('Invalid JSON in request body', 400)
            return
        
        # Update transaction (preserve ID)
        existing_transaction = transactions_dict[transaction_id]
        
        # Update fields if provided
        if 'type' in update_data:
            existing_transaction['type'] = update_data['type']
        if 'amount' in update_data:
            existing_transaction['amount'] = float(update_data['amount'])
        if 'sender' in update_data:
            existing_transaction['sender'] = update_data['sender']
        if 'receiver' in update_data:
            existing_transaction['receiver'] = update_data['receiver']
        if 'timestamp' in update_data:
            existing_transaction['timestamp'] = update_data['timestamp']
        if 'status' in update_data:
            existing_transaction['status'] = update_data['status']
        
        # Update in list as well
        for i, trans in enumerate(transactions_list):
            if trans['id'] == transaction_id:
                transactions_list[i] = existing_transaction
                break
        
        # Return updated transaction
        self._send_json_response({
            'success': True,
            'message': f'Transaction {transaction_id} updated successfully',
            'data': existing_transaction
        })
    
    # ============================================================
    # DELETE ENDPOINT (Author: Darlene Ayinkamiye - Team Leader)
    # ============================================================
    
    def do_DELETE(self):
        """
        Handle DELETE requests.
        DELETE /transactions/{id} -> Delete transaction
        """
        # Check authentication
        if not self._authenticate():
            self._send_json_response(get_auth_error_response(), 401)
            return
        
        endpoint, transaction_id = self._parse_path()
        
        if endpoint != 'transactions':
            self._send_error_response('Invalid endpoint', 404)
            return
        
        if transaction_id is None:
            self._send_error_response('Transaction ID is required for DELETE request', 400)
            return
        
        # Check if transaction exists
        if transaction_id not in transactions_dict:
            self._send_error_response(f'Transaction with ID {transaction_id} not found', 404)
            return
        
        # Get transaction before deleting (for response)
        deleted_transaction = transactions_dict[transaction_id]
        
        # Delete from dictionary
        del transactions_dict[transaction_id]
        
        # Delete from list
        transactions_list[:] = [t for t in transactions_list if t['id'] != transaction_id]
        
        # Return success response
        self._send_json_response({
            'success': True,
            'message': f'Transaction {transaction_id} deleted successfully',
            'data': deleted_transaction
        })
    
    # ============================================================
    # OPTIONS (for CORS preflight)
    # ============================================================
    
    def do_OPTIONS(self):
        """Handle OPTIONS requests for CORS."""
        self._set_headers(204)
    
    # Suppress default logging
    def log_message(self, format, *args):
        """Custom logging."""
        print(f"{self.address_string()} - [{self.log_date_time_string()}] {format % args}")


def run_server(host='localhost', port=8000):
    """
    Start the HTTP server.
    
    Args:
        host (str): Server host address
        port (int): Server port number
    """
    # Initialize data
    initialize_data()
    
    # Create server
    server_address = (host, port)
    httpd = HTTPServer(server_address, TransactionAPIHandler)
    
    print("=" * 60)
    print("MoMo Transaction REST API Server")
    print("=" * 60)
    print(f"Server running on http://{host}:{port}")
    print("\nEndpoints:")
    print(f"  GET    http://{host}:{port}/transactions")
    print(f"  GET    http://{host}:{port}/transactions/{{id}}")
    print(f"  POST   http://{host}:{port}/transactions")
    print(f"  PUT    http://{host}:{port}/transactions/{{id}}")
    print(f"  DELETE http://{host}:{port}/transactions/{{id}}")
    print("\nAuthentication: Basic Auth (username: admin, password: password)")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 60)
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\nShutting down server...")
        httpd.shutdown()
        print("Server stopped.")


if __name__ == "__main__":
    run_server()