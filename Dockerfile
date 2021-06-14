FROM python:3.8
ENV TELEGRAM_BOT_TOKEN 1808023205:AAG1LNnbHCNdwXFIl-fMcdLSwRGtZsYc8OQ
RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app/
COPY . /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
CMD ["python", "main.py"]

