FROM python:3.9-slim


COPY generate_data_clients.py .
COPY generate_data_products.py .
COPY generate_data_orders.py .


RUN pip install psycopg2-binary faker

CMD ["sh", "-c", "sleep 10 && python generate_data_clients.py && python generate_data_products.py && python generate_data_orders.py"]
