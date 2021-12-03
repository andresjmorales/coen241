# test docker file
# pip packages needed are: google-cloud-storage tensorflow pandas matplotlib sklearn

FROM python:3.9

ADD MLdriver.py .
ADD cred.json .
ADD upload.py .
ADD download.py .
ADD app.py .

RUN pip install google-cloud-storage tensorflow pandas matplotlib sklearn flask requests

EXPOSE 5000

CMD ["python3", "./app.py"]
