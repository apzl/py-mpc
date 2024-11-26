Q = 17

def encode(n: int):
    return n%Q

def decode(n: int):
    return n if n <= Q/2 else n-Q


def extended_binary_gcd(a: int, b: int) -> int:
    """
    Extended binary GCD algorithm to find the greatest common divisor of two integers
    and also to express this gcd as a linear combination of these two integers.
    
    Args:
        a (int): The first integer.
        b (int): The second integer.

    Returns:
        tuple: A tuple containing the gcd, and the coefficients x and y such that ax + by = gcd.
    """
    u, v, s, t, r = 1, 0, 0, 1, 0
    while (a % 2 == 0) and (b % 2 == 0):
        a, b, r = a//2, b//2, r+1
    alpha, beta = a, b
    while (a % 2 == 0):
        a = a//2
        if (u % 2 == 0) and (v % 2 == 0):
            u, v = u//2, v//2
        else:
            u, v = (u + beta)//2, (v - alpha)//2
    while a != b:
        if (b % 2 == 0):
            b = b//2
            if (s % 2 == 0) and (t % 2 == 0):
                s, t = s//2, t//2
            else:
                s, t = (s + beta)//2, (t - alpha)//2
        elif b < a:
            a, b, u, v, s, t = b, a, s, t, u, v
        else:
            b, s, t = b - a, s - u, t - v
    return (2 ** r) * a, s, t
    
def inverse(a: int):
    """
    Multiplicative inverse of 'a' 
    """
    _, inverse, _ = extended_binary_gcd(a, Q)
    return inverse
