from flask import Flask, g
from proxy_pool import save_model

__all__ = ["app"]
app = Flask(__name__)


def get_conn():
    if not hasattr(g, 'redis'):
        g.redis = save_model.SaveModel()
    return g.redis


@app.route('/')
def index():
    return "<h2>欢迎来到代理池</h2>"


@app.route('/random')
def get_proxy():
    conn = get_conn()
    return conn.random_get_proxy()


@app.route('/count')
def get_counts():
    conn = get_conn()
    return str(conn.count())


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
