import sqlalchemy
import pandas
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("user", type=str,
        help="username to access postgresql database")
parser.add_argument("password", type=str,
        help="password to access postgresql database")
parser.add_argument("database", type=str,
        help="database name")
parser.add_argument("--host","-H", type=str,
        help="database host")
parser.add_argument("--port","-p", type=str,
        help="database port")
args = parser.parse_args()


def connect(user, password, db, host, port):
    url = 'postgresql://{}:{}@{}:{}/{}'
    url = url.format(user,password,host,port,db)
    con = sqlalchemy.create_engine(url)
    return con

user = args.user
password = args.password
db = args.database
host = "localhost"
if args.host is not None:
    host = args.host
port = 5432
if args.port is not one:
    port = args.port
con = connect(user,password,db,host,port)

limit = 1000

jams_db = pandas.read_sql("SELECT * FROM waze2.jams ORDER BY pub_millis,street;".
        format(limit),con,index_col=None)

road_types = pandas.read_sql("SELECT * FROM waze.roads;",con,index_col=None)

rt = {}
for i,row in road_types.iterrows():
    value = int(row['value'])
    name = row['name']
    rt[value] = name

def transform(n):
    return rt[n]

jams_db['road_type'] = jams_db['road_type'].apply(transform)

jams_db.to_csv("data/jams.csv",index=False)

