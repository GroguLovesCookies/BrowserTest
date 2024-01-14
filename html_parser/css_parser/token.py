class Token:
    TOKEN_RELATION: str = "REL"
    TOKEN_SELECTOR: str = "SELECTOR"
    TOKEN_PROPERTY: str = "PROPERTY"
    TOKEN_VALUE: str = "VALUE"

    RELATION_INDIRECT_PARENT: str = "INP"
    RELATION_DIRECT_PARENT: str = "DP"

    def __init__(self, tok_type, tok_value):
        self.type = tok_type
        self.value = tok_value

    def __repr__(self) -> str:
        return f"{self.type}: {self.value}"