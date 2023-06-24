# Containerized_Python_Backend_App
# DevOps Project: User Authentication and Management

This project focuses on building a user authentication and management system using FastAPI and Tortoise ORM. It provides a Dockerized development environment for seamless deployment.

## Features

- User sign-in and token generation using OAuth2 password flow
- User creation with hashed passwords
- Protected routes with token-based authentication
- User details retrieval
- Home page access

## Technologies Used

- Python 3.9
- FastAPI
- Tortoise ORM
- Docker

## Setup Instructions

To run the project locally, follow these steps:

1. Clone the repository:

   ```
   git clone https://github.com/mohamedassaker/Containerized_Python_Backend_App.git
   ```

2. Navigate to the project directory:

   ```
   cd Containerized_Python_Backend_App
   ```

3. Build the Docker image and start the container:

   ```
   docker-compose up -d --build
   ```

   This command will build the Docker image and start the services defined in the `docker-compose.yaml` file.

4. The API will be accessible at `http://localhost:8000`.

## API Endpoints

- **POST /sign-in**: Generate an access token by providing the username and password in the request body. Returns the access token.

- **POST /create-user**: Create a new user by providing the username, email, and password in the request body. Returns the created user details.

- **POST /user-details**: Get the details of the currently authenticated user. Requires a valid access token.

- **POST /home**: Access the home page. Requires a valid access token.

## Environment Variables

The following environment variables can be set in the `.env` file:

- `DB_URL`: URL for the database connection (default: `sqlite://db.sqlite3`)
- `JWT_SECRET`: Secret key for JWT token generation (default: `"$ecretH@shP@ssw0rdTest"`)

## Development

If you want to modify it for your specific use case, follow these instructions:

1. Install the required dependencies from `requirements.txt`.

2. Make the necessary changes to the codebase.

3. Test the changes locally.

4. Build the Docker image using the provided Dockerfile or modify it according to your requirements.

5. Update the `docker-compose.yaml` file if needed.

6. Deploy the updated container or share the modified project with others.

## Notes

- By default, the project uses SQLite as the database. You can modify the `DB_URL` environment variable to use a different database.

- Ensure that you keep the `JWT_SECRET` environment variable secure. It is recommended to use a long, randomly generated string.
