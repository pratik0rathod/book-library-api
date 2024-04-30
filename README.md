# Book library API

# Running Locally


## Copy environment file and fill all requirements

    $ cp .env.template .env

## Run Server
- **Create Virtual environment**

        $ python3 -m venv /path/to/new/virtual/environment`

        $ source /path/to/new/virtual/environment/bin/activate`


- **Install dependencies**
    
        > pip install -r requirements.txt


- **Run Migrations**

         > alembic upgrade head


- **Run Server**

        > uvicorn book_management.main:app --reload