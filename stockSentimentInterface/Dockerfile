FROM python:3.8.12-buster

COPY . .

RUN pip install -U pip
RUN pip install -e .

CMD streamlit run app.py