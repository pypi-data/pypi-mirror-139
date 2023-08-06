import hashlib
import requests
import sys


class beenpwnded:

    api_key = None

    def check_pwned_pwd(pw_in):
        try:
            sh1hash = hashlib.sha1(pw_in.encode('utf-8')).hexdigest().upper()
            head, tail = sh1hash[:5], sh1hash[5:]
            r = requests.get(
                f'https://api.pwnedpasswords.com/range/{head}')
            hashes = (line.split(':') for line in r.text.splitlines())
            count = next((int(count)
                          for t, count in hashes if t == tail), 0)
            if count:
                print(
                    f'Password : "{pw_in}" found {count} times [{sh1hash}]')
            else:
                print('Your password has not been pwned...yet! Keep Safe')
        except Exception:
            print(f'Something went wrong : {sys.exc_info()[0]}')

    def check_pwned_account(accounts):
        payload = {'hibp-api-key': beenpwnded.api_key}
        for account in accounts:
            r = requests.get(
                f'https://haveibeenpwned.com/api/v3/breachedaccount/{account}', params=payload)
            if r.text:
                for breach in r.json():
                    print(
                        f'{account} -> Account breached at : {breach["Name"]} - {breach["BreachDate"]}')
            else:
                print("No breach as been found")
