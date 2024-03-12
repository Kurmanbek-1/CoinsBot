FROM python:3.10
EXPOSE 5002
RUN mkdir -p /opt/CoinsBot
WORKDIR /opt/CoinsBot

RUN mkdir -p /opt/CoinsBot/requirements
ADD requirements.txt /opt/CoinsBot/

COPY . /opt/CoinsBot/

RUN pip install -r requirements.txt
CMD ["python", "/opt/CoinsBot/main.py"]