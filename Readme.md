# CulturaAI

## Project Overview

This project aims to provide a platform for cultural preservation in the digital space through AI-powered tools. It leverages Python, Django Rest frameworks, and Docker for development and deployment.

## Key Features & Benefits

*   **AI Model Integration:** Utilizes AI models for content generation, translation and narrayion.
*   **User Authentication:** Secure authentication via Firebase.
*   **API Endpoints:** Provides RESTful APIs for accessing [Specify API functionalities].
*   **Dockerized Deployment:** Simplified deployment with Docker.
*   **Modular Design:** Organized into apps for maintainability (ai_models, analytics, authentication, games, stories, translations).
*   **Asynchronous Tasks:** Utilizes Celery for handling background tasks, such as translations.

## Prerequisites & Dependencies

Before you begin, ensure you have the following installed:

*   **Python:** Version 3.11 or higher.
*   **Docker:**  For containerization.
*   **Docker Compose:**  For multi-container application orchestration.
*   **PostgreSQL client:** Required for database interaction.

## Installation & Setup Instructions

Follow these steps to install and set up the project:

1.  **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd culturaAI
    ```

2.  **Create a virtual environment (recommended):**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Linux/macOS
    # venv\Scripts\activate  # On Windows
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure environment variables:**

    *   Create a `.env` file based on the `.env.example` template.
    *   Set the necessary environment variables, including database credentials, Firebase configuration, and API keys.

5.  **Set up the database:**

    *   Configure your PostgreSQL database.
    *   Update the `DATABASE` settings in `cultura_ai/settings.py` with your database credentials.
    *   Run migrations:

        ```bash
        python manage.py migrate
        ```

6.  **Configure Firebase:**
     *   Set up a Firebase project.
     *   Download your Firebase Admin SDK credentials as `serviceAccountKey.json` and place it in the `cultura_ai` directory.
     *   Configure Firebase settings in `cultura_ai/firebase_settings.py` and `apps/authentication/firebase_config.py` using the credentials and project settings.

7.  **Run the development server:**

    ```bash
    python manage.py runserver
    ```

8.  **Docker Setup (Alternative):**

    *   Build and run the Docker containers:

        ```bash
        docker-compose up --build
        ```

    *   This will start the application along with its dependencies (e.g., database) in Docker containers.

## Usage Examples & API Documentation

[Provide information on how to use the application, including API endpoints if applicable.  Example API endpoint documentation would be included here].

Example:

*   **Authentication Endpoint:** `/api/authentication/login` (POST - requires email and password)
*   **AI Model Endpoint:** `/api/ai_models/` (GET - retrieve list of available AI Models)

## Configuration Options

The following environment variables can be configured:

*   `DATABASE_URL`: The URL for the PostgreSQL database.
*   `FIREBASE_PROJECT_ID`: Your Firebase Project ID.
*   `SECRET_KEY`: Django's secret key.
*   `DEBUG`: Set to `True` for development mode.
*   Other API keys and credentials required by the application.

## Contributing Guidelines

We welcome contributions! To contribute to this project:

1.  Fork the repository.
2.  Create a new branch for your feature or bug fix.
3.  Make your changes and commit them with descriptive messages.
4.  Submit a pull request.

Please follow our coding style and guidelines.

## License Information

[Specify the project's license. If no license is intended, state that all rights are reserved].

Example:

This project is licensed under the [MIT License](LICENSE).

## Acknowledgments

[Acknowledge any third-party libraries, tools, or resources that were used in the project.]

Example:

*   Django ([https://www.djangoproject.com/](https://www.djangoproject.com/))
*   Celery ([https://docs.celeryq.dev/en/stable/](https://docs.celeryq.dev/en/stable/))
*   Firebase ([https://firebase.google.com/](https://firebase.google.com/))
