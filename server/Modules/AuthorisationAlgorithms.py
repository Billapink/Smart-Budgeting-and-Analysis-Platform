import random as r
from flask import g

from Repositories.AuthorisationRepository import getAuthorisationRepo

class AuthorisationAlgorithms:
    def __init__ (self):
        self.authorisation_repo= getAuthorisationRepo()
        self.min_password_length, self.max_password_length = 7,10
        self.min_username_length, self.max_username_length = 4, 10
        self.min_company_length, self.max_company_length = 4, 10
        self.code_length = 6

    def login(self, username, password):
        #test to see if the user is in the database
        user_id= self.authorisation_repo.get_id_by_user(username)
        if user_id is None:
            return ["error", "Your username is not recognised, please try another."]
        elif self.verify_password(user_id, password):
            return ["success", "You have successfully logged in."]
        return ["error", "Incorrect password"]
            
        
    def verify_password(self, user_id, password):
        if len(password)< self.min_password_length:
            return ["error", "Password length too short."]
        #retrieving the hashed password of user in database
        actual_password_hash = self.authorisation_repo.get_passwordhash_by_id(user_id)
        if self.hash_password(password)== actual_password_hash:
            return True
        return False
        
    def hash_password(self, password):
        password_list= list(password)
        hash_value=0
        #multiplying the first two ascii values of characters in the password
        hash_value += ord(password_list[0])*ord(password_list[1])
        #for the rest of the characters in the word, we add the ascii values to that
        for char in password_list[2:]:
            hash_value += ord(char)
        #we return the hashed password as a number
        return hash_value

    def register_user(self, username, password):
        spec_char = False
        numeric_char = False
        #length validation
        if len(username) < self.min_username_length or len (username) > self.max_username_length:
            return ["error", "Username must be between 4 and 10 characters."]
        if len(password) < self.min_password_length or len(password) > self.max_password_length:
            return ["error","Password must be between 7 and 10 characters."]
        #special character and numerical values validation
        for char in password:
            if char in '!@£$%^&*()':
                spec_char = True
            if char in '0123456789':
                numeric_char = True
        if spec_char and numeric_char:
            [status, message] = self.authorisation_repo.create_user(username,self.hash_password(password))
            return ["success", "Account successfully created."] if status == "success" else ["error", message]
        return ["error","Password must include one special character and numerical value."]

    def create_company(self, user_id, company_name):
        #company name validation
        if len(company_name) < self.min_company_length or len(company_name) > self.max_company_length:
            return ["error", "Company name must be between 4 and 10 characters."]
        #checking if name already taken
        if self.authorisation_repo.get_company_id(company_name):
            return ["error", "Company already exists with that name."]
        #if all checks succeed, create the company access code
        company_code = []
        for i in range(6):
            company_code.append(str(r.randint(1,9)))
        company_code = ''.join(company_code)
        self.authorisation_repo.create_company(company_name, company_code)
        company_id = self.authorisation_repo.get_company_id(company_name)
        self.authorisation_repo.add_membership(user_id, company_id, "owner")
        return ["success", "Company successfully created."]

    #joining a company as a member using the code
    def join_company_by_code(self, user_id, company_id, role, code_input):
        company_code = self.authorisation_repo.get_company_code(company_id)
        if code_input == company_code:
            self.authorisation_repo.create_membership(user_id, company_id, role)
            return ["success", "Successfully joined company."]
        return ["error", "Incorrect company name or code."]

    #authorising the access to the company data as an existing member of the company
    def authorise_company_access(self, user_id, company_id, input_company_code):
        membership_exists = self.authorisation_repo.membership_exists(user_id)
        if membership_exists:
            if input_company_code == self.authorisation_repo.get_company_code(company_id):
                return ["success", "You have successfully logged into the company data."]
            return ["error", "Company code incorrect."]
        return ["error", "You do not have a membership to this company."]

def getAuthorisationAlgorithms():
    if "auth_algorithms" in g:
        return g.auth_algorithms;

    g.auth_algorithms = AuthorisationAlgorithms()
    return g.auth_algorithms
