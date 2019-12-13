docker-compose up -d --build
psql postgres < "./data/create.sql"
