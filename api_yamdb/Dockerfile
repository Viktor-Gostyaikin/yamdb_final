FROM python:3.7-slim
WORKDIR /app
COPY api_yamdb .
RUN pip3 install -r /app/requirements.txt --no-cache-dir
RUN python3 /app/manage.py collectstatic --no-input
CMD ["gunicorn", "api_yamdb.wsgi:application", "--bind", "0:8000" ]
