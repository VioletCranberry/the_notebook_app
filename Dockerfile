# Use an official Python runtime as a builder image.
FROM python:3.9-slim-bullseye AS builder

# Set the maintainer label.
LABEL repository="https://github.com/VioletCranberry/the_notebook_app"
LABEL maintainer="VioletCranberry"

# Set up a working directory.
WORKDIR /app

# Don’t check PyPI for a new version of pip.
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

# Install dependencies.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt --target /app

# Use the distroless image.
# See https://github.com/GoogleContainerTools/distroless
FROM gcr.io/distroless/python3-debian12:nonroot

# Set up a working directory.
WORKDIR /app

# Ensure Python will find the dependencies.
ENV PYTHONPATH=/app
# Prevent Python from buffering stdout and stderr.
ENV PYTHONUNBUFFERED=1

# Copy dependencies.
COPY --from=builder /app .
COPY templates templates/
COPY static/ static/
COPY k8s_manager.py .
COPY utils.py .

# Add the application script.
COPY app.py .
ENTRYPOINT ["python3", "app.py"]
