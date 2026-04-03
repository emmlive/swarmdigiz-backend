import pyotp


def generate_mfa_secret():

    return pyotp.random_base32()


def verify_mfa(secret, token):

    totp = pyotp.TOTP(secret)

    return totp.verify(token)