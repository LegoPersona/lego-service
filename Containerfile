FROM localhost/lego-service:latest
COPY src/ ./src/
COPY templates/ ./templates/
COPY test-api.py ./test-api.py
COPY model.ldr ./model.ldr
