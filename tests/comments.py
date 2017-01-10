import requests


def main():
    ret = requests.get('http://eacon.duoshuo.com/admin/')
    if ret.status_code == 200:
        print ret.text


if __name__ == '__main__':
    main()
