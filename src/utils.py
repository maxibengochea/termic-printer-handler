def validate_field(colection: dict, field: str) -> bool:
    return colection[field] == True if field in colection.keys() else False