import random

# Generate a random number between 1 and 9
randNo = random.randint(1, 9)
a = -1
guesses = 0
print("\nGuess the number between 1 and 9")
print("\n..:: The Perfect Guess ::..")

# Loop until the guessed number is equal to the random number
while (a != randNo):
    try:
        a = int(input(f"\n{guesses+1}. Enter the number: "))
        guesses += 1  # Increment the guess count for each attempt
        if(a > randNo):
            print("-->> Lower Number Please")
        elif(a < randNo):
            print("-->> Higher Number Please")
    except ValueError:
        print("--> You have entered the wrong number! Please enter the number between 1 and 9")
# Print the result after guessing the number correctly
print(f"\n..:: You have guessed the number {randNo} correctly in {guesses} attempts\n")
