FROM python:3.10

# Set working directory
WORKDIR /code

# Install system dependencies
# RUN apt-get install libgeos-c1

# Install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy source code
COPY ./src/app/ ./app/
COPY ./src/sql/ ./sql/
COPY ./src/main.py ./
COPY settings.py ./

# Expose port
EXPOSE 8000

# Run the app
CMD ["python", "main.py"]
#CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
