from flask import g

from Data.database import getDB

class CategorisationRepository:
    def __init__(self):
        self.dbCon = getDB()
    
    def get_categories(self, companyID):
        res = self.dbCon.execute("SELECT categoryID, category_name, type FROM categories WHERE companyID=?", (companyID,))

        categories = []
        for row in res:
            categories.append({
                "categoryID": row[0],
                "category_name": row[1],
                "type": row[2]
            })
        
        return categories

    def create_category(self, companyID, category, categoryType):
        data = (companyID, category, categoryType)
        
        self.dbCon.execute(
            "INSERT INTO categories(companyID, category_name, type) VALUES (?,?,?)", 
            data)
        self.dbCon.commit()
        return 
    
    def update_category(self, category):
        data = (category["companyID"], category["category_name"], category["type"], category["categoryID"])
        
        self.dbCon.execute(
            "UPDATE categories SET companyID = ?, category_name = ?, type = ? WHERE categoryID = ?", 
            data)

    def get_rules(self):
        res = self.dbCon.execute("SELECT ruleID, companyID, match_type, pattern, categoryID, priority, active FROM category_rules ORDER BY priority DESC")


        rules = []
        for row in res:
            rules.append({
                "ruleID": row[0],
                "companyID": row[1],
                "match_type": row[2],
                "pattern": row[3],
                "categoryID": row[4],
                "priority": row[5],
                "active": row[6]
            })
        
        return rules

    def create_rule(self, companyID, categoryID, matchType, pattern, priority):
        data = (companyID, categoryID, matchType, pattern, priority)
        
        self.dbCon.execute(
            "INSERT INTO category_rules(companyID, categoryID, match_type, pattern, priority, active) VALUES (?,?,?,?,?,1)", 
            data)
        self.dbCon.commit()
    
    def set_rule_active(self, ruleID, active):
        data = (active, ruleID)
        
        self.dbCon.execute(
            "UPDATE category_rules SET active = ? WHERE ruleID = ?", 
            data)

    def update_rule_priotity(self, ruleID, priority):
        data = (priority, ruleID)
        
        self.dbCon.execute(
            "UPDATE category_rules SET priority = ? WHERE ruleID = ?", 
            data)


def getCategorisationRepo():
    if "cat_repo" in g:
        return g.cat_repo;

    g.cat_repo = CategorisationRepository()
    return g.cat_repo