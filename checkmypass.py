# usage: in commandline: python3 checkmypass.py techecken passwords 1234567
import requests
import hashlib
import sys


def request_api_data(query_char):
    """query naar de api van pwndpasswords.com
    alleen door als goede response terugkomt
    """
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(
            f'Error fetching: {res.status_code}, check the API and try again!')
    return res


def get_password_leaks_count(hashes, hash_to_check):
    """ Antwoord van de api is de resterende karakters van gehashed password, inclusief
    het aantal keer dat deze in de database voorkomt. Door antwoord te splitsen
    kan gecheckt worden tegen de "tail" van ons eigen password
    """
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0


def pwned_api_check(password):
    """ check of password(tail) aanwezig is in api response
    eigen password eerst omzetten in eigen formaat en 2 delen 
    definieren; eerste 5 worden verstuurd naar api
    """
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = sha1password[:5], sha1password[5:]
    response = request_api_data(first5_char)
    return get_password_leaks_count(response, tail)



def main(agrs):
    """Main functie: meegegeven argumenten(passwords) worden 
    gecheked
    """
    for password in agrs:
        count = pwned_api_check(password)
        if count:
            print(f'{password} was found {count} times...time to change it!')
        else:
            print(f'{password} was not found; Carry on!')
    return 'done!'


if __name__ == '__main__':
    # main(sys.argv[1:])
    # als er iets mis loopt; dan eruit!
    sys.exit(main(sys.argv[1:]))
