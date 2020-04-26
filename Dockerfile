FROM python:3-alpine

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN apk add \
	zlib-dev \
	jpeg-dev \
	build-base
RUN pip install --no-cache-dir -r requirements.txt

COPY ./astra .

RUN python manage.py makemigrations smt
RUN python manage.py migrate

EXPOSE 5000
CMD ["python", "manage.py", "runserver", "0.0.0.0:5000", "--noreload"]
