import re


class CategorisationAlgorithm:
    def __init__(self, repo, defaultCategoryID, priority):
        self.repo = repo
        self.defaultCategoryID = defaultCategoryID
        self.priority = priority
        # Rules filled with sample data until we implement load_rules
        # Rules are assumed to be sorted by priority at all times
        self.rules = [
            {
                "ruleID": 1,
                "companyID": 123,
                "match_type": "regex", # regex or exact
                "pattern": "Adobe",
                "categoryID": 456,
                "priority": 9,
                "active": True
            }
        ]
    
    def load_rules(self):
        self.rules = self.repo.get_rules()


    def match_rule(self):
        pass
    
    def categorise_df(self):
        pass


    def categorise_transaction(self, transaction):
        '''
        Takes a transaction and returns the category ID
        '''
        for rule in self.rules:
            if not rule["active"]:
                continue
            
            if rule["match_type"] == "exact" and rule["pattern"] == transaction["merchant"]:
                return rule["categoryID"]
            
            if rule["match_type"] == "regex" and re.match(rule["pattern"], transaction["merchant"]) != None:
                return rule["categoryID"]


        # fallback when no rule matches the transaction
        return self.defaultCategoryID


    def apply_overrides(self):
        pass


    def set_manual_override(self):
        pass