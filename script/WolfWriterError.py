
class WWError (Exception):
    def __init__(self,raison):
        self.raison = raison
    
    def __str__(self):
        return self.raison.encode('ascii','replace')

class WWEvalError (WWError):
    def __init__(self,to_evaluate):
        self.raison = "Can not evaluate the expression : "+to_evaluate
    
