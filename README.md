<h1 align="center">City Car Management API</h1>

<p align="center">
  A Flask-based RESTful API for managing car owners and their vehicles in the quirky town of Nork-Town, where car ownership is limited and strictly regulated.
</p>

## 🌟 Features

- ✅ Add and list car owners
- 🚗 Add and list cars with specific color and model restrictions
- 🚫 Enforce a maximum of 3 cars per owner
- 🔐 Secure routes with JWT authentication

## 🛠 Prerequisites

- Docker
- Docker Compose

## 🚀 Getting Started

1. Clone the repository:

   ```sh
   git clone https://github.com/your-username/city-car-management.git
   cd city-car-management
   ```

2. Build and run the Docker containers:

   ```sh
   docker-compose up --build
   ```

   This command will build the Docker image and start the containers for the web application and the database.

3. The API will be available at `http://localhost:5000`

## 🧪 Testing

To run the automated tests, use the following command:

```sh
docker-compose run web pytest tests/test_app.py
```

This command will:

- Start a new container based on the web service configuration
- Run the pytest command inside the container
- Execute all tests defined in the `tests/test_app.py` file

For more detailed test output, you can add the `-v` flag:

```sh
docker-compose run web pytest -v tests/test_app.py
```

## 🛣 API Endpoints

| Method | Endpoint          | Description         |
| ------ | ----------------- | ------------------- |
| POST   | `/api/login`      | Obtain JWT token    |
| GET    | `/api/car_owners` | List all car owners |
| POST   | `/api/car_owners` | Add a new car owner |
| GET    | `/api/cars`       | List all cars       |
| POST   | `/api/cars`       | Add a new car       |

> **Note:** All endpoints except `/api/login` require JWT authentication.

## 🔧 Running API Requests

To interact with the API, you can use tools like curl or Postman. Here's an example using curl:

1. Login to get a token:

   ```sh
   curl -X POST http://localhost:5000/api/login -H "Content-Type: application/json" -d '{"username":"admin","password":"password"}'
   ```

2. Use the token to make authenticated requests:
   ```sh
   curl -X GET http://localhost:5000/api/car_owners -H "Authorization: Bearer YOUR_TOKEN_HERE"
   ```

Replace `YOUR_TOKEN_HERE` with the actual token received from the login request.

## 💻 Development

To make changes to the project:

1. Modify the code as needed
2. Rebuild and restart the Docker containers:
   ```sh
   docker-compose down
   docker-compose up --build
   ```
