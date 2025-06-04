import random
import string

def generate_password(
    length=12,
    include_upper=1,
    include_lower=1,
    include_digits=1,
    include_special=1
):
    chars = ""
    password = []

    if include_upper:
        chars += string.ascii_uppercase
        password.append(random.choice(string.ascii_uppercase))

    if include_lower:
        chars += string.ascii_lowercase
        password.append(random.choice(string.ascii_lowercase))

    if include_digits:
        chars += string.digits
        password.append(random.choice(string.digits))

    if include_special:
        special_chars = "!@#$%^&*()"
        chars += special_chars
        password.append(random.choice(special_chars))

    if not chars:
        return "Error: At least one character type must be included."

    while len(password) < length:
        password.append(random.choice(chars))

    random.shuffle(password)
    return "".join(password)

def check_rules(pwd, include_upper=1, include_lower=1, include_digits=1):
    if include_upper and not any(c.isupper() for c in pwd):
        return False
    if include_lower and not any(c.islower() for c in pwd):
        return False
    if include_digits and not any(c.isdigit() for c in pwd):
        return False
    return True

def check_strength(pwd):
    score = 0
    length = len(pwd)

    if length >= 8:
        score += 1
    if any(c.islower() for c in pwd):
        score += 1
    if any(c.isupper() for c in pwd):
        score += 1
    if any(c.isdigit() for c in pwd):
        score += 1
    if any(c in "!@#$%^&*()" for c in pwd):
        score += 1

    if score <= 2:
        strength = "Weak"
    elif score == 3:
        strength = "Medium"
    elif score == 4:
        strength = "Strong"
    else:
        strength = "Very Strong"

    return score, strength

#Test
if __name__ == "__main__":
    try:
        user_length = int(input("Enter password length (8 to 32): "))
        if user_length < 8 or user_length > 32:
            print("Length must be between 8 and 32.")
        else:
            pwd = generate_password(
                length=user_length,
                include_upper=1,
                include_lower=1,
                include_digits=1,
                include_special=1
            )
            print("Generated Password:", pwd)
            print("Valid Password:", check_rules(pwd))
            score, strength = check_strength(pwd)
            print(f"Password Strength: {strength} ({score}/5)")
    except ValueError:
        print("Please enter a valid number.")
