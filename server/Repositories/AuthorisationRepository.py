from Data.database import getDB
from flask import g

class AuthorisationRepository:
    def __init__(self):
        self.db = getDB()

    def get_id_by_user(self, username):
        userResult = self.db.execute('SELECT userID from users where username=?', (username,)).fetchall()
        if (len(userResult) > 0):
            print('USER', userResult[0][0])
            return userResult[0][0]
        
        return None

    
    def get_passwordhash_by_id(self, user_id):
        userResult = self.db.execute('SELECT password from users where userID=?', (user_id,)).fetchall()
        if (len(userResult) > 0):
            return userResult[0][0]
        
        return None
    
    def create_user(self, username, passwordhash):
        userIfExists = self.db.execute('SELECT userID from users where username=?', (username,)).fetchall()
        if (len(userIfExists) > 0):
            return ["error", "User already exists"]
        self.db.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, passwordhash))
        self.db.commit()
        return ["success", "user inserted into database"]

    def get_company_id(self, companyname):
        companyResult = self.db.execute('SELECT companyID from companies where company_name=?', (companyname,)).fetchall()
        if (len(companyResult) > 0):
            return companyResult[0][0]
        
        return None

    
    def create_company(self, company_name, company_code):
        self.db.execute('INSERT INTO companies (company_name, company_code) VALUES (?, ?)', (company_name, company_code))
        self.db.commit()

    def add_membership(self, user_id, company_id, role):
        self.db.execute('INSERT INTO memberships (userID, companyID, role) VALUES (?, ?, ?)', (user_id, company_id, role))
        self.db.commit()

    def get_company_code(self, company_id):
        companyResult = self.db.execute('SELECT company_code from companies where companyID=?', (company_id,)).fetchall()
        if (len(companyResult) > 0):
            return companyResult[0][0]
        
        return None

    def membership_exists(self, user_id):
        return True


def getAuthorisationRepo():
    if "auth_repo" in g:
        return g.auth_repo;

    g.auth_repo = AuthorisationRepository()
    return g.auth_repo
