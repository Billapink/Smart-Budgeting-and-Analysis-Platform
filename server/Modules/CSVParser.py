# The base state class serves as an abstract class that all other classes will inherit from.
class BaseState:
    def nextState(self, token):
        return self

    def consume(self, token, csvData):
        pass


# Start State
# Also reached for every start of a row in the CSV
class StateA(BaseState):
    def nextState(self, token):
        match token:
            case '"':
                return StateB(True)
            case ',': 
                return StateC()
            case '\n': 
                return self
            case "epsilon": 
                return StateZ()
        return StateD()

    def consume(self, token, csvData):
        csvData["fields"].append(csvData["current_field"])
        csvData["rows"].append(csvData["fields"])
        csvData["current_field"] = ""
        csvData["fields"] = []

# Quoted string field
class StateB(BaseState):
    def __init__(self, ignoreFirstToken):
        self.ignoreToken = ignoreFirstToken
    
    def nextState(self, token):
        match token:
            case '"': return StateE()
            case '\\': return StateF()
            case "epsilon": raise RuntimeError("Unexpected end of input")
        return self

    def consume(self, token, csvData):
        if self.ignoreToken:
            self.ignoreToken = False
            return
        
        csvData["current_field"] += token


# End of field
class StateC(BaseState):
    def nextState(self, token):
        match token:
            case '"': return StateB(True)
            case ',': return self
            case '\n': return StateA()
            case "epsilon": return StateZ()
        return StateD()

    def consume(self, token, csvData):
        csvData["fields"].append(csvData["current_field"])
        csvData["current_field"] = ""

# Regular unquoted field contents
class StateD(BaseState):
    def nextState(self, token):
        match token:
            case ',': return StateC()
            case '\n': return StateA()
            case "epsilon": return StateZ()
        return self

    def consume(self, token, csvData):
        csvData["current_field"] += token


# End of quoted string
class StateE(BaseState):
    def nextState(self, token):
        match token:
            case ',': return StateC()
            case '\n': return StateA()
            case "epsilon": return StateZ()
        
        raise RuntimeError("Invalid character after quoted string")

    def consume(self, token, csvData):
        pass

# Escaped character inside quoted string
class StateF(BaseState):
    def nextState(self, token):
        match token:
            case "epsilon": raise RuntimeError("Unexpected end of input")

        return StateB(False)

    def consume(self, token, csvData):
        pass

# End state
class StateZ(BaseState):
    def nextState(self, token):
        return self

    def consume(self, token, csvData):
        if (len(csvData["current_field"]) > 0 or len(csvData["fields"]) > 0):
            csvData["fields"].append(csvData["current_field"])
            csvData["rows"].append(csvData["fields"])

        csvData["current_field"] = ""
        csvData["fields"] = []


def makeRow(headers, rowData):
    row = {}
    if (len(headers) != len(rowData)):
        raise RuntimeError("Incorrect number of columns")
    
    for (i, name) in enumerate(headers):
        row[name.lower()] = rowData[i]
    
    return row

def parseCSV(csv_string):
    tokens = list(csv_string)
    # The epsilon token is a special token signalling the end of input.
    # All other tokens are single characters, so this can't be mistaken for a string
    tokens.append('epsilon')


    # accumulates the CSV data
    csvData = {
        "rows": [],
        "fields": [],
        "current_field": ""
    }

    state = StateA()

    for t in tokens:
        state = state.nextState(t)
        state.consume(t, csvData)
    
    rows = csvData["rows"]
    headers = rows.pop(0)
    return {
        "headers": headers,
        "rows": [makeRow(headers, r) for r in rows]
    }


