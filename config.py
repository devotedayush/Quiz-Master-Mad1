from dotenv import load_dotenv
import os


# Load environment variables
load_dotenv()

# old way for which we had to import app. 
# app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
#app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
# new way
class Config:
    SQLALCHEMY_DATABASE_URI=os.getenv('SQLALCHEMY_DATABASE_URI',"192b9bdd22ab9ed9012e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf")
    SECRET_KEY= os.getenv('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    