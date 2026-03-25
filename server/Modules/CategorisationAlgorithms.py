import re
from flask import g

from Repositories.CategorisationRepository import getCategorisationRepo
class CategorisationAlgorithm:
    def __init__(self, defaultCategoryID, priority):
        self.repo = getCategorisationRepo()
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
    def create_category(self, companyID, category, categoryType):
        self.repo.create_category(companyID, category, categoryType)

        return ["success", "Category successfully created."]
    
    def create_rule(self, companyID, categoryID, matchType, pattern, priority):
        self.repo.create_rule(companyID, categoryID, matchType, pattern, priority)

        return ["success", "Rule successfully created."]

    def get_categories(self, companyID):
        result = self.repo.get_categories(companyID)
        
        if (result != None):
            return result
        else:
            raise RuntimeError("Could not obtain categories")
 
    def get_rules(self, companyID):
        result = self.repo.get_rules(companyID)
        
        if (result != None):
            return result
        else:
            raise RuntimeError("Could not obtain categories")
 
    def load_rules(self, companyID):
        self.rules = self.repo.get_rules(companyID)

    def set_rule_active(self, ruleID, active):
        self.rules = self.repo.set_rule_active(ruleID, active)

    def update_rule_priority(self, ruleID, priority):
        self.rules = self.repo.update_rule_priority(ruleID, priority)

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


def getCategorisationAlgorithms():
    if "cat_algorithms" in g:
        return g.cat_algorithms;

    g.cat_algorithms = CategorisationAlgorithm(1, 1)
    return g.cat_algorithms