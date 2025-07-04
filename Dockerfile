
ARG PYTHON_VERSION=3.9-slim-bullseye
FROM python:${PYTHON_VERSION}

# Create a virtual environment
RUN python -m venv ./venv

# Set the virtual environment as the current location
ENV PATH=./venv/bin:$PATH

# Upgrade pip
RUN pip install --upgrade pip

# Set Python-related environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install os dependencies for our mini vm
RUN apt-get update && apt-get install -y \
    # for postgres
    libpq-dev \
    # for Pillow
    libjpeg-dev \
    # for CairoSVG
    libcairo2 \
    # other
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Create the mini vm's code directory
# RUN mkdir -p /code

# Set the working directory to that same code directory
WORKDIR /usr/src/app

# Copy the requirements file into the container
COPY requirements.txt /tmp/requirements.txt
COPY bootstrap.sh .
# copy the project code into the container's working directory
COPY . .

# Install the Python project requirements
RUN pip install -r /tmp/requirements.txt

ARG PROJ_NAME="stackstats"
# Clean up apt cache to reduce image size
RUN apt-get remove --purge -y \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
RUN chmod +x /usr/src/app/bootstrap.sh
 # Start app
EXPOSE 5000
ENTRYPOINT ["/usr/src/app/bootstrap.sh"]