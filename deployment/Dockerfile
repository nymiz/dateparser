FROM python:3.9
# Create app directory
WORKDIR /usr/src/app
# Install app dependencies
COPY . ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENV PYTHONUNBUFFERED=1
ENV PYTHONIOENCODING=UTF-8

EXPOSE 5000

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 run:app