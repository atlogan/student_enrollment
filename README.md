# Student Enrollment System

A Django-based student enrollment system with user authentication, permissions, and social login capabilities.

## Features

- User Authentication (Local and Google OAuth)
- Role-based Access Control
- CRUD Operations with Permission Checks
- Secure Environment Variable Management
- PostgreSQL Database Support

## Prerequisites

- Python 3.10 or higher
- PostgreSQL
- Google Cloud Platform Account (for OAuth)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/atlogan/student_enrollment
cd student_enrollment
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root with the following variables:
```env
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=postgres://user:password@localhost:5432/dbname
ACCOUNT_EMAIL_REQUIRED=True
ACCOUNT_USERNAME_REQUIRED=False
ACCOUNT_AUTHENTICATION_METHOD='email'
ACCOUNT_EMAIL_VERIFICATION='optional'
LOGIN_REDIRECT_URL='/'
ACCOUNT_LOGOUT_REDIRECT_URL='/'
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
```

## Google OAuth Setup

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Navigate to "APIs & Services" > "Credentials"
4. Click "Create Credentials" > "OAuth client ID"
5. Configure the OAuth consent screen:
   - Select "External" user type
   - Fill in required fields (App name, User support email, Developer contact)
   - Add scopes: `.../auth/userinfo.email` and `.../auth/userinfo.profile`
   - Add your email as a test user
6. Create OAuth client ID:
   - Application type: Web application
   - Name: "Django Student Enrollment"
   - Authorized redirect URI: `http://127.0.0.1:8000/accounts/google/login/callback/` (and/or http://localhost:8000/accounts/google/login/callback/)
7. Copy the Client ID and Client Secret to your `.env` file

## Database Setup

1. Create a PostgreSQL database
2. Update the `DATABASE_URL` in your `.env` file
3. Run migrations:
```bash
python manage.py migrate
```

## Running the Application

1. Start the development server:
```bash
python manage.py runserver
```

2. Visit `http://127.0.0.1:8000` in your browser

## Testing Authentication

### Local Authentication
1. Create a superuser:
```bash
python manage.py createsuperuser
```
2. Visit `http://127.0.0.1:8000/accounts/login/`
3. Log in with your superuser credentials

### Google Authentication
1. Visit `http://127.0.0.1:8000/accounts/login/`
2. Click "Login with Google"
3. Select your Google account
4. Authorize the application

## Testing Permissions

1. Create a regular user account
2. Log in as the regular user
3. Try to:
   - Create new records (should work)
   - Edit your own records (should work)
   - Edit others' records (should be denied)
   - Delete your own records (should work)
   - Delete others' records (should be denied)

## API Endpoints (Django REST Framework)

The application now includes RESTful API endpoints built with Django REST Framework (DRF). These endpoints provide programmatic access to the system's data.

### Base URL
All API endpoints are available under the `/api/` prefix.

### Available Endpoints
- `/api/students/` - Student management endpoints
- `/api/courses/` - Course management endpoints
- `/api/enrollments/` - Enrollment management endpoints

### Testing the API

1. Start the development server:
```bash
python manage.py runserver
```

2. Log in to the web interface first:
   - Visit `http://127.0.0.1:8000/accounts/login/`
   - Log in with your credentials

3. Access the API:
   - Visit `http://127.0.0.1:8000/api/` to see available endpoints
   - Use the browsable API interface to test endpoints
   - All endpoints require authentication

### API Features

#### Filtering, Searching, and Ordering
The API supports filtering, searching, and ordering through query parameters:

- **Filtering**: Filter results by specific field values
  ```
  GET /api/students/?major=Computer+Science
  ```

- **Searching**: Search across multiple fields
  ```
  GET /api/students/?search=john
  ```

- **Ordering**: Sort results by any field
  ```
  GET /api/students/?ordering=last_name
  ```

Multiple parameters can be combined:
```
GET /api/students/?search=smith&ordering=-created_at
```

#### Pagination
The API implements pagination with the following features:

- Default page size: 10 items per page
- Custom page size: `?page_size=20`
- Navigation: `?page=2`
- Example:
  ```
  GET /api/students/?page=2&page_size=20
  ```

#### Permissions
The API implements custom permission logic:

- **Student Records**:
  - List/Create: Any authenticated user
  - Retrieve: Any authenticated user
  - Update/Delete: Only the student owner or staff members

- **Course Records**:
  - List/Retrieve: Any authenticated user
  - Create/Update/Delete: Staff members only

- **Enrollment Records**:
  - List/Create: Any authenticated user
  - Retrieve: The enrolled student or staff members
  - Update/Delete: Staff members only

### Testing API Features

1. **Test Filtering and Search**:
   ```bash   
   # Filter active students
   curl -H "Authorization: Bearer <your-token>" "http://127.0.0.1:8000/api/students/?status=active"

   # Search for students
   curl -H "Authorization: Bearer <your-token>" "http://127.0.0.1:8000/api/students/?search=john"
   ```

2. **Test Pagination**:
   ```bash
   # Get second page with 20 items
   curl -H "Authorization: Bearer <your-token>" "http://127.0.0.1:8000/api/students/?page=2&page_size=20"
   ```

3. **Test Permissions**:
   ```bash
   # Try to update another student's record (should fail)
   curl -X PATCH -H "Authorization: Bearer <your-token>" "http://127.0.0.1:8000/api/students/2/" -d '{"status":"inactive"}'
   ```

## Project Structure

```
student_enrollment/
├── myproject/          # Project settings
├── myapp/             # Main application
├── manage.py          # Django management script
├── requirements.txt   # Project dependencies
└── .env              # Environment variables (not in git)
```

## Security Notes

- Never commit the `.env` file to version control
- Keep your `SECRET_KEY` secure
- Regularly update dependencies
- Use HTTPS in production
