# DevHubs

DevHubs is a developer marketplace platform where developers can showcase their projects and monetize them if desired. It provides a space for both frontend and backend projects, allowing creators to set up profiles, upload their work, and engage with consumers who can browse, download, or purchase projects.


## Prerequisites

Before running the application, ensure you have the following:

- Git (for version control)
- Node.js runtime environment
- Python3 and pip3

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