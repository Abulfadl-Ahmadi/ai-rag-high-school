#!/bin/bash
cat << 'EOF' > /etc/postgresql/16/main/pg_hba.conf
local   all             all                                     trust
host    all             all             127.0.0.1/32            trust
host    all             all             ::1/128                 trust
host    all             all             0.0.0.0/0               trust
host    all             all             ::/0                    trust
EOF

su - postgres -c "psql -c \"ALTER USER myuser WITH PASSWORD 'mypassword';\""
service postgresql restart
