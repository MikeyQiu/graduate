# -*- coding: utf-8 -*-

from py2neo import Graph
import json
import re


class Neo4jToJson3(object):
    """知识图谱数据接口"""

    def __init__(self):
        """初始化数据"""
        # 与neo4j服务器建立连接
        self.graph = Graph("bolt://localhost:11011")
        self.links = []
        self.nodes = []

    def post(self):
        """与前端交互"""
        nodes_data = self.graph.run("match (n:School) return n.Name as SchoolName, n.under as under,n.post as post,n.doc as doc order by n.Graduate").data()
        neo4j_data= {"result":nodes_data}
        neo4j_data_json = json.dumps(neo4j_data, ensure_ascii=False).replace(u'\xa0', u'')
        return neo4j_data_json





if __name__ == '__main__':
    data_neo4j = Neo4jToJson3()
    print(data_neo4j.post())