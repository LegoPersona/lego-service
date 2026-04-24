FROM localhost/lego-service:latest
COPY src/ src
COPY templates/ templates
COPY requirements.txt .
RUN pip3 install -r requirements.txt
EXPOSE 8004
CMD ["uvicorn", "src.index:app", "--host", "0.0.0.0", "--port", "8004"]
