Two-phase Commit
===================

# Dependências

    sudo apt-get install python3-psycopg2
    sudo apt-get install docker.io
    
# Postgres

      postgres=# CREATE DATABASE two_phase_commit;

      postgres=# \c two_phase_commit
    
      CREATE TABLE conta (
          cd_conta SERIAL,
          vl_saldo NUMERIC NOT NULL DEFAULT 0
      );
      
      
# Executar localmente

      python3.3 cliente.py
      python3.3 participante.py
