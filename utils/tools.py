"""
Tools module.
"""
def kbytes_to_gbytes(value: float) -> str:
    """
    Transform Kb into Gb.
    """
    _value = value / (1024 ** 3)
    return "{:.2f}".format(_value)
