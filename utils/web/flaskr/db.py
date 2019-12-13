import os

from py2neo import Graph

url = os.environ.get('http://localhost:7474')
username = os.environ.get('NEO4J_USERNAME')
password = os.environ.get('NEO4J_PASSWORD')

graph = Graph(url, username=username, password=password)
