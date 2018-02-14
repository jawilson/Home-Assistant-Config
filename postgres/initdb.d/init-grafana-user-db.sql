CREATE USER grafana WITH PASSWORD 'graphallthethings';
CREATE DATABASE grafana;
ALTER DATABSE grafana OWNER TO grafana;
GRANT ALL PRIVILEGES ON DATABASE grafana TO grafana;
