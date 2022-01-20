FROM python:3.7-slim
WORKDIR /app
# COPY api_yamdb/requirements.txt .
COPY api_yamdb .
RUN pip3 install -r /app/requirements.txt --no-cache-dir
CMD ["python3", "manage.py", "migrate"] 
CMD ["python3", "manage.py", "collectstatic", "--no-input"]
CMD ["gunicorn", "api_yamdb.wsgi:application", "--bind", "0:8000" ]
