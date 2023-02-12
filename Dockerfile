FROM pytorch/pytorch:1.12.1-cuda11.3-cudnn8-devel

## Update the package list and install necessary packages
#RUN apt-get update && apt-get install -y build-essential python3-pip
COPY . /workspace
RUN apt-get update
RUN apt-get -y install libgl1-mesa-glx
RUN apt-get -y install libglib2.0-0
RUN apt-get -y install curl
RUN pip install -r /workspace/requirements.txt

RUN alembic revision --autogenerate
RUN alembic upgrade head
#CMD ["uvicorn", "main:app", "--host 0.0.0.0", "--port 8000", "--reload"]

#VOLUME .
