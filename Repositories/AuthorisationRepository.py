class AuthorisationRepository:
    def get_id_by_user(self, username):
        return 123
    
    def get_passwordhash_by_id(self, user_id):
        'abcde'
    
    def create_user(self, username, passwordhash):
        pass

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