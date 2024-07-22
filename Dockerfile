FROM python:3.12.3-alpine3.20
WORKDIR /usr/src/app
COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r /usr/src/app/requirements.txt
COPY insyn.py app.py proxies.txt /usr/src/app/
EXPOSE 80
CMD ["fastapi", "run", "/usr/src/app/app.py", "--port", "80"]