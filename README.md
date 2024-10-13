# DevHubs

DevHubs is a developer marketplace platform where developers can showcase their projects and monetize them if desired. It provides a space for both frontend and backend projects, allowing creators to set up profiles, upload their work, and engage with consumers who can browse, download, or purchase projects. Developers can manage their uploads and track performance metrics.


## Prerequisites

Before running the application, ensure you have the following:

- Git (for version control)
- Node.js runtime environment
- Python3.8+ and pip3
- Django 5+

## Features

- **User Registration**: Separate registration for Developers and Consumers.
- **Developer Dashboard**: Manage uploaded projects, view project metrics (views, downloads, ratings).
- **Consumer Dashboard**: View bookmarked projects and projects they’ve rated.
- **Project Search**: Filter projects by categories and tags.
- **Project Ratings**: Consumers can rate and leave feedback on projects.
- **JWT Authentication**: Secure login/logout and token-based authentication.

## Project Structure

The project follows the **Django REST Framework** for the backend and utilizes **PostgreSQL** for database management. API documentation is available using **Swagger**.

```bash
project_root/
│
├── apps/
│   ├── users/       # Handles user registration, login, profile, and authentication
│   └── projects/    # Manages project uploads, ratings, and category/tag filtering
│
├── config/
│   ├── base.py  # Base Django settings and configuration 
│   ├── local.py  # Django settings and configuration for local environment
│   ├── production.py  # Django settings and configuration for production environment
│   └── urls.py      # Main URL routing
│
├── README.md        # Project documentation
└── requirements.txt # List of dependencies
```

## Running the App

1. Clone the repository

   ```bash
   git clone https://github.com/happychuks/devhubs-backend.git
   cd devhubs-backend
   ```

2. Create virtual environment

- For Linux/MacOS,

  ```bash  
  python3 -m venv .venv #if not created already
  source .venv/bin/activate
  ```

- For Windows,

  ```bash  
  pip3 install virtualenv
  virtualenv myenv
  myenv\Scripts\activate
  ```

3. Install dependencies for the project:

   ```bash
    pip3 install -r requirements.txt
   ```

4. Setup Environment Variables:

   Create a .env file in the root directory using the .env.example template and add all required variables:

   ```env
    DJANGO_SETTINGS_MODULE='devhubs_core.config.local' #for Dev environment

    # Sqlite3 database config
    SECRET_KEY='paste db.sqlite3 key here'

    # Production-Only Env Database config
    # PostgreSql Credentials
    DB_NAME=<enter database name>
    DB_USER=<enter username>
    DB_PASS=<enter password>
    DB_HOST=localhost
    DB_PORT=5432

    SITE_URL='http://localhost:8000'
    
   ```

5. Run the application in development mode:

- Start Server:

  ```bash
  python3 manage.py makemigrations # To compile the migrations
  python3 manage.py migrate  # To migrate the changes in Database
  python3 manage.py runserver # To run the API server  
  ```

## Testing and Documentation

### Sample Endpoints

- User Registration: /api/v1/users/register/
- Login: /api/v1/auth/login/
- Project List: /api/v1/projects/
- Add Project: /api/v1/projects/ (Developers only)
- Rate Project: /api/v1/projects/<project_id>/rate/

Test API endpoints [here](https://www.postman.com/martian-firefly-952437/workspace/devhubs/collection/20852361-c64bcd00-73f5-4a03-b0cd-94a214b5e44c?action=share&creator=20852361)

- View Swagger documentation here `http://127.0.0.1:8000/redoc/` and `http://127.0.0.1:8000/swagger/`

- To run Test Suites: `python manage.py test`

## Future Enhancements

- Paid project uploads and payment integration.
- Enhanced search and filtering by multiple tags.
- User role switching from consumer to developer.