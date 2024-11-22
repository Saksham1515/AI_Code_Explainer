FROM python:3.10-slim

WORKDIR /code

COPY ./requirements.txt ./

RUN pip install -r requirements.txt

COPY . .
EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0","debug=True"]