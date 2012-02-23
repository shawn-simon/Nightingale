"""
Rebuild application from scratch with the following command:

python -m nightingale.bootstrap

"""
from nightingale.database import create_database, drop_database
from nightingale.models import User
from nightingale.simulation import registerusers
        
def create_users():
    print "adding user 1/35..."
    User.addUser(name='kdeloach', password='qwerasdf', namecss='f2 c3')
    for n in range(34):
        print "adding user %d/35..." % (n+1)
        registerusers(1)
    print "done"
    
if __name__ == '__main__':
    drop_database()
    create_database()
    create_users()
