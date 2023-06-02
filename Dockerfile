# Usa una imagen base de Python
FROM python:3.10.6

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app
# Copia el archivo Pipfile y Pipfile.lock
COPY Pipfile Pipfile.lock /app/

RUN pip install django && pip install pipenv
COPY . /app/

RUN pipenv install --deploy
RUN pipenv install --system 

CMD ["pipenv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
#ENTRYPOINT ["tail", "-f", "/dev/null"]
