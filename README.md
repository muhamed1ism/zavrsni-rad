# 🏥 eHospital - Microservice-Based Appointment Management System

- [Project Overview](#-license)
- [Key Features](#-key-features)
- [Technologies Used](#-technologies-used)
- [Project Structure](#-project-structure)
- [Usage](#-usage)
- [Docker Setup](#-docker-setup)
- [CI/CD Pipeline](#-ci/cd-pipeline)
- [Contributing](#-contributing)
- [License](#-license)
- [Acknowledgments](#-acknowledgments)

## 📖 Project Overview

eHospital is a **microservice-based web application** designed to streamline patient-doctor appointments. It allows patients to schedule appointments with doctors, while providing doctors with tools to manage their schedule and appointments efficiently. The backend is built using **Flask** microservices, and the frontend is developed using **Vue.js** with **Vuetify** for a responsive and user-friendly interface. This project uses **Docker** to containerize services for easier deployment.

## 🚀 Key Features

- **User Authentication**: Secure registration and login using JWT-based authentication.
- **Patient Profile Management**: Patients can manage their profiles and appointments.
- **Doctor Profile Management**: Doctors can manage their profiles and view patient appointments.
- **Appointment Management**: Schedule, cancel, and approve/reject appointments.
- **Microservices Architecture**: Independent services for authentication, profile management, and appointment handling.
- **Dockerized Deployment**: Each service is containerized using Docker for scalability and easy deployment.

## 🛠️ Technologies Used

- **Backend**:
  - Flask
  - Flask-SQLAlchemy
  - Flask-JWT-Extended
  - Flask-CORS
  - Gunicorn
  - SQLite
- **Frontend**:
  - Vue.js
  - Vuetify
  - Vue Router
  - Pinia (state management)
- **Containerization**:
  - Docker
  - Docker Compose
- **Testing**:
  - Pytest
  - Unit tests for microservices

## 📂 Project Structure

```bash
doctor-patient-appointment-system/
├── auth-microservice/
├── patient-microservice/
├── doctor-microservice/
├── appointment-microservice/
├── frontend/
├── docker-compose.yml
└── README.md
```

Each microservice has its own directory with the following structure:

- `/app`: Core application logic including routes, models, and configurations.
- `/tests`: Unit tests for the microservices.
- `/Dockerfile`: Configuration for Docker container.
- `/requirements.txt`: Dependencies for the service.

## ⚙️ Setup and Installation

### Prerequisites

- Docker & Docker Compose installed on your system.
- Yarn package manager for frontend dependencies.

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/doctor-patient-appointment-system.git
cd doctor-patient-appointment-system
```

### 2. Build and Run the Project with Docker Compose

```bash
docker-compose up --build
```

This will build and start all microservices and the frontend. The app will be accessible at `http://localhost:3000`.

### 3. Environment Configuration

Each microservice has its `.env` file for environment-specific configurations like database URIs and secret keys. An example `.env.example` is provided for guidance.

### 4. Running Tests

To run unit tests for the microservices:

```bash
docker-compose exec auth-microservice pytest
docker-compose exec patient-microservice pytest
```

## 🧭 Usage

1. **Sign up** as a patient or doctor.
2. **Login** to access the dashboard.
3. Patients can:
   - View available doctors and schedule appointments.
   - Cancel appointments if necessary.
4. Doctors can:
   - View their appointments.
   - Approve or reject appointment requests.

## 🐳 Docker Setup

Each service is dockerized, and a `docker-compose.yaml` file is provided to orchestrate the containers. To build and run all services:

```bash
docker-compose up --build
```

To bring down the containers:

```bash
docker-compose down
```

## 🔄 CI/CD Pipeline

For continuous integration and deployment, this project uses:

- **GitHub Actions**: To run unit tests and linting on each push.
- **Docker Hub**: For pushing and pulling Docker images.

## 🌟 Contributing

We welcome contributions! Please follow these steps to contribute:

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a pull request.

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Acknowledgments

- Special thanks to the **Faculty of Mechanical Engineering, Computing, and Electrical Engineering at the University of Mostar** for their support.
- Flask and Vue.js communities for their fantastic frameworks and tools.
