FROM pytorch/pytorch:1.12.1-cuda11.3-cudnn8-devel

## Update the package list and install necessary packages
COPY . /workspace
RUN apt-get update
RUN pip install -r /workspace/requirements.txt

CMD ["uvicorn", "main:app", "--host 0.0.0.0", "--port 8000", "--reload"]

#VOLUME .
