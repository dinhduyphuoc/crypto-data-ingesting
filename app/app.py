from flask import Flask
from api.market.market import market_module
from api.retry.retry import retry_module
from api.market_backfill.backfill import backfill_module
from utils.gcscheduler import createScheduler

app = Flask(__name__)


@app.get('/')
def index():
    return "Homepage"


app.register_blueprint(market_module, name='market')
app.register_blueprint(retry_module, name='retry')
app.register_blueprint(backfill_module, name='backfill')

if __name__ == "__main__":
    createScheduler()
    app.run(host="0.0.0.0", debug=True)
