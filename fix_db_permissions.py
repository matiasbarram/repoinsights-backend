from django.conf import settings
from metabase.views.connector.create_role_and_policy import create_user_with_policy


if __name__ == "__main__":
    user = "valeriahenriquez"
    password = "valeriahenriquez"
    create_user_with_policy(
                    dbname=settings.CONSOLIDADA_DATABASE,
                    dbuser=settings.CONSOLIDADA_USER,
                    dbhost=settings.CONSOLIDADA_IP,
                    dbpassword=settings.CONSOLIDADA_PASSWORD,
                    dbport=settings.CONSOLIDADA_PORT,
                    username=user,
                    password=password,
                )