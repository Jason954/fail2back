FROM python:3.9-slim-buster

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV TZ=Europe/Paris
RUN date

# Set two environment variables
ENV SOCKET_PATH /app/socket
ENV DB_PATH /app/fail2ban.sqlite3
ENV DB_STATS_PATH /app/db/stats.db

# Set work directory in the container
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /app/

# Make start.sh executable
RUN chmod +x /app/start.sh

# Expose port
EXPOSE 8000

# Command to run the app
#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
# Command to run the app
CMD ["/app/start.sh"]