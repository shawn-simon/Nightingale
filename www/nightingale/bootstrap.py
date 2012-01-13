"""
Rebuild application from scratch with the following command:

python -m nightingale.bootstrap

"""
from nightingale.database import create_database, drop_database
        
if __name__ == '__main__':
    drop_database()
    create_database()