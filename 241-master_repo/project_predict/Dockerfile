# test docker file
# pip packages needed are: google-cloud-storage tensorflow keras

FROM python:3.9

ADD cred.json .
ADD upload.py .
ADD download.py .
ADD predictAPI.py .

RUN pip install google-cloud-storage tensorflow keras flask requests

EXPOSE 8080

CMD ["python3", "./predictAPI.py"]
