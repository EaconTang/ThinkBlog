import json

import requests


def log(ret):
    with open('duoshuo.log', 'a') as f:
        try:
            mes = json.dumps(ret.json(), indent=4)
        except AttributeError:
            mes = ret.text
        except:
            mes = ret

        f.write(mes)
        f.write('\n' + '#' * 40 + '\n')


def clear_log():
    with open('duoshuo.log', 'w') as f:
        f.write('')


def main():
    clear_log()
    _d = dict(short_name='eacon',
              secret='74cd6131489314687b1433fceb9aa985',
              limit=999999)
    url = 'http://api.duoshuo.com/log/list.json?short_name={short_name}&secret={secret}&limit={limit}'.format(**_d)
    ret = requests.get(url)
    print ret.text
    log(ret)

    url = 'http://api.duoshuo.com/users/profile.json?user_id=13996649'
    log(requests.get(url))

    url = 'http://api.duoshuo.com/threads/counts.json?short_name=eacon&threads=355c6e035f24c7489321a164ff834f7a'
    log(requests.get(url))


if __name__ == '__main__':
    main()
