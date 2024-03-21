FROM python

WORKDIR /var/bot

COPY . /var/bot/

RUN pip install -r requirements.txt

CMD [ "python", "manager.py" ]
