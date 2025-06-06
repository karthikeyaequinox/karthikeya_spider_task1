import random
from sympy import nextprime

# Evaluates the polynomial at a given x (mod prime)
def evaluate_polynomial(coeffs, x, prime):
    result = 0
    for i, coeff in enumerate(coeffs):
        result = (result + coeff * pow(x, i, prime)) % prime
    return result

# Generates n shares using a random polynomial of degree k-1
def generate_shares(secret, n, k, prime):
    coeffs = [secret] + [random.randint(1, prime - 1) for _ in range(k - 1)]
    shares = [(x, evaluate_polynomial(coeffs, x, prime)) for x in range(1, n + 1)]
    return shares

# Computes modular inverse (used for division in finite fields)
def mod_inverse(a, prime):
    return pow(a, -1, prime)

# Reconstructs the secret using Lagrange interpolation
def reconstruct_secret(shares, prime):
    secret = 0
    k = len(shares)

    for i in range(k):
        xi, yi = shares[i]
        li = 1
        for j in range(k):
            if i != j:
                xj, _ = shares[j]
                numerator = (0 - xj) % prime
                denominator = (xi - xj) % prime
                li *= numerator * mod_inverse(denominator, prime)
                li %= prime
        secret = (secret + yi * li) % prime

    return secret

def main():
    secret = int(input("Enter the secret (a number): "))
    n = int(input("How many total shares to create? "))
    k = int(input("Minimum shares needed to recover the secret? "))

    if k > n:
        print("Error: Threshold can't be greater than number of shares.")
        return

    prime = nextprime(secret + 100)
    print(f"Chosen prime for field arithmetic: {prime}")

    shares = generate_shares(secret, n, k, prime)
    print("\nGenerated Shares:")
    for i, share in enumerate(shares, start=1):
        print(f"  Share {i}: x = {share[0]}, y = {share[1]}")

    print(f"\nEnter any {k} shares to reconstruct the secret:")
    selected_shares = []
    for i in range(k):
        x = int(input(f"  Share {i+1} - x: "))
        y = int(input(f"  Share {i+1} - y: "))
        selected_shares.append((x, y))

    recovered = reconstruct_secret(selected_shares, prime)
    print(f"\nRecovered Secret: {recovered}")

if __name__ == "__main__":
    main()
