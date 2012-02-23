"""
Rebuild application from scratch with the following command:

python -m nightingale.bootstrap

"""
from nightingale.database import create_database, drop_database
from nightingale.models import User
from nightingale.simulation import registerusers
        
def create_users():
    User.addUser(name='kdeloach', password='qwerasdf', namecss='f2 c3')
    registerusers(30)
    
if __name__ == '__main__':
    drop_database()
    create_database()
    create_users()
