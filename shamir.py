import random
from utils import inverse, encode, decode

Q=17
N=10
T=5

class Secret:
    def __init__(self, secret=None):
        self.secret = encode(secret) if secret is not None else None
        self.points =  [ p for p in range(1, N+1) ]
        self.degree = T
    
    def share(self):
        """
        Generate 'N' shares for the secret.
        """
        polynomial = sample_polynomial(self.secret)
        self.shares = [evaluate_polynomial(polynomial, i) for i in range(1, N+1)] 
        return self.shares

    def reconstruct(self):
        polynomial = [ (p,v) for p,v in zip(self.points, self.shares) if v is not None ]
        secret = interpolate_at_point(polynomial, 0)
        return secret

    def __add__(x, y):
        z = Secret()
        z.shares = [(xi + yi) % Q for xi, yi in zip(x.shares, y.shares) ]
        z.degree = max(x.degree, y.degree)
        return z        

    def __sub__(x, y):
        z = Secret()
        z.shares = [(xi - yi) % Q for xi, yi in zip(x.shares, y.shares) ]
        z.degree = max(x.degree, y.degree)
        return z   

    def __mul__(x, y):
        z = Secret()
        z.shares = [xi * yi for xi, yi in zip(x.shares, y.shares)]
        z.degree = x.degree + y.degree
        return z


def sample_polynomial(zero_coeff: int):
    """
    Sample a random polynomial of degree T, with zero_coeff as the coefficient of x^0    """
    coeffs = [zero_coeff] + [random.randrange(Q) for _ in range(T)]
    return coeffs

def evaluate_polynomial(coeffs: list[int], point: int):
    """
    Evaluate polynomial at a point (Horner's Rule)
    """
    result = 0
    for c in reversed(coeffs):
        result = (c+point*result) % Q
    return result

def lagrange_basis_polynomials(x_values: list[int], x:int):
    """
    Calculate the Lagrange basis polynomials for a given set of points at point `x`.
    """
    n = len(x_values)
    if n == 0:
        raise ValueError("The list of x values must not be empty.")
    
    # Initialize result
    lagrange_basis = []
    
    for i in range(n):
        num, denom = 1, 1
        for j in range(n):
            if i != j:
                num = (num * (x - x_values[j])) % Q
                denom = (denom * (x_values[i] - x_values[j])) % Q
                term = (num * inverse(denom)) % Q
        lagrange_basis.append(term)
    
    return lagrange_basis

def interpolate_at_point(points_values: list[(int, int)], point: int):
    """
    Interpolate points to get the polynomial using Lagrange's Polynomial Theorem 
    """
    points, values = zip(*points_values)
    constants = lagrange_basis_polynomials(points, point)
    return sum( vi * ci for vi, ci in zip(values, constants) ) % Q


