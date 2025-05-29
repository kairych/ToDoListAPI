# To-Do App API

This is a simple To-Do list API implemented using Django, Django REST Framework, and PostgreSQL. 
The project runs in Docker containers using Docker Compose.

### 1. Clone the repository
`git clone https://github.com/kairych/ToDoListAPI.git`

### 2. Configure environment variables
In your root project folder rename `.env.example` to `.env`

### 3. Build and start the containers
`docker compose up --build`

### 4. Open Swagger UI
Open `http://localhost:8000/api/docs/` to test endpoints.