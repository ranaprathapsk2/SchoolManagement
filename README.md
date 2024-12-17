# School Management System 

with Role-Based Access Control (Django) Description Develop a school management system using Django, allowing users to perform CRUD operations to manage student details across various classes. 

#  Description
The system should also handle library history and fees history for each student, which will be managed by specific roles within the school. The system will have separate logins for different user roles: School Admin, Office Staff, and Librarian. The Admin will have full control over both the Office Staff and Librarians, including the ability to create, edit, and delete staff and librarian accounts. The Librarian will only have access to view library history and student details, enabling them to manage the borrowing records of students effectively. The Office Staff will have access to all student details, including the ability to view library reviews, manage fees history, and perform other administrative tasks. 
# Roles & Permissions 
## Admin 
##### ● Full access to the system. 
##### ● Can create, edit, and delete accounts for Office Staff and Librarians.
##### ● Can manage student details, library history, and fees history. 
## Office Staff 
##### ● Access to all student details. 
##### ● Can manage (add, edit, delete) fees history. 
##### ● Can review library records. 
##### ● Cannot create or delete librarian or staff accounts. 
## Librarian 
##### ● View-only access to library history and student details. 
##### ● Cannot modify student data or fees records. 
##### ● Limited capabilities focused on managing library resources.

# Requirements 
#### Django 5.1.4
#### Django Rest Framework 3.15.2
#### Jwt Token 5.3.1


## Installation

#### 1. Create virtual Environment 

```bash
python -m venv venv
```
#### 2. Install Requirements
```bash
pip install -r requirements.txt
```
#### 3. Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

#### 4. Create a Superuser
```bash
python manage.py createsuperuser
```
#### 4. Create a Superuser
```bash
python manage.py runserver
```
