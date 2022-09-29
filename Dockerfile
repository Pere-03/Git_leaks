FROM python:3.9.13-slim

ADD . ./
RUN apt update && apt-get install git -y && pip install -r requirements.txt 

CMD ["python3", "git_leaks.py"]