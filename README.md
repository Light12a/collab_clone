This is git for Collabos project
# Sync table to mysql
1. pip install alembic
2. alembic init alembic
3. alembic revision --autogenerate -m "your message"
4. alembic upgrade head

# Sync table of mysql to python object
sqlacodegen mysql://<username>:<password>@<host>:3306/backend --outfile db.py

