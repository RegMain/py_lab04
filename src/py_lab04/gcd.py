
def iteration_gcd(a: int, b: int) -> int:
    if not isinstance(a, int) or not isinstance(b, int):
        raise TypeError(
            f"ERROR: Expected {int}, {int}, got {type(a)}, {type(b)} instead.\n"
        )
    while b != 0:
        a, b = b, a % b
    return abs(a)

def recursion_gcd(a: int, b: int) -> int:
    if not isinstance(a, int) or not isinstance(b, int):
        raise TypeError(
            f"ERROR: Expected {int}, {int}, got {type(a)}, {type(b)} instead.\n"
        )
    if b == 0:
        return abs(a)
    else:
        return recursion_gcd(b, a % b)
