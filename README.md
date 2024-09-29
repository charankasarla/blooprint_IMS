# Inventory Management System API's

## Overview
The Inventory Management System API is a backend application built with Django Rest Framework (DRF) designed to manage inventory items securely. It provides a comprehensive set of features including user registration, JWT authentication, CRUD operations for inventory items, and caching for improved performance using Redis. The application utilizes PostgreSQL for data storage and is structured to facilitate easy maintenance and testing.

## Table of Contents
- [Technologies Used](#technologies-used)
- [Features](#features)
- [API Endpoints](#api-endpoints)
  - [Authentication Endpoints](#authentication-endpoints)
  - [Inventory Item Endpoints](#inventory-item-endpoints)
- [Setup Instructions](#setup-instructions)
  - [Prerequisites](#prerequisites)
  - [Installation Steps](#installation-steps)
- [Running Tests](#running-tests)
- [Logging](#logging)
- [Future Improvements](#future-improvements)
- [License](#license)

## Technologies Used
- **Django Rest Framework (DRF)**: For building the RESTful API.
- **PostgreSQL**: As the database management system.
- **Redis**: For caching to enhance performance.
- **Django**: Web framework used to create the application.
- **JWT (JSON Web Token)**: For secure user authentication.
- **Python**: Programming language (version 3.9+).

## Features
- **User Registration**: Allows users to create new accounts.
- **User Login**: Authenticates users and provides JWT tokens for session management.
- **CRUD Operations**: Supports create, read, update, and delete operations for inventory items.
- **Caching**: Utilizes Redis for caching frequently accessed data, reducing database load.
- **Logging**: Integrated logging to monitor API usage and errors.
- **Unit Testing**: Comprehensive test coverage to ensure reliability and correctness.

## API Endpoints

### Authentication Endpoints
- **Register User**
  - **Method**: `POST`
  - **Endpoint**: `/api/register/`
  - **Request Body**: 
    ```json
    {
      "username": "your_username",
      "password": "your_password"
    }
    ```
  - **Response**:
    - `201 Created`: User registered successfully.
    - `400 Bad Request`: Username already exists.

- **Login User**
  - **Method**: `POST`
  - **Endpoint**: `/api/login/`
  - **Request Body**: 
    ```json
    {
      "username": "your_username",
      "password": "your_password"
    }
    ```
  - **Response**:
    - `200 OK`: Returns access and refresh tokens.
    ```json
    {
      "access": "access_token",
      "refresh": "refresh_token"
    }
    ```
    - `401 Unauthorized`: Invalid credentials.

### Inventory Item Endpoints
- **Create Item**
  - **Method**: `POST`
  - **Endpoint**: `/api/items/`
  - **Request Body**: 
    ```json
    {
      "name": "item_name",
      "description": "item_description"
    }
    ```
  - **Response**:
    - `201 Created`: Returns created item details.
    - `400 Bad Request`: Item already exists.

- **Get Item**
  - **Method**: `GET`
  - **Endpoint**: `/api/items/{item_id}/`
  - **Response**:
    - `200 OK`: Returns item details.
    - `404 Not Found`: Item not found.

- **Update Item**
  - **Method**: `PUT`
  - **Endpoint**: `/api/items/{item_id}/`
  - **Request Body**: 
    ```json
    {
      "name": "updated_item_name",
      "description": "updated_item_description"
    }
    ```
  - **Response**:
    - `200 OK`: Returns updated item details.
    - `404 Not Found`: Item not found.

- **Delete Item**
  - **Method**: `DELETE`
  - **Endpoint**: `/api/items/{item_id}/`
  - **Response**:
    - `204 No Content`: Item deleted successfully.
    - `404 Not Found`: Item not found.

- **Get All Items**
  - **Method**: `GET`
  - **Endpoint**: `/api/items/`
  - **Response**:
    - `200 OK`: Returns a list of all items.

## Setup Instructions

### Prerequisites
- Python 3.9 or higher
- PostgreSQL
- Redis
- Virtual Environment (venv)

### Installation Steps
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
python -m venv venv
# For Windows
.\venv\Scripts\activate
# For macOS/Linux
source venv/bin/activate

pip install -r requirements.txt

