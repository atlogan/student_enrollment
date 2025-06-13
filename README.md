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
- Docker and Docker Compose (for containerized setup)

## Installation

### Option 1: Docker Setup (Recommended)

1. Clone the repository:
```bash
git clone https://github.com/atlogan/student_enrollment
cd student_enrollment
```

2. Create a `.env` file:
```bash
cp .env.example .env
```

3. Update the `.env` file with your configuration:
```env
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=postgres://postgres:postgres@db:5432/postgres
ACCOUNT_EMAIL_REQUIRED=True
ACCOUNT_USERNAME_REQUIRED=False
ACCOUNT_AUTHENTICATION_METHOD='email'
ACCOUNT_EMAIL_VERIFICATION='optional'
LOGIN_REDIRECT_URL='/'
ACCOUNT_LOGOUT_REDIRECT_URL='/'
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
POSTGRES_USER=your-user
POSTGRES_PASSWORD=your-password
POSTGRES_DB=your-db
POSTGRES_HOST='db'
```

4. Build and start the containers:
```bash
docker compose build
docker compose up -d
```

5. The application will be available at:
   - Web Interface: http://localhost:8000
   - API Interface: http://localhost:8000/api/

### Option 2: Local Development Setup

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
   - Authorized redirect URI: `http://localhost:8000/accounts/google/login/callback/` (and/or http://localhost:8000/accounts/google/login/callback/)
7. Copy the Client ID and Client Secret to your `.env` file

## Database Setup

1. Create a PostgreSQL database
2. Update the `DATABASE_URL` in your `.env` file
3. Run migrations:
```bash
python manage.py migrate
```

## AWS Deployment

This project is deployed on AWS using the following services:
- Amazon ECR (Elastic Container Registry) for storing Docker images
- Amazon EC2 for hosting the application
- IAM Roles for secure access management

### Prerequisites
- AWS CLI installed and configured
- Docker and Docker Compose installed locally
- AWS account with appropriate permissions

### Deployment Process

#### 1. Setting up ECR Repository
```bash
# Create ECR repository
aws ecr create-repository --repository-name student-enrollment

# Login to ECR
aws ecr get-login-password --region <your-region> | docker login --username AWS --password-stdin <your-account-id>.dkr.ecr.<your-region>.amazonaws.com
```

#### 2. Building and Pushing Docker Image
```bash
# Build the image
docker build -t student-enrollment .

# Tag the image for ECR
docker tag student-enrollment:latest <your-account-id>.dkr.ecr.<your-region>.amazonaws.com/student-enrollment:latest

# Push to ECR
docker push <your-account-id>.dkr.ecr.<your-region>.amazonaws.com/student-enrollment:latest
```

#### 3. EC2 Instance Setup
1. Launch an EC2 instance (t3.micro recommended for Free Tier)
2. Configure security group to allow:
   - SSH (port 22)
   - HTTP (port 80)
   - Custom TCP (port 8000 for Django)
3. Attach an IAM role with ECR pull permissions (AmazonEC2ContainerRegistryReadOnly)
4. SSH into the instance and install Docker:
```bash
# Update system
sudo yum update -y

# Install Docker Engine and Docker Compose V2 plugin
sudo yum install -y docker docker-compose-plugin

# Start and enable Docker service
sudo systemctl start docker
sudo systemctl enable docker

# Add ec2-user to docker group
sudo usermod -aG docker ec2-user

# Activate group changes without logout/login
newgrp docker

# Verify installations
docker --version
docker compose version
```

#### 4. Required File Modifications

##### docker-compose.yml (Production Version)
The production version of docker-compose.yml requires several modifications:
1. Replace the `build: .` directive with the ECR image reference
2. Remove the local volume mount for code
3. Adjust the command to only run Gunicorn (migrations will be run separately)
4. Ensure proper port mapping

Example production docker-compose.yml:
```yaml
version: '3.8'
services:
  web:
    image: <your-account-id>.dkr.ecr.<your-region>.amazonaws.com/student-enrollment:latest
    container_name: django_web
    command: gunicorn myproject.wsgi:application --bind 0.0.0.0:8000
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - db
    restart: always

  db:
    image: postgres:16-alpine
    container_name: postgres_db
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    env_file:
      - .env
    restart: always

volumes:
  postgres_data:
```

##### .env (Production Version)
The production .env file requires specific modifications:
1. Set DEBUG=False for security
2. Configure ALLOWED_HOSTS with EC2 public IP/DNS
3. Set CSRF_TRUSTED_ORIGINS for the EC2 access URLs
4. Use production-grade secret key

Example production .env:
```env
DEBUG=False
SECRET_KEY=your-secure-production-key
ALLOWED_HOSTS=your-ec2-public-ip,your-ec2-public-dns
CSRF_TRUSTED_ORIGINS=http://your-ec2-public-ip:8000,http://your-ec2-public-dns:8000
DATABASE_URL=postgres://postgres:postgres@db:5432/postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=postgres
ACCOUNT_EMAIL_REQUIRED=True
ACCOUNT_USERNAME_REQUIRED=False
ACCOUNT_AUTHENTICATION_METHOD='email'
ACCOUNT_EMAIL_VERIFICATION='optional'
LOGIN_REDIRECT_URL='/'
ACCOUNT_LOGOUT_REDIRECT_URL='/'
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
```

#### 5. Deploying to EC2
1. Transfer files to EC2:
```bash
# From your local machine
scp -i your-key.pem docker-compose.yml .env ec2-user@your-ec2-ip:~/
```

2. SSH into EC2 and run the application:
```bash
# Login to ECR (if not using IAM role)
aws ecr get-login-password --region <your-region> | docker login --username AWS --password-stdin <your-account-id>.dkr.ecr.<your-region>.amazonaws.com

# Start the application
docker compose up -d

# Run migrations
docker compose exec web python manage.py migrate

# Create superuser (if needed)
docker compose exec web python manage.py createsuperuser
```

The application should now be accessible at `http://your-ec2-public-ip:8000`

### Important Notes
- Never commit the production `.env` or modified `docker-compose.yml` files
- Keep your AWS credentials secure
- Regularly update your EC2 instance and Docker images
- Consider setting up HTTPS using AWS Certificate Manager
- Monitor your application using AWS CloudWatch
- Set up regular backups of your PostgreSQL database
- Remember to stop or terminate your EC2 instance when not in use to avoid unnecessary charges

## Kubernetes Deployment

### Prerequisites
- Minikube or Docker Desktop with Kubernetes enabled
- kubectl CLI tool
- Helm v3+
- Docker image of the application (local or in a registry)

### Local Kubernetes Setup

1. Start Minikube:
```bash
minikube start
```

2. Add Health Check Endpoint
Add to `myapp/views.py`:
```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class HealthCheckView(APIView):
    def get(self, request, *args, **kwargs):
        return Response({"status": "ok"}, status=status.HTTP_200_OK)
```

Add to `myapp/urls.py`:
```python
from django.urls import path
from .views import HealthCheckView

urlpatterns = [
    # ... other urls
    path('health/', HealthCheckView.as_view(), name='health_check'),
]
```

3. Create Kubernetes Secrets
```bash
# Create postgres secret
echo "POSTGRES_PASSWORD=your_actual_db_password" > k8s-pg-secrets.env
kubectl create secret generic postgres-secret --from-env-file=k8s-pg-secrets.env
rm k8s-pg-secrets.env

# Create app secret
cat > k8s-app-secrets.env << EOL
SECRET_KEY=your_production_django_secret_key
DATABASE_URL=postgres://your_db_user:your_actual_db_password@postgres-service:5432/your_db_name
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
EOL
kubectl create secret generic app-secret --from-env-file=k8s-app-secrets.env
rm k8s-app-secrets.env
```

4. Image Management
For local images with Minikube:
```bash
# Option 1: Build with Minikube's Docker daemon
eval $(minikube -p minikube docker-env)
docker build -t student-enrollment:latest .

# Option 2: Load existing image
minikube image load student-enrollment:latest
```

5. Deploy Application
```bash
# Apply all manifests
kubectl apply -f k8s/postgres-pvc.yaml
kubectl apply -f k8s/postgres-deployment.yaml
kubectl apply -f k8s/postgres-service.yaml
kubectl apply -f k8s/app-configmap.yaml
kubectl apply -f k8s/app-deployment.yaml
kubectl apply -f k8s/app-service.yaml

# Run migrations
kubectl exec $(kubectl get pod -l app=myapp -o jsonpath="{.items[0].metadata.name}") -- python manage.py migrate
```

6. Access Application
```bash
# Get service URL
minikube service app-service --url

# Or use port-forwarding
kubectl port-forward service/app-service 8000:80
```

### Monitoring Setup

1. Install Prometheus & Grafana:
```bash
# Add Helm repo
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

# Install monitoring stack
helm install prom-stack prometheus-community/kube-prometheus-stack --namespace monitoring --create-namespace --version 72.0.1
```

2. Access Grafana:
```bash
# Get admin password
kubectl get secret --namespace monitoring prom-stack-grafana -o jsonpath="{.data.admin-password}" | base64 --decode

# Port-forward to Grafana
kubectl port-forward --namespace monitoring svc/prom-stack-grafana 3000:80
```
Access Grafana at http://localhost:3000 (admin/password-from-above)

### Scaling & Updates

```bash
# Scale deployment
kubectl scale deployment app-deployment --replicas=3

# Rolling update
kubectl set image deployment/app-deployment web=student-enrollment:v2
kubectl rollout status deployment/app-deployment

# Rollback if needed
kubectl rollout undo deployment/app-deployment
```

## Running the Application

### Using Docker (Recommended)

1. Start the application:
```bash
docker compose up -d
```

2. View logs:
```bash
docker compose logs -f web
```

3. Stop the application:
```bash
docker compose down
```

4. Access the application:
   - Web Interface: http://localhost:8000
   - API Interface: http://localhost:8000/api/

### Using Local Development Server

1. Start the development server:
```bash
python manage.py runserver
```

2. Visit `http://localhost:8000` in your browser

## Testing Authentication

### Local Authentication
1. Create a superuser:
```bash
python manage.py createsuperuser
```
2. Visit `http://localhost:8000/accounts/login/`
3. Log in with your superuser credentials

### Google Authentication
1. Visit `http://localhost:8000/accounts/login/`
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
   - Visit `http://localhost:8000/accounts/login/`
   - Log in with your credentials

3. Access the API:
   - Visit `http://localhost:8000/api/` to see available endpoints
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
   curl -H "Authorization: Bearer <your-token>" "http://localhost:8000/api/students/?status=active"

   # Search for students
   curl -H "Authorization: Bearer <your-token>" "http://localhost:8000/api/students/?search=john"
   ```

2. **Test Pagination**:
   ```bash
   # Get second page with 20 items
   curl -H "Authorization: Bearer <your-token>" "http://localhost:8000/api/students/?page=2&page_size=20"
   ```

3. **Test Permissions**:
   ```bash
   # Try to update another student's record (should fail)
   curl -X PATCH -H "Authorization: Bearer <your-token>" "http://localhost:8000/api/students/2/" -d '{"status":"inactive"}'
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

## Database Management

### Using Docker

The database migrations are automatically run when the containers start up. However, if you need to run migrations manually:

```bash
docker compose exec web python manage.py migrate
```

To create a superuser:
```bash
docker compose exec web python manage.py createsuperuser
```

