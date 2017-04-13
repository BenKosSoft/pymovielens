from neo4j.v1 import GraphDatabase

uri = "bolt://localhost"
auth_token = ("neo4j", "123456")
driver = GraphDatabase.driver(uri, auth=auth_token)
session = driver.session()
