from Data.database import getDB
from flask import g

class AuthorisationRepository:
    def __init__(self):
        self.db = getDB()

    def get_id_by_user(self, username):
        userResult = self.db.execute('SELECT userID from users where username=?', (username,)).fetchall()
        if (len(userResult) > 0):
            return ["success", userResult[0]]
        
        return ["error", "User not found"]

    
    def get_passwordhash_by_id(self, user_id):
        userResult = self.db.execute('SELECT password from users where userID=?', (user_id,)).fetchall()
        if (len(userResult) > 0):
            return ["success", userResult[0]]
        
        return ["error", "User not found"]
    
    def create_user(self, username, passwordhash):
        userIfExists = self.db.execute('SELECT userID from users where username=?', (username,)).fetchall()
        if (len(userIfExists) > 0):
            return ["error", "User already exists"]
        self.db.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, passwordhash))
        self.db.commit()
        return ["success", "user inserted into database"]

    def get_company_id(self, companyname):
        return 123
    
    def create_company(self, company_name, company_code):
        pass

    def add_membership(self, user_id, company_id, role):
        pass

    def get_company_code(self, company_id):
        return 456
    
    def create_membership(self, user_id, company_id, role):
        pass

    def membership_exists(self, user_id):
        return True


def getAuthorisationRepo():
    if "auth_repo" in g:
        return g.auth_repo;

    g.auth_repo = AuthorisationRepository()
    return g.auth_repo
