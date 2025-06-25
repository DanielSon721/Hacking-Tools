import itertools

def brute_force(target_pw, characters):

    attempts = 0

    for length in range (1, 10):
        for combination in itertools.product(characters, repeat = length):

            attempts += 1

            guess = "".join(combination)

            if guess == target_pw:
                print(f"The password is {guess}")
                print(f"Attempts: {attempts}")
                return
            elif attempts % 100000 == 0:
                print(f"Attempt {attempts}")


if __name__ == "__main__":

    target_pw = input("Enter a mock password: ")
    
    brute_force(target_pw, characters = "abcdefghijklmnopqrstuvwxyz1234567890")