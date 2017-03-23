import requests

APP_ID = ''
SECRET = ''
REDIRECT_URI = ''


def main():
    """"""


def get_code():
    url = 'https://open.weixin.qq.com/connect/qrconnect?appid={}&redirect_uri={}&response_type=code&scope=snsapi_login&state=STATE#wechat_redirect'.format(
        APP_ID, REDIRECT_URI)
    return requests.get(url)


def get_token(code):
    url = 'https://api.weixin.qq.com/sns/oauth2/access_token?appid={}&secret={}&code={}&grant_type=authorization_code'.format(
        APP_ID, SECRET, code
    )


def refresh_token():
    """"""


def get_user_info():
    """"""
    url = '/sns/userinfo'


if __name__ == '__main__':
    main()
