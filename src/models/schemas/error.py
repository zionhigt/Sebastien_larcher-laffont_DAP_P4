class SchemaError(Exception):
    def __init__(self, key, raison=None):
        self.key = key
        self.raison = raison
        super().__init__(self.raison)
    
    def __str__(self):
        return f"'{self.key}'\t{self.raison}"

class SchemaRequiredKeyError(SchemaError):
    def __init__(self, key, raison="Cette clé est requise"):
        self.key = key
        self.raison = raison
        super().__init__(self.key, self.raison)

class SchemaNotFoundKeyError(SchemaError):
    def __init__(self, key, raison="Cette clé n'existe pas dans le schema"):
        self.key = key
        self.raison = raison
        super().__init__(self.key, self.raison)

class SchemaEmptyFoundError(SchemaError):
    def __init__(self, key, raison="Le schema ne peux pas être vide"):
        self.key = key
        self.raison = raison
        super().__init__(self.key, self.raison)
