class Token:
    TOKEN_RELATION: str = "REL"
    TOKEN_SELECTOR: str = "SELECTOR"
    TOKEN_PROPERTY: str = "PROPERTY"
    TOKEN_VALUE: str = "VALUE"
    TOKEN_SPLIT: str = "SPLIT"

    RELATION_INDIRECT_PARENT: str = "INP"
    RELATION_DIRECT_PARENT: str = "DP"
    RELATION_INDIRECT_SIBLING: str = "INS"
    RELATION_DIRECT_SIBLING: str = "DS"

    PSEUDOTYPE_NONE: str = "PSN"
    PSEUDOTYPE_TARGETED: str = "PST"

    def __init__(self, tok_type: str, tok_value: str, pseudo_type: str = "PSN"):
        self.type = tok_type
        self.value = tok_value
        self.pseudo_type = pseudo_type

    def __repr__(self) -> str:
        return f"{self.type}: {self.value}: {self.pseudo_type}"