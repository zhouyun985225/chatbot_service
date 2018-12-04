# Use an official Python runtime as a parent image
FROM python:3.6-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
#RUN apt-get update && apt-get install -y gcc \
#    && pip install --trusted-host https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

RUN apt-get update && apt-get install -y gcc \
    && pip install -r requirements.txt

# Run app.py when the container launches

# CMD [ "python", "manage.py","runserver","0.0.0.0:8082"]
CMD ["python", "app.py"]