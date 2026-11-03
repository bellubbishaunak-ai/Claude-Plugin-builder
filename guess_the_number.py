"""Guess the secret number between 1 and 100 in as few tries as possible."""
import random

secret = random.randint(1, 100)
tries = 0

print("I picked a number between 1 and 100. Guess it!")
while True:
    try:
        guess = int(input("Your guess: "))
    except ValueError:
        print("Numbers only, please.")
        continue
    tries += 1
    if guess < secret:
        print("Too low.")
    elif guess > secret:
        print("Too high.")
    else:
        print(f"Correct! You got it in {tries} tries.")
        break
