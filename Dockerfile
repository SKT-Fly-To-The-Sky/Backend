FROM pytorch/pytorch:1.12.1-cuda11.3-cudnn8-devel

## Update the package list and install necessary packages
#RUN apt-get update && apt-get install -y build-essential python3-pip
COPY . /workspace
RUN apt-get update
RUN apt-get -y install libgl1-mesa-glx
RUN apt-get -y install libglib2.0-0
RUN apt-get -y install curl
RUN pip install -r /workspace/requirements.txt

#RUN curl -L -o ./ai_service/yolov3/weights/best_403food_e200b150v2.pt https://www.dropbox.com/s/msz9yfrmsrs0zst/best_403food_e200b150v2.pt?dl=0
#RUN alembic revision --autogenerate
#RUN alembic upgrade head
CMD ["uvicorn", "main:app", "--host 0.0.0.0", "--port 8000", "--reload"]

#VOLUME .
