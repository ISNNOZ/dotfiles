import pyotp
import qrcode
import time

# Step 1: Generate a Secret Key
# This secret key is unique for each user. In a real-world scenario, you would store this in the user's database record.
def generate_secret_key():
    return pyotp.random_base32()

# Step 2: Generate a QR Code for Google Authenticator Setup
# This allows the user to scan the QR code and add the TOTP to their Google Authenticator app.
def generate_qr_code(secret, user_email):
    # Create a TOTP instance using the user's secret key
    totp = pyotp.TOTP(secret)
    
    # Generate a provisioning URL (for Google Authenticator, Authy, etc.)
    provisioning_url = totp.provisioning_uri(user_email, issuer_name="Instagram Security")
    
    # Generate a QR code for the provisioning URL
    qr = qrcode.make(provisioning_url)
    qr.show()  # Shows the QR code, which you can scan with an authenticator app
    
    return totp

# Step 3: Verify the TOTP Code (2FA Code)
# This verifies if the code provided by the user matches the one generated using the secret key.
def verify_2fa_code(totp, user_input_code):
    # Verify the user inputted code
    return totp.verify(user_input_code)

# Sample Usage
if __name__ == "__main__":
    # Generate a new secret key (In real applications, each user has their own secret key stored)
    secret_key = generate_secret_key()
    print(f"Your secret key (save this securely!): {secret_key}")
    
    # User's email (usually tied to their account)
    user_email = "user@example.com"
    
    # Generate a QR code for the user to scan
    totp_instance = generate_qr_code(secret_key, user_email)
    
    # Ask the user to enter the code generated in their Authenticator app
    user_code = input("Enter the 2FA code from your Authenticator app: ")
    
    # Verify the user-provided 2FA code
    if verify_2fa_code(totp_instance, user_code):
        print("2FA Code verified successfully!")
    else:
        print("Invalid 2FA Code! Please try again.")
