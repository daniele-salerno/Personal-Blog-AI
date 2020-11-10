from blog import app, db
from blog.models import User, Post

# passiamo i seguenti paramentri alla shell in 
# automatico così da non doverli richiamare ogni volta
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}