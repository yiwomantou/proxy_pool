from flask import Flask, g
from proxy_pool.save_model import SaveModel

__all__ = ['app']
app = Flask(__name__)


def get_conn():
    if not hasattr(g, 'redis'):
        g.redis = SaveModel()
    return g.redis


@app.route('/index')
def index():
    return '<h2>Welcome to Proxy Pool System</h2>'


@app.route('/random')
def get_proxy():
    """
    获取可用的代理
    :return: 可用代理
    """
    conn = get_conn()
    return conn.random()


@app.route('/count')
def get_count():
    """
    获取可用的数量
    :return: 代理数量
    """
    conn = get_conn()
    return str(conn.count())


@app.route('/all')
def get_all():
    """
    获取所有可用的代理
    :return: 代理
    """
    conn = get_conn()
    result = ''
    for proxy in conn.all():
        result = result + proxy + '<br>'
    return str(result)


if __name__ == '__main__':
    app.run()
