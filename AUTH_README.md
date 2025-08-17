# Authentication System

This loan approval backend now includes a complete authentication system with JWT tokens.

## Available Endpoints

### POST /register
Register a new user with username and password.

**Request Body:**
```json
{
    "username": "your_username",
    "password": "your_password"
}
```

**Response:**
```json
{
    "message": "User registered successfully",
    "user_id": 1,
    "username": "your_username"
}
```

### POST /login
Login with username and password to receive a JWT token.

**Request Body:**
```json
{
    "username": "your_username",
    "password": "your_password"
}
```

**Response:**
```json
{
    "message": "Login successful",
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "user_id": 1,
    "username": "your_username"
}
```

### POST /logout
Logout and clear authentication cookies.

**Response:**
```json
{
    "message": "Logged out successfully"
}
```

### GET /protected
Example protected route that requires authentication.

**Headers:**
```
Authorization: Bearer your_jwt_token_here
```

**Response:**
```json
{
    "message": "This is protected data",
    "user_id": 1,
    "username": "your_username",
    "data": "Only authenticated users can see this"
}
```

## Using Authentication in Your Routes

To protect any route with authentication, use the `@token_required` decorator:

```python
from routes.auth_middleware import token_required

@token_required
def my_protected_function(current_user_id, current_username):
    # Your protected code here
    return jsonify({'message': f'Hello {current_username}!'})
```

## Authentication Methods

The system supports two ways to send the JWT token:

1. **Authorization Header (recommended):**
   ```
   Authorization: Bearer your_jwt_token_here
   ```

2. **Cookie (for web browsers):**
   The token is automatically stored in `jwt_token` cookie when using form-based login.

## Security Notes

- JWT tokens expire after 1 hour
- Passwords are hashed using Werkzeug's security functions
- Make sure to change the SECRET_KEY in production
- The current SECRET_KEY is: `your-secret-key-change-this-in-production`
