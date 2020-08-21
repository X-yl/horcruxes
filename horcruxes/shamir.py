"""
    Implement's Shamir's Secret Sharing.
"""
import secrets 

MAX_PRIME = 2 ** 127 - 1  

def eval_polynomial_at(poly: tuple, x: int):
    """Evaluates a tuple polynomial at a point"""
    accum = 0
    for coeff in reversed(poly):
        accum *= x
        accum += coeff
        accum %= MAX_PRIME
    return accum

def generate_shares(secret: int, n: int, k: int) -> list:
    """Generates n shares such that k are required to recreate `secret`"""
    poly = secret, *tuple(secrets.randbelow(MAX_PRIME) for _ in range(k-1))

    points = [(x, eval_polynomial_at(poly, x)) for x in range(1, n+1)]

    return points
    
def extended_gcd(a, b):
    x = 0
    last_x = 1
    y = 1
    last_y = 0
    while b != 0:
        quot = a // b
        a, b = b, a % b
        x, last_x = last_x - quot * x, x
        y, last_y = last_y - quot * y, y
    return last_x, last_y

def divide_mod(num, den, p):
    """Compute num / den modulo prime p"""
    inv, _ = extended_gcd(den, p)
    return num * inv


def lagrange_interpolate(x, x_s, y_s, p):
    """
    Find the y-value for the given x, given n (x, y) points;
    k points will define a polynomial of up to kth order.
    """
    k = len(x_s)
    assert k == len(set(x_s)), "points must be distinct"
    def PI(vals):  # upper-case PI -- product of inputs
        accum = 1
        for v in vals:
            accum *= v
        return accum
    nums = []  # avoid inexact division
    dens = []
    for i in range(k):
        others = list(x_s)
        cur = others.pop(i)
        nums.append(PI(x - o for o in others))
        dens.append(PI(cur - o for o in others))
    den = PI(dens)
    num = sum([divide_mod(nums[i] * den * y_s[i] % p, dens[i], p)
               for i in range(k)])
    return (divide_mod(num, den, p) + p) % p


def find_secret(shares: list) -> int:
    x_s, y_s = zip(*shares)
    return lagrange_interpolate(0, x_s, y_s, MAX_PRIME)


import unittest

class TestShamir(unittest.TestCase):
    def test_shamir(self):
        import random
        from tqdm import tqdm

        tests = 50

        print(f"Running {tests} test cases...")
        for i in tqdm(range(tests)):
            secret = secrets.randbelow(MAX_PRIME)
            n = random.randrange(3,40)
            k = random.randrange(2,n)

            shares = generate_shares(secret, n, k)


            for i in range(5):
                random.shuffle(shares)
                recovered = find_secret(shares[:k])
                self.assertEqual(secret, recovered)

if __name__ == '__main__':
    unittest.main()