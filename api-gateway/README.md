# Audit Manager API Gateway

Node.js API Gateway using Express that handles authentication and proxies requests to the Application Service.

## Features

- JWT-based authentication
- Three user roles: DEV, APPROVER, DEVOPS
- Fake authentication endpoints for testing
- Proxy middleware to Application Service
- Automatic injection of user role and email headers

## Setup

1. Install dependencies:
```bash
npm install
```

2. Start the server:
```bash
npm start
```

The gateway will run on port 3000 (or the PORT specified in .env).

## Authentication Endpoints

### Login as DEV
```bash
POST /api/v1/auth/login/dev
```

Response:
```json
{
  "data": {
    "type": "auth",
    "attributes": {
      "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
      "user": {
        "id": 1,
        "name": "John Developer",
        "email": "john.dev@example.com",
        "role": "DEV"
      }
    }
  }
}
```

### Login as APPROVER
```bash
POST /api/v1/auth/login/approver
```

### Login as DEVOPS
```bash
POST /api/v1/auth/login/devops
```

## Using the API

1. Get a token from one of the authentication endpoints
2. Include the token in the Authorization header:
```bash
Authorization: Bearer <token>
```

3. Make requests to the proxied endpoints:

```bash
# Create application (DEV only)
POST /api/v1/audit/applications
Authorization: Bearer <dev-token>
Content-Type: application/json

{
  "name": "My Application",
  "owner_team": "Platform Team",
  "repo_url": "https://github.com/org/repo"
}

# List applications (DEV, APPROVER, DEVOPS)
GET /api/v1/audit/applications
Authorization: Bearer <token>

# Get application by ID (DEV, APPROVER, DEVOPS)
GET /api/v1/audit/applications/{id}
Authorization: Bearer <token>

# Create release (DEV only)
POST /api/v1/audit/releases
Authorization: Bearer <dev-token>
Content-Type: application/json

{
  "application_id": 1,
  "version": "v1.0.0"
}

# Note: The 'env' field is optional and defaults to "DEV" if not provided.
# You can optionally specify: "env": "DEV" | "PREPROD" | "PROD"

# List releases (DEV, APPROVER, DEVOPS)
GET /api/v1/audit/releases
Authorization: Bearer <token>

Response:
{
  "data": [
    {
      "release_id": 1,
      "application_id": 1,
      "application_name": "My Application",
      "version": "v1.0.0",
      "env": "DEV",
      "status": "PENDING_PREPROD",
      "evidence_url": "https://evidence.example.com/releases/...",
      "logs": "[timestamp] validation logs...",
      "created_at": "2025-10-20T...",
      "deployed_at": null
    }
  ]
}

# Approve release (APPROVER only)
POST /api/v1/audit/releases/{id}/approve
Authorization: Bearer <approver-token>
Content-Type: application/json

{
  "notes": "Approved for deployment"
}

# Promote release (DEVOPS only)
POST /api/v1/audit/releases/{id}/promote
Authorization: Bearer <devops-token>
```

## How it Works

1. Client sends request with JWT token in Authorization header
2. Auth middleware validates the token and extracts user info
3. Middleware injects X-User-Role and X-User-Email headers
4. Request is proxied to the Application Service
5. Application Service validates role permissions and processes the request

## Environment Variables

- `PORT`: Gateway port (default: 3000)
- `JWT_SECRET`: Secret key for signing JWT tokens
- `JWT_EXPIRES_IN`: Token expiration time (default: 24h)
- `APPLICATION_SERVICE_URL`: URL of the Application Service (default: http://localhost:5000)
