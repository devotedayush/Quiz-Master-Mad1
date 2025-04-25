# Quiz-Master-Mad1

Quiz Master Mad1 is a web-based quiz management system built with Flask and SQLAlchemy. It allows administrators to create, manage, and organize quizzes, subjects, chapters, and questions. The project demonstrates the use of relational databases, Flask web development, and dynamic content rendering with Jinja templates.

## Features

- Admin dashboard for managing subjects, chapters, quizzes, and questions
- Relational database design with one-to-many and many-to-one relationships
- Dynamic forms and data validation
- Error handling and debugging tips
- Modular code structure with separate configuration, models, and controllers

## Technologies Used

- **Python 3**
- **Flask** (web framework)
- **Flask-SQLAlchemy** (ORM for database management)
- **Jinja2** (templating engine)
- **Bootstrap** (for frontend styling)
- **dotenv** (for environment variable management)

## Project Structure

```
/controllers      # Flask route handlers and business logic
/models           # SQLAlchemy models for database tables
/templates        # Jinja2 HTML templates
/static           # Static files (CSS, JS, images)
app.py            # Main Flask application
config.py         # Configuration and environment loading
```

## What I Learned

- **Database Design:** Importance of clear column naming, setting up proper relationships (one-to-many, many-to-one), and handling cascade deletes and updates.
- **Flask App Setup:** The order of configuration and initialization matters. Debugging configuration issues by printing loaded values and switching initialization order.
- **Admin Interface:** Handling form submissions, session management, and dynamic template rendering. Dealing with issues like undefined variables in Jinja templates and redirecting with data.
- **Error Handling:** Recognizing and fixing common errors such as 405 (method not allowed) and 500 (server errors), and debugging template and database issues.
- **Frontend Integration:** Using Bootstrap for styling and resolving conflicts with Jinja syntax.

## How to Run

1. Clone the repository.
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set up environment variables in a `.env` file (see `config.py` for required variables).
4. Initialize the database:
   ```
   flask shell
   >>> from app import db
   >>> db.create_all()
   ```
5. Run the Flask app:
   ```
   flask run
   ```

## Troubleshooting

- Ensure configuration is loaded before initializing the database.
- Use Flask's debug mode to trace errors.
- Check for correct HTTP methods (GET/POST) in forms and routes.
- For template errors, verify variable names and use Jinja's conditional rendering.

## Acknowledgements

This project helped me understand the full stack of web development with Flask, from database design to frontend integration and debugging complex issues.
