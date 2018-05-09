# Use an official Python runtime as a parent image
FROM python:3.6-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

# Make port 8082 available to the world outside this container
EXPOSE 8082

# Run app.py when the container launches

CMD [ "python", "manage.py","runserver","0.0.0.0:8082"]