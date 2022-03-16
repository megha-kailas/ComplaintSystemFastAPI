import databases
import sqlalchemy

DATABASE_URL = "sqlite:///./complaints.db"

database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()
