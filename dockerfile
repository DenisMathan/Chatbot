FROM python:3.11.6-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --upgrade pip 
RUN pip install -r requirements.txt
RUN pip install gunicorn
RUN mkdir llms

COPY . .

# CMD ["python", "app.py"]

# CMD ["gunicorn", "-w" "4", "wsgi:app", "0.0.0.0:3333"]
EXPOSE 3333

CMD ["sh", "./start.sh"]
