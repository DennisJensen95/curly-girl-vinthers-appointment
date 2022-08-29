FROM python:3.10-slim AS compile-image

COPY requirements.txt requirements.txt
RUN pip install --user -r requirements.txt

FROM python:3.10-slim AS application-image
WORKDIR /curly-girl
COPY --from=compile-image /root/.local /root/.local
COPY src src

CMD ["python", "src/main.py"]



