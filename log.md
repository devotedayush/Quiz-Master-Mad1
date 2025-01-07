### Poem for where to start from - 
### Making the database 
1. Don't use shortcut for coulumn names. 
2. Carefull about the relation with the help of action while making the database
    1. like being carefull about cascade delete, and auto update. 
3. One-to-Many:
Focuses on the parent (Quiz) having multiple children (Questions).
The Quiz table gets a relationship() field for accessing its related questions.
Many-to-One:
Focuses on the child (Question) pointing to its parent (Quiz).
The Question table gets a ForeignKey field for linking to the Quiz
### Setting up the Flask app
1. way 1 (all on app.py)
    1. Configuration mus come BEFORE db= sqlachemy(app), configuration helps setup the database file path, which the intialised data base will work extending the flask app instance. 
    2. Debug by printing the loaded configuration, switching the intialization and conguration. 
2. way 2 (diffused & import)
    1. import config (load dotenv and filling value)
    2. import models (import app => db=SQLalchemy(app)=>with app.app_context, db.create_all())

