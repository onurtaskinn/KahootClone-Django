Make sure that database settings are correct.

    brew services stop postgresql@14
    brew services start postgresql@14

    psql postgres

        check if the following database exists :-> 
        psi       | onurtaskin | UTF8     | C       | C     | =Tc/onurtaskin           +
                  |            |          |         |       | onurtaskin=CTc/onurtaskin+

        if doesnt exist => 
            CREATE DATABASE psi;
            CREATE USER alumnodb WITH PASSWORD 'alumnodb';
            ALTER ROLE alumnodb SET client_encoding TO 'utf8';
            ALTER ROLE alumnodb SET default_transaction_isolation TO 'read committed';
            ALTER ROLE alumnodb SET timezone TO 'UTC';
            GRANT ALL PRIVILEGES ON DATABASE psi TO alumnodb;                  


    TESTING = exist => in .env file

    chmod +x build.sh

    python3 manage.py runserver






