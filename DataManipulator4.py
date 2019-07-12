# -*- coding: utf-8 -*-

from py2neo import Graph
import json
import re


class Neo4jToJson4(object):
    """知识图谱数据接口"""

    def __init__(self):
        """初始化数据"""
        # 与neo4j服务器建立连接
        self.graph = Graph("bolt://localhost:11011")
        self.links = []
        self.nodes = []

    def post(self):
        """与前端交互"""
        nodes_data1 = self.graph.run("match (n1:School)-[:Go_Study]->(n2:GoStudy) return n1.Name as schoolName,n1.Graduate as graduates,n1.workRate as workRate,n2.studyDomestic as studyDomestic,n2.studyAbroad as studyAbroad order by n1.Name").data()
        nodes_data2 = self.graph.run(
            "match (n3:School)-[:Go_Work]->(n4:GoWork) return n4.Name as SchoolName,n3.Graduate as graduates,n4.gowork as goWork order by SchoolName").data()
        neo4j_data= {"result1":nodes_data1,"result2":nodes_data2}
        neo4j_data_json = json.dumps(neo4j_data, ensure_ascii=False).replace(u'\xa0', u'')
        return neo4j_data_json





if __name__ == '__main__':
    data_neo4j = Neo4jToJson4()
    print(data_neo4j.post())