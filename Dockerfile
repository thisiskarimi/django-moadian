FROM python:3.8-slim-bookworm

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1

WORKDIR /home

COPY requirements requirements

RUN pip install --no-index --find-links requirements/ -r requirements/requirements.txt

RUN rm -rf /tmp/*
RUN rm -rf requirements/

CMD ["python", "django_moadian/manage.py", "runserver", "0.0.0.0:8000"]
