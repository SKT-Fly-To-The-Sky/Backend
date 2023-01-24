#FROM python:3.10
FROM continuumio/anaconda3

WORKDIR /code/

COPY ./ /code/
#COPY ./requirements.txt /code/requirements.txt

RUN
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

#CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]