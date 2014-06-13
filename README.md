Two-phase Commit
===================

# Dependências

    sudo apt-get install python3-psycopg2
    
# Postgres

      postgres=# CREATE DATABASE two_face_commit;

      postgres=# \c two_face_commit
    
      CREATE TABLE conta (
          cd_conta SERIAL,
          vl_saldo NUMERIC NOT NULL DEFAULT 0
      );
      
      
# Executar

      python3.3 cliente.py
      python3.3 participante.py
