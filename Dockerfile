FROM python:3.9.1
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV DJANGO_SETTINGS_MODULE=ecookbook.settings
WORKDIR /code
RUN apt-get -y update && apt-get -y install netcat
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
# run entrypoint.sh
ENTRYPOINT ["/code/entrypoint.sh"]