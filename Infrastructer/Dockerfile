FROM python:3.8.8

COPY requirements.txt .

RUN python -m pip install --upgrade pip

RUN pip install -r requirements.txt

COPY . .

ENV PORT=80

EXPOSE 80

CMD [ "python", "app.py" ]