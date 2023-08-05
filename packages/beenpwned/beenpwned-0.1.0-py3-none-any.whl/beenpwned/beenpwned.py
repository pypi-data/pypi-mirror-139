import hashlib
import requests
import json
import argparse
import sys


def check_pwned_pwd(pw_in):    
    for pw in pw_in:
        try:
            sh1hash = hashlib.sha1(pw.encode('utf-8')).hexdigest().upper()
            head, tail = sh1hash[:5], sh1hash[5:]
            r = requests.get(f'https://api.pwnedpasswords.com/range/{head}')
            hashes = (line.split(':') for line in r.text.splitlines())
            count = next((int(count) for t, count in hashes if t == tail), 0)
            if count:
                print(f'Password : "{pw}" found {count} times [{sh1hash}]')
            else:
                print('Your password has not been pwned...yet! Keep Safe')
        except Exception:
            print(f'Something went wrong : {sys.exc_info()[0]}')


def check_pwned_account(accounts):
    for account in accounts:
        r = requests.get(f'https://haveibeenpwned.com/api/v2/breachedaccount/{account}')
        if r.text:
            for breach in r.json():
                print(f'{account} -> Account breached at : {breach["Name"]} - {breach["BreachDate"]}')
        else:
            print("No breach as been found")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check if a user account or password has been found in the haveibeenpwned database.")
    parser.add_argument('-p', '--p', nargs='+')
    parser.add_argument('-u', '--u', nargs='+')
    args = parser.parse_args()
    if args.p:
        check_pwned_pwd(args.p)
    if args.u:
        check_pwned_account(args.u)