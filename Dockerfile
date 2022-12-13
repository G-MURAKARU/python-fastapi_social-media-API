# ORDER MATTERS

# point to the base container to build on top of
FROM python:3.11.0

# set the working directory of the application IN THE IMAGE
WORKDIR /usr/src/fastapi-app

# copy from the local directory to WORKDIR
COPY requirements.txt ./

# run a command on the target image
RUN pip3 install --no-cache-dir -r requirements.txt

# same as COPY above
COPY . .

# command we want to run
CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000" ]
