import random
import string
import streamlit as st

# ==== Password Generator ====
def generate_password(length=12, include_upper=1, include_lower=1, include_digits=1, include_special=1):
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

# ==== Rule Checker ====
def check_rules(pwd, include_upper=1, include_lower=1, include_digits=1):
    if include_upper and not any(c.isupper() for c in pwd):
        return False
    if include_lower and not any(c.islower() for c in pwd):
        return False
    if include_digits and not any(c.isdigit() for c in pwd):
        return False
    return True

# ==== Strength Checker ====
def check_strength(pwd):
    score = 0
    if len(pwd) >= 8: score += 1
    if any(c.islower() for c in pwd): score += 1
    if any(c.isupper() for c in pwd): score += 1
    if any(c.isdigit() for c in pwd): score += 1
    if any(c in "!@#$%^&*()" for c in pwd): score += 1

    if score <= 2:
        return score, "Weak"
    elif score == 3:
        return score, "Medium"
    elif score == 4:
        return score, "Strong"
    else:
        return score, "Very Strong"

# ==== Streamlit UI ====
st.sidebar.title("Advanced Password Generator & Strength Checker")

# Sidebar controls
with st.sidebar:
    length = st.slider("Select Password Length", 8, 32, 12)
    include_upper = st.checkbox("Include Uppercase Letters (A-Z)", value=True)
    include_lower = st.checkbox("Include Lowercase Letters (a-z)", value=True)
    include_digits = st.checkbox("Include Numbers (0-9)", value=True)
    include_special = st.checkbox("Include Special Characters (!@#$...)", value=True)

    if st.button("Generate Password", use_container_width=True):
        pwd = generate_password(
            length=length,
            include_upper=include_upper,
            include_lower=include_lower,
            include_digits=include_digits,
            include_special=include_special
        )

        if "Error" in pwd:
            st.session_state.generated_pwd = None
            st.session_state.error = pwd
        else:
            st.session_state.generated_pwd = pwd
            st.session_state.error = None
            st.session_state.valid = check_rules(pwd, include_upper, include_lower, include_digits)
            st.session_state.score, st.session_state.strength = check_strength(pwd)

# Main display area
st.title("Password Output")

if st.session_state.get('error'):
    st.error(st.session_state.error)
elif st.session_state.get('generated_pwd'):
    st.code(st.session_state.generated_pwd, language='text')

    # Progress bar value and color logic
    score = st.session_state.score
    strength = st.session_state.strength
    progress = score / 5  # since max score is 5

    # Color mapping for strength
    color_map = {
        "Weak": "red",
        "Medium": "orange",
        "Strong": "yellowgreen",
        "Very Strong": "green"
    }
    bar_color = color_map.get(strength, "grey")

    
    st.progress(progress)

    
    st.markdown(
        f"<span style='color:{bar_color}; font-weight:bold;'>Strength: {strength} ({score}/5)</span>",
        unsafe_allow_html=True
    )
    st.markdown(f"*Fulfills selected rules:* {'Yes' if st.session_state.valid else 'No'}")
else:
    st.info("Generate a password using the controls in the sidebar.")
