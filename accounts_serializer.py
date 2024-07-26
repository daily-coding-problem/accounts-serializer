import json
import base64
import os
import re
import argparse


def validate_email(email):
    """Check if email is valid."""

    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        raise ValueError(f"Invalid email format for {email}.")


def print_dictionary(prompt, data):
    print("-----------------------------------------------")
    print(prompt)
    print(json.dumps(data, indent=4))


def main():
    parser = argparse.ArgumentParser(description="Add multiple users to TEST_ACCOUNTS environment variable.")
    parser.add_argument("--emails", nargs='+', required=True, help="User emails separated by space.")
    parser.add_argument("--passwords", nargs='+', required=True, help="User passwords separated by space.")
    parser.add_argument("--secrets", nargs='+', required=True, help="User secrets separated by space.")

    args = parser.parse_args()

    if not (len(args.emails) == len(args.passwords) == len(args.secrets)):
        raise ValueError("The number of emails, passwords, and secrets should match.")

    for email in args.emails:
        validate_email(email)

    print("This script will help you generate a base64 encoded string that can be used to set the TEST_ACCOUNTS "
          "environment variable.")
    print("The TEST_ACCOUNTS environment variable is used to authenticate users in the test environment.")

    if base64string := os.environ.get('TEST_ACCOUNTS', ''):
        decoded_bytes = base64.b64decode(base64string)
        decoded_string = decoded_bytes.decode('utf-8')
        accounts = json.loads(decoded_string)
    else:
        accounts = {}

    print_dictionary("Current data:", accounts)

    for email, password, secret in zip(args.emails, args.passwords, args.secrets):
        accounts[email] = {'password': password, 'secret': secret}

    serialized_data = json.dumps(accounts).encode('utf-8')

    print_dictionary("New data:", accounts)
    print("-----------------------------------------------")

    base64_encoded = base64.b64encode(serialized_data)

    print("Base64 Encoded Serialized Data:")
    print(base64_encoded.decode())


if __name__ == "__main__":
    main()
