import requests
import hashlib
import sys


def request_api_password(a):
    url = 'https://api.pwnedpasswords.com/range/' + a
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error: {res.status_code} check what ur doing')
    return res


def get_password_leaks_count(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            # print(count)
            return count
    return 0


def pwned_api_check(password):
    hashed_password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    five_chars, tail = hashed_password[:5], hashed_password[5:]
    response = request_api_password(five_chars)

    return get_password_leaks_count(response, tail)


def main(args):
    for password in args:
        count = pwned_api_check(password)
        if count:
            print(f'{password} was found {count} times... you should probably change your password!')
        else:
            print(f'{password} was NOT found. Carry on!')
    return '\n \n done!'


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
