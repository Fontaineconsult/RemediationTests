from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base



Base = declarative_base()


if __name__ == '__main__':

    from campus_resources_model import *
    from canvas_tracking_model import *

    psql_connection = "postgresql://postgres:accesslearning!1@130.212.104.18/amcrp_test"
    print(psql_connection)
    engine = create_engine(psql_connection,
                           connect_args={'options': '-csearch_path={}'.format("main"),
                                         'connect_timeout': 5,
                                         'application_name': "application"},
                           client_encoding='utf8',
                           pool_size=50,
                           max_overflow=10,
                           pool_recycle=300,
                           pool_pre_ping=True,
                           pool_use_lifo=True
                           )
    Base.metadata.create_all(engine)
    DBsession = sessionmaker(bind=engine)
