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

## Authentication Guide
This API uses JWT Authentication. You must obtain a token to access protected endpoints.

### 1. Register a new user (Signup)
Endpoint: POST /api/users/

Permissions: Public

Body:
```JSON
{
    "username": "User",
    "password": "Password",
    "first_name": "martin",
    "last_name": "pierre",
    "email": "user@example.com",
    "age": 18,
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

### 4. API Documentation & Examples

Here are the JSON bodies you need to send to create resources.

**Create a project**

```JSON
{
    "title": "Super iOS App",
    "description": "Development of the new mobile banking app.",
    "type": "IOS"
}
```
Note: type choices are: BACKEND, FRONTEND, IOS, ANDROID.
Note: The logged-in user automatically becomes the Author and a Contributor

**Create an issue**

```JSON
{
    "title": "Login Screen Crash",
    "description": "App crashes when clicking the button.",
    "issue_type": "BUG",
    "priority": "HIGH",
    "status": "TODO",
    "project": 1,
    "assignee": 2
}
```
Fields:

issue_type: BUG, FEATURE, TASK
priority: LOW, MEDIUM, HIGH
status: TODO, IN_PROGRESS, Finished
project: The ID of the project.
assignee: (Optional) The ID of the user assigned to this issue (must be a contributor).

**Create a Comment**

```JSON
{
    "description": "I have fixed this bug.",
    "issue": 5
}
```
Note: You must be a contributor of the project linked to issue #5 to post here.

**Add a Contributor to a Project**

```JSON
{
    "user": 3,
    "project": 1
}
```
Note: This adds User #3 to Project #1.


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

