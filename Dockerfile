FROM pytorch/pytorch:1.12.1-cuda11.3-cudnn8-devel

## Update the package list and install necessary packages
#RUN apt-get update && apt-get install -y build-essential python3-pip
COPY . /workspace
RUN apt-get update
RUN apt-get -y install libgl1-mesa-glx
RUN apt-get -y install libglib2.0-0
RUN apt-get -y install curl
RUN pip install -r /workspace/requirements.txt
## Download and install the CUDA Toolkit
## ARG DEBIAN_FRONTEND=noninteractive
## RUN echo "Acquire::Check-Valid-Until \"false\";\nAcquire::Check-Date \"false\";" | cat > /etc/apt/apt.conf.d/10no--check-valid-until
#RUN ln -snf /usr/share/zoneinfo/$CONTAINER_TIMEZONE /etc/localtime && echo $CONTAINER_TIMEZONE > /etc/timezone
#RUN apt -y install nvidia-cuda-toolkit
#RUN apt-get install -y wget && apt-get install -y software-properties-common
#RUN wget -O /etc/apt/preferences.d/cuda-repository-pin-600 https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-ubuntu2004.pin
## RUN mv cuda-ubuntu2004.pin /etc/apt/preferences.d/cuda-repository-pin-600
## RUN apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/3BF863CC.pub
#RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys A4B469963BF863CC
#RUN add-apt-repository "deb http://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/ /"
#ARG DEBIAN_FRONTEND=noninteractive
#RUN apt-get -y install cuda-11-2
#RUN apt-get install -y nvidia-docker2

# RUN wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/cuda-ubuntu1804.pin
# RUN mv cuda-ubuntu1804.pin /etc/apt/preferences.d/cuda-repository-pin-600
# RUN apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/7fa2af80.pub
# RUN add-apt-repository "deb http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/ /"
# RUN apt-get update
# RUN apt-get -y install cuda

# # Set environment variables
# RUN echo "export CUDA_HOME=/usr/local/cuda" >> ~/.bashrc
# RUN echo "export PATH=$PATH:$CUDA_HOME/bin" >> ~/.bashrc
# RUN echo "export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$CUDA_HOME/lib64" >> ~/.bashrc

# Install PyTorch
# RUN pip3 install torch==1.7.0 torchvision

#VOLUME .
