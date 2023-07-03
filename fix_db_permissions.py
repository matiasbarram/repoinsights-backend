from metabase.views.connector.create_role_and_policy import create_user_with_policy

import os

if __name__ == "__main__":
    user = "valeriahenriquez"
    password = "valeriahenriquez"

    CONSOLIDADA_DATABASE = os.environ["CONSOLIDADA_DB"]
    CONSOLIDADA_USER = os.environ["CONSOLIDADA_USER"]
    CONSOLIDADA_IP = os.environ["CONSOLIDADA_IP"]
    CONSOLIDADA_PASSWORD = os.environ["CONSOLIDADA_PASS"]
    CONSOLIDADA_PORT = os.environ["CONSOLIDADA_PORT"]
    

    create_user_with_policy(
                    dbname=CONSOLIDADA_DATABASE,
                    dbuser=CONSOLIDADA_USER,
                    dbhost=CONSOLIDADA_IP,
                    dbpassword=CONSOLIDADA_PASSWORD,
                    dbport=CONSOLIDADA_PORT,
                    username=user,
                    password=password,
                )