TODO

## Tech stack

The project was made with Django Rest Framework and SQLite as a backend and Next.js as a frontend. Shadcn was used as a base for our own components styled with Tailwind CSS.

## How to run

You have to have python,pip and npm installed to run this project.

Do it in cmd instead of powershell.

**Backend server**:

- `cd backend`

- Create virtual environment: `python -m venv venv`

- Activate virtual environment: `".\venv\scripts\activate"`  
(if it's not activating try using cmd instead of powershell)

- If (venv) is present before your directory in terminal, install required packages:
`pip install -r requirements.txt`

- Run Django server:
`python manage.py runserver`

- Server should run on http://localhost:8000

**Frontend server** (in other console):

- `cd frontend/`

- Install required packages: `npm install`

- Create build: `npm run build` (should take around 2 minutes)

- Start app: `npm run start`

- If doesn't work for some reason run in development mode\*: `npm run dev`

- Server should run at http://localhost:3000

- You can login using example account `email: admin@admin.pl` `password: admin`

\*-Development is faster to run but switching between sites might take longer due to jit compiling. If you click through routes and wait for 10-20s it should be faster
