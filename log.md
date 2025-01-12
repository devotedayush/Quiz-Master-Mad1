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
### setting up admin bugs
1. database error
2. options not visible error - either jinja syntax issue, or bootstrap overriding issue to be fixed by adding a div. 
3. setting view chapter wihout changing the url, but relaoding with new session
    1. I defined form to select subject id, and post it on endpoint admin.get_chapter
        1. I reload it in new html, whilst storing the subject_id in endpoint
        2. I store it as session, and reload the current url, and the jinja template waiting for chapter, suddenly presents itself. 
### Errors
1. 405 error - Sending Get Request, When Post is needed, and vice versa. 
2. 500 error - Server side issue.
