from celery import Celery
from brain.management.commands import import_google_sheets

app = Celery('sheetscrape', broker='pyamqp://alex@localhost//')


@app.task
def google_sheets():
    import_google_sheets.run()

