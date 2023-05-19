#set base image (host os)
FROM python

WORKDIR /code

#COPY /src/requirements.txt .
COPY /src/ .

RUN pip install -r requirements.txt



CMD [ "python", "./app.py" ]