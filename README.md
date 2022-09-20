# Educata
## General info 
Educata is a learning management system project for Software Engineering 3rd grade, 1st term.

## Project setup

Prerequisites: **Python 3.10.X, NodeJS 16.14**

1. Go to root folder and run `python -m venv backend/.py-venv` to create python virtual environment
2. Select the venv in your IDE
3. Kill the IDE terminal and open it again to apply selected venv (check if `pip -V` gives you right path), otherwise activate the venv manually
4. Switch to backend directory `cd backend` and install the packages: `pip install -r requirements.txt`
5. Then switch to frontend directory `cd ../frontend` and install the packages: `npm i`
6. `cd .docker` from root and create `db.env` file according to `.example`
7. Run the database container: `docker compose up -d`

## Running the project

**From root:**

- frontend: `npm run start --prefix frontend`
- backend: 

## Git
### Branch flow

```
<type>/<project-prefix><ticket-number>-<short-desc>
```

#### Types:

- task
- fix

#### Examples:

- `task/frontend5-add-signin-page`
- `task/backend12-add-filters`
- `fix/common16-fix-signup-validation`

### Commit flow

```
<project-prefix>-<ticket-number>: <modifier> <desc>
```

#### Modifiers:

- `+` (add)
- `*` (edit)
- `-` (remove)

#### Examples:

- `frontend-5: + form component`
- `backend-12: * filter markup`
- `shared-16: - require prop for nickname field`

## Workflow

### Pull requests
