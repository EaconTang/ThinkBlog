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
              limit=200,
              order='desc',
              since_id=6358198312285242113)
    url = 'http://api.duoshuo.com/log/list.json?short_name={short_name}&secret={secret}&limit={limit}'.format(**_d)
    ret = requests.get(url)
    print ret.text
    log(ret)


if __name__ == '__main__':
    main()
