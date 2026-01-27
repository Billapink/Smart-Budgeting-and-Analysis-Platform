class CategorisationRepository:
    def __init__(self, dbCon):
        self.dbCon = dbCon
    
    def get_categories(self):
        res = self.dbCon.execute("SELECT categoryID, companyID, category_name, type FROM categories")


        categories = []
        for row in res:
            categories.append({
                "categoryID": row[0],
                "companyID": row[1],
                "category_name": row[2],
                "type": row[3]
            })
        
        return categories

    def create_category(self, category):
        data = (category["companyID"], category["category_name"], category["type"])
        
        self.dbCon.execute(
            "INSERT INTO categories(companyID, category_name, type) VALUES (?,?,?)", 
            data)
    
    def update_category(self, category):
        data = (category["companyID"], category["category_name"], category["type"], category["categoryID"])
        
        self.dbCon.execute(
            "UPDATE categories SET companyID = ?, category_name = ?, type = ? WHERE categoryID = ?", 
            data)

    def get_rules(self):
        res = self.dbCon.execute("SELECT ruleID, companyID, match_type, pattern, categoryID, priority, active FROM rules ORDER BY priority DESC")


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

    def create_rule(self, rule):
        data = (rule["companyID"], rule["match_type"], rule["pattern"], rule["categoryID"], rule["priority"], rule["active"])
        
        self.dbCon.execute(
            "INSERT INTO rules(companyID, match_type, pattern, categoryID, priority, active) VALUES (?,?,?,?,?,?)", 
            data)
    
    def set_rule_active(self, ruleID, active):
        data = (active, ruleID)
        
        self.dbCon.execute(
            "UPDATE rules SET active = ? WHERE ruleID = ?", 
            data)

    def update_rule_priotity(self, ruleID, priority):
        data = (priority, ruleID)
        
        self.dbCon.execute(
            "UPDATE rules SET priority = ? WHERE ruleID = ?", 
            data)
