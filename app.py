from chalice import Chalice

app = Chalice(app_name='projectbazar')


@app.route('/')
def index():
    return {'hello': 'world'}


