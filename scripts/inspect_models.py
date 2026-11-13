from sqlalchemy.dialects import postgresql
from sqlalchemy.schema import CreateTable

from app.db.base import Base
from app.models.post import Post


def main():

    print("ORM class:", Post)
    print("Model Base:", Post.__bases__)
    print("Registered tables:", list(Base.metadata.tables.keys()))

    table = Base.metadata.tables["posts"]

    sql = CreateTable(table).compile(dialect=postgresql.dialect())

    print("\nSQL generated:")
    print(sql)


if __name__ == "__main__":
    main()
