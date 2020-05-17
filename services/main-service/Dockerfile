FROM python:3.6
WORKDIR /app
COPY requirements.txt /app
RUN pip install -r ./requirements.txt
COPY app.py /app
RUN mkdir -p ~/app/static
RUN mkdir -p ~/app/templates
COPY static/* /app/static/
COPY templates/* /app/templates/

CMD ["python", "app.py"]~