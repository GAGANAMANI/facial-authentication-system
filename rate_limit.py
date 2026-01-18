MAX_ATTEMPTS = 3
attempts = 0

def check_attempt(success):
    global attempts
    if success:
        attempts = 0
        return True

    attempts += 1
    if attempts >= MAX_ATTEMPTS:
        print("Too many attempts. Try again later.")
        return False
    return True
