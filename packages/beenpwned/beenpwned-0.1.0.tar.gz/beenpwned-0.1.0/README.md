# pwned
pwned is a small python script to check if a user account or password has been pwned and can be found in the [https://haveibeenpwned.com/](https://haveibeenpwned.com/) database. 

# How to use
## Check Passwords
`pwned.py -p password1 password2 password3 ...`

If your password has been found it will return with a result set

`Password : "password1" found 74831 times [A94A8FE5CCB19BA61C4C0873D391E987982FBBD3]`

## Check user account
`pwned.py -u user@account.com user1@account.com`

If one of the user accounts have been found it will return a list of the breached services

`user@account.com -> Account breached at : Adobe - 2013-10-04`
