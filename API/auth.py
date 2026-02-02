"""
Authentication Module
Handles Basic Auth for the API.
"""

import base64
from typing import Optional, Tuple


# Valid usernames and passwords
# NOTE: In real app, these should be in a database with hashed passwords!
VALID_CREDENTIALS = {
    'admin': 'password',
    'user1': 'test123',
    'developer': 'devpass'
}


def parse_basic_auth_header(auth_header: str) -> Optional[Tuple[str, str]]:
    """
    Parse Basic Authentication header and extract username and password.
    
    Args:
        auth_header (str): The Authorization header value
        
    Returns:
        tuple: (username, password) if valid, None otherwise
    """
    try:
        # Check if header starts with 'Basic '
        if not auth_header.startswith('Basic '):
            return None
        
        # Extract the base64 encoded credentials
        encoded_credentials = auth_header[6:]  # Remove 'Basic ' prefix
        
        # Decode from base64
        decoded_bytes = base64.b64decode(encoded_credentials)
        decoded_str = decoded_bytes.decode('utf-8')
        
        # Split username and password
        if ':' not in decoded_str:
            return None
        
        username, password = decoded_str.split(':', 1)
        return (username, password)
    
    except Exception:
        return None


def validate_credentials(username: str, password: str) -> bool:
    """
    Validate username and password against stored credentials.
    
    Args:
        username (str): Username to validate
        password (str): Password to validate
        
    Returns:
        bool: True if credentials are valid, False otherwise
    """
    return VALID_CREDENTIALS.get(username) == password


def authenticate_request(auth_header: Optional[str]) -> bool:
    """
    Authenticate a request using Basic Authentication.
    
    Args:
        auth_header (str): The Authorization header value
        
    Returns:
        bool: True if authenticated, False otherwise
    """
    if not auth_header:
        return False
    
    credentials = parse_basic_auth_header(auth_header)
    if not credentials:
        return False
    
    username, password = credentials
    return validate_credentials(username, password)


def get_auth_error_response() -> dict:
    """
    Get a standardized authentication error response.
    
    Returns:
        dict: Error response dictionary
    """
    return {
        'error': 'Unauthorized',
        'message': 'Invalid or missing authentication credentials',
        'status': 401
    }


# Security Analysis and Recommendations
SECURITY_ANALYSIS = """
===========================================
BASIC AUTHENTICATION - SECURITY ANALYSIS
===========================================

Author: Solomon Leek

WEAKNESSES OF BASIC AUTHENTICATION:

1. **Credentials Transmitted in Base64 (Not Encrypted)**
   - Base64 is encoding, NOT encryption
   - Anyone intercepting the request can easily decode credentials
   - Example: 'YWRtaW46cGFzc3dvcmQ=' decodes to 'admin:password'

2. **Credentials Sent with Every Request**
   - Increases exposure window for credential theft
   - More opportunities for interception

3. **No Built-in Protection Against Replay Attacks**
   - Captured credentials can be reused by attackers
   - No session expiration or token invalidation

4. **Vulnerable to Man-in-the-Middle (MITM) Attacks**
   - Without HTTPS, credentials are sent in plain text
   - Even with HTTPS, basic auth is still considered weak

5. **No Logout Mechanism**
   - Browsers cache credentials
   - Difficult to "log out" a user properly

6. **Password Storage Issues**
   - Often leads to storing passwords in plain text
   - No password hashing or salting in basic implementations

RECOMMENDED ALTERNATIVES:

1. **JWT (JSON Web Tokens)**
   - Stateless authentication
   - Includes expiration times
   - Can carry user metadata
   - Implementation:
     * User logs in with credentials
     * Server generates signed JWT token
     * Client includes token in header: Authorization: Bearer <token>
     * Server validates token signature and expiration

2. **OAuth 2.0**
   - Industry-standard authorization framework
   - Supports multiple grant types
   - Separates authentication from authorization
   - Ideal for third-party integrations
   - Used by: Google, Facebook, GitHub

3. **API Keys with HMAC Signatures**
   - Each client gets unique API key and secret
   - Requests are signed with HMAC
   - Prevents tampering and replay attacks

4. **Session-Based Authentication with Cookies**
   - Server maintains session state
   - Secure, HTTP-only cookies
   - CSRF protection required

BEST PRACTICES FOR ANY AUTH SYSTEM:

1. Always use HTTPS/TLS
2. Implement rate limiting to prevent brute force
3. Use strong password policies
4. Implement account lockout after failed attempts
5. Hash passwords with bcrypt or Argon2
6. Use multi-factor authentication (MFA)
7. Implement proper session management
8. Log authentication attempts for security monitoring

CONCLUSION:
Basic Authentication is acceptable ONLY for:
- Internal tools on secure networks
- Educational/demonstration purposes
- Quick prototypes or development environments

For production APIs, especially those handling financial data like MoMo transactions,
JWT or OAuth 2.0 should be used with HTTPS enforcement.
"""


if __name__ == "__main__":
    print(SECURITY_ANALYSIS)
    
    # Test the authentication functions
    print("\n" + "=" * 60)
    print("AUTHENTICATION TESTING")
    print("=" * 60)
    
    # Test 1: Valid credentials
    test_header_valid = "Basic " + base64.b64encode(b"admin:password").decode('utf-8')
    print(f"\nTest 1 - Valid credentials: {authenticate_request(test_header_valid)}")
    
    # Test 2: Invalid credentials
    test_header_invalid = "Basic " + base64.b64encode(b"admin:wrongpass").decode('utf-8')
    print(f"Test 2 - Invalid password: {authenticate_request(test_header_invalid)}")
    
    # Test 3: No header
    print(f"Test 3 - No header: {authenticate_request(None)}")
    
    # Test 4: Malformed header
    print(f"Test 4 - Malformed header: {authenticate_request('Bearer token123')}")