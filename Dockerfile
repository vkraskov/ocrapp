FROM tesseractshadow/tesseract4re
MAINTAINER vkraskov

RUN apt-get update
RUN apt-get -y install python3 python3-pip

WORKDIR /app
ADD app /app

RUN pip3 install -r app/requirements.txt

EXPOSE ${APP_API_PORT}

CMD ["python3","-u","/app/bin/ocrapp.py"]
