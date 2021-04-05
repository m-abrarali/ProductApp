# First stage
FROM python:3.8 AS builder
COPY requirements.txt .

# Install dependencies to the local user directory (eg. /root/.local)
RUN pip install --user -r requirements.txt

# Second unnamed stage
FROM python:3.8-slim
WORKDIR /code

# Copy only the dependencies installation from the 1st stage image
COPY --from=builder /root/.local /root/.local
COPY ./src .

# Update PATH environment variable
ENV PATH="/root/.local:$PATH"

EXPOSE 5000

CMD [ "python", "./main.py" ]
