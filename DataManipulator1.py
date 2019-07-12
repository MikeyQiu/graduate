# -*- coding: utf-8 -*-

from py2neo import Graph
import json
import re


class Neo4jToJson(object):
    """知识图谱数据接口"""

    def __init__(self):
        """初始化数据"""
        # 与neo4j服务器建立连接
        self.graph = Graph("bolt://localhost:11011")
        self.links = []
        self.nodes = []

    def post(self):
        """与前端交互"""
        links_data = self.graph.run(
            'MATCH p=(source)-[r:Work_At]->(target) RETURN source.Name as source,target.Name as target '
            'UNION MATCH p=(source)-[r:GoIndustry]->(target) RETURN source.Name as source,target.Name as target '
            'UNION MATCH p=(source)-[r:Belong_to]->(target) RETURN source.Name as source,target.Name as target').data()
        nodes_data = self.graph.run(
            "match (n:GoWork) return n  UNION match (n:Company) return n UNION match (n:Industry) return n").data()
        self.get_all_nodes(nodes_data)

        # 数据格式转换
        neo4j_data = {'nodes': self.nodes, 'links': links_data}
        neo4j_data_json = json.dumps(neo4j_data, ensure_ascii=False).replace(u'\xa0', u'')
        return neo4j_data_json

    def get_links(self, links_data):
        """知识图谱关系数据获取"""
        links_data_str = str(links_data)
        links = []
        i = 1
        dict = {}
        # 正则匹配
        links_str = re.sub("[\!\%\[\]\,\。\{\}\-\:\'\(\)\>]", " ", links_data_str).split(' ')
        for link in links_str:
            if len(link) > 1:
                if i == 1:
                    dict['source'] = link
                elif i == 2:
                    dict['name'] = link
                elif i == 3:
                    dict['target'] = link
                    self.links.append(dict)
                    dict = {}
                    i = 0
                i += 1
        return self.links

    def get_all_nodes(self, nodes_data):
        """获取知识图谱中所有节点数据"""
        dict_node = {}
        for node in nodes_data:
            Name = node['n']['Name']
            tag = node['n']['tag']
            dict_node['id'] = Name
            dict_node['tag'] = tag
            dict_node['color'] = self.judge_tag_color(tag)
            dict_node['value'] = self.judge_tag_value(tag)
            self.nodes.append(dict_node)
            dict_node = {}
        return self.nodes

    def judge_tag_color(self, tag):
        """根据tag确定颜色"""
        if tag == "School" or tag == "GoWork" or tag == "GoStudy":
            return 3
        elif tag == "Nation":
            return 1
        elif tag == "Company":
            return 5
        elif tag == "ForeignSchool":
            return 0
        elif tag == "Industry":
            return 4
        elif tag == "Region":
            return 2

    def judge_tag_value(self, tag):
        """根据tag确定大小"""
        if tag == "School":
            return 18
        elif tag == "Region":
            return 12
        elif tag == "GoWork":
            return 10
        elif tag == "GoStudy":
            return 10
        elif tag == "Nation":
            return 9
        elif tag == "Company":
            return 6
        elif tag == "ForeignSchool":
            return 6
        elif tag == "Industry":
            return 9


if __name__ == '__main__':
    data_neo4j = Neo4jToJson()
    print(data_neo4j.post())
