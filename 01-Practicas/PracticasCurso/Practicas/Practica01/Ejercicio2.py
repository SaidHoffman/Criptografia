from sympy import isprime, randprime
import random

def generar_ec_no_singular(p):
    if p < 2 or not isprime(p):
        raise ValueError("El número debe ser primo y mayor a 2")

    while True:
        a = random.randint(1, p - 1)
        b = random.randint(1, p - 1)
        if (4 * pow(a, 3) + 27 * pow(b, 2)) % p != 0:
            return a, b, f'y^2 = x^3 + {a}x + {b}'
