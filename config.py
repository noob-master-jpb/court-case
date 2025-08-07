import subprocess
import sys
subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])

from app import app, db
from model import *
with app.app_context():
    db.create_all()
    
