from celery import Celery 

app = Celery ('test', backend = None, broker = 'redis://localhost:6379/0')

@app.task(name='test.add')
def add(x, y): 
    print('{} + {} = {}'.format(x,y, x+y))