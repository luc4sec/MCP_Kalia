FROM kalilinux/kali-rolling

# Set working directory
WORKDIR /app

# Install Python, pip, and venv
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-venv

# Create and activate virtual environment
RUN python3 -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"

# Install Python dependencies in virtual environment
RUN pip install flask python-dotenv

# Copy only necessary files
COPY main.py .
COPY routes/ routes/
COPY responses.py .

# Create log directory
RUN mkdir -p /app/log

# Expose port
EXPOSE 8080

# Command to run the application
CMD ["python3", "-u", "main.py"] 