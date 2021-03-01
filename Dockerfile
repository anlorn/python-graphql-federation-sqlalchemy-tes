FROM python:3.7
WORKDIR .
COPY . /usr/app
WORKDIR /usr/app
RUN pip install SQLAlchemy graphene_sqlalchemy Flask-GraphQL Flask graphene-federation
EXPOSE 5000
CMD ["python", "app.py"]
