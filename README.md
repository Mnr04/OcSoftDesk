# SoftDesk

This project is a RESTful API developed as part of the OpenClassrooms Python Developer path (Project 10).
It allows teams to manage their projects, issues, and comments securely.

## Technologies Used
* Python 3
* Django
* Django REST Framework (DRF)
* JWT Authentication

## Features

* **Authentication:** Secure login and signup using JWT Tokens.
* **Users:** Management of users.
* **Projects:** Create and manage projects.
* **Issues:** Track bugs, features, and tasks with priorities and status.
* **Comments:** Add comments to specific issues.
* **Permissions:**
    * Users must be authenticated to access data.
    * Only contributors of a project can view its issues and comments.
    * Only the author of a resource can update or delete it.

## Prerequisites

Before you begin, ensure you have met the following requirements:
* **Python**  installed.
* **Pipenv** or **Pip** for dependency management.
* **Git** installed.

## Installation & Setup

Follow these steps to run the project locally.

### 1. Clone the repository
```bash
git clone [https://github.com/Mnr04/OcSoftDesk.git]
cd ocsoftdesk
```

### 2. Set up the Virtual Environment
We recommend using pipenv to manage dependencies.

Using Pipenv:
```bash
pipenv install
pipenv shell
```

### 3. Database Configuration
Apply the migrations to create the database schema (SQLite by default).
```python
python manage.py makemigrations
python manage.py migrate
```

### 4. Run the Server
```python
python manage.py runserver
```

## Authentification Guide
This API uses JWT Authentication. You must obtain a token to access protected endpoints.

### 1. Register a new user (Signup)
Endpoint: POST /api/users/

Permissions: Public

Body:
```JSON
{
    "username": "MyUser",
    "password": "StrongPassword123!",
    "age": 25,
    "can_be_contacted": true,
    "can_data_be_shared": true
}
```

### 2. Login to get a Token
Endpoint: POST /api/login/
Body:
```JSON
{
    "username": "MyUser",
    "password": "StrongPassword123!"
}
```

### 3. Access Protected Routes
For all other requests (Projects, Issues, etc.), you must include the token in the Header:

Key: Authorization
Value: Bearer YOUR_ACCESS_TOKEN

##  API Endpoints

### User Management
* **Signup:** `POST /api/users/`
* **Login (Get Token):** `POST /api/login/`
* **Refresh Token:** `POST /api/token/refresh/`

### Projects
* **List / Create:** `GET` / `POST` -> `/api/projects/`
* **Details / Update / Delete:** `GET` / `PUT` / `DELETE` -> `/api/projects/{id}/`

### Issues
* **List / Create:** `GET` / `POST` -> `/api/issues/`
* **Details / Update / Delete:** `GET` / `PUT` / `DELETE` -> `/api/issues/{id}/`

### Comments
* **List / Create:** `GET` / `POST` -> `/api/comments/`
* **Details / Update / Delete:** `GET` / `PUT` / `DELETE` -> `/api/comments/{id}/`

### Contributors
* **List / Add:** `GET` / `POST` -> `/api/contributors/`
* **Remove:** `DELETE` -> `/api/contributors/{id}/`