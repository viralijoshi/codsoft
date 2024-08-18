import random
import string

def generate_password(length):
    # Define the character set to use for the password
    characters = string.ascii_letters + string.digits + string.punctuation
    # Generate a random password
    password = ''.join(random.choice(characters) for _ in range(length))
    return password


# Prompt the user to specify the desired length of the password
length = int(input("Enter the desired length of the password: "))

if length <= 0:
    print("Please enter a positive number.")




# Generate the password
password = generate_password(length)
    
# Display the password
print("Generated Password:", password)


