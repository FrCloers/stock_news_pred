FROM python:3.8.12-buster

COPY app.py app.py
COPY connect_db.py connect_db.py
COPY requirements.txt requirements.txt
COPY setup.py setup.py

RUN pip install -U pip
RUN pip install -e .

CMD streamlit run app.py --server.port 8080 --server.address '0.0.0.0'