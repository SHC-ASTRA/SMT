FROM python:3-alpine

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./astra .

EXPOSE 5000
CMD ["python", "manage.py", "runserver", "0.0.0.0:5000"]