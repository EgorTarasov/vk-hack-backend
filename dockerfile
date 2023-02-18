FROM python:3.10

WORKDIR /code

COPY requirements.txt /code/requirements.txt

# RUN apt-get install libgeos-c1

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app
COPY ./sql /code/sql
COPY main.py /code
COPY settings.py /code

CMD ["python", "main.py"]
#CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]