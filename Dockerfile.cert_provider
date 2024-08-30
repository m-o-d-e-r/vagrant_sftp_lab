FROM python:3.10-alpine AS builder

WORKDIR /app

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .env ./

RUN pip install -r requirements.txt


FROM python:3.10-alpine

WORKDIR /app

COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY cert_provider/ ./cert_provider/

CMD [ "python", "-m", "cert_provider" ]
