# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.8-slim

EXPOSE 3001

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get -y install build-essential

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt
RUN python -m nltk.downloader -d /usr/share/nltk_data all
RUN python -m spacy download en_core_web_sm

WORKDIR /app
COPY . /app

#cronjob for dump update
COPY my_python /bin/my_python
COPY root /var/spool/cron/crontabs/root
RUN chmod +x /bin/my_python

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["gunicorn", "--bind", "0.0.0.0:3001", "main:app", "cron", "-f"]
