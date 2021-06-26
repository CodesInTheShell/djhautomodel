# DJHAUTOMODEL
FROM ubuntu

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1  
ENV LANG C.UTF-8
ENV PIP_TIMEOUT=6000

# System requirements
RUN apt-get update && apt-get install -y \
  build-essential \
  curl \
  python3-pip \
  swig \
  && rm -rf /var/lib/apt/lists/*

# Upgrade pip then install dependencies
RUN pip3 install --upgrade pip
RUN curl https://raw.githubusercontent.com/automl/auto-sklearn/master/requirements.txt \
  | xargs -n 1 -L 1 pip3 install

COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt

EXPOSE 8000

RUN python3 manage.py makemigrations
RUN python3 manage.py migrate --noinput
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
# CMD gunicorn djhautomodel.wsgi --workers=2 --bind="0.0.0.0:8000"