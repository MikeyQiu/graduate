# -*- coding: utf-8 -*-

from collections import defaultdict
from py2neo import Graph
import json
import re


class Neo4jToJson2(object):
    """知识图谱数据接口"""

    def __init__(self):
        """初始化数据"""
        # 与neo4j服务器建立连接
        self.graph = Graph("bolt://localhost:11011")
        self.links = []
        self.nodes = []

    def post(self):
        """与前端交互"""
        links_data = self.graph.run("MATCH p=(source)-[r]->(target) RETURN source.Name as source,target.Name as target").data()
        #print(links_data)
        nodes_data = self.graph.run("MATCH (n) RETURN n").data()
        industry_data = self.graph.run("MATCH (gs:GoWork)-[r]->(ind:Industry) "
                                       "return ind.Name as industryName,avg(toFloat(r.IndustryRate))as industryRate").data()
        nation_data=self.graph.run("MATCH(gs: GoStudy)-[r]->(n:Nation) return n.Name as nationName, sum(toInt(r.Amount))as amount").data()
        foreign_data=self.graph.run("MATCH (gs:GoStudy)-[r]->(c:ForeignSchool) return c.Name as schoolName,sum(toInt(r.Amount))as amount").data()
        company_data=self.graph.run("MATCH (gs:GoWork)-[r]->(c:Company) return c.Name as companyName,sum(toInt(r.Amount))as amount").data()
        self.get_all_nodes(nodes_data,industry_data,nation_data,foreign_data,company_data)


        # 数据格式转换
        neo4j_data=self.nodes
        temp="{"
        for i in neo4j_data:
            #print(i["id"]+str(i))
            temp+="\'"+i["id"]+"\'"+":"+str(i)+","
        temp=temp[:-1]
        temp+="}"
        temp2=temp.replace('\'','"')
        return (temp2)

    def get_links(self, links_data):
        """知识图谱关系数据获取"""
        links_data_str = str(links_data)
        links = []
        i = 1
        dict = {}
        # 正则匹配
        links_str = re.sub("[\!\%\[\]\,\。\{\}\-\:\"\(\)\>]", " ", links_data_str).split(" ")
        for link in links_str:
            if len(link) > 1:
                if i == 1:
                    dict["source"] = link
                elif i == 2:
                    dict["name"] = link
                elif i == 3:
                    dict["target"] = link
                    self.links.append(dict)
                    dict = {}
                    i = 0
                i += 1
        return self.links

    def get_all_nodes(self, nodes_data,industry_data,nation_data,foreign_data,company_data):
        """获取知识图谱中所有节点数据"""
        result={}
        dict_node = {}
        for node in nodes_data:
            dict_Node={}
            Name = node["n"]["Name"]
            tag = node["n"]["tag"]
            if tag=="School":
                node["n"]["workRate"]=str(float(node["n"]["workRate"])*100)[:5]+"%"
                dict_node["毕业生人数"]= node["n"]["Graduate"]
                dict_node["博士生人数"] = node["n"]["doc"]
                dict_node["硕士生人数"] = node["n"]["post"]
                dict_node["本科生人数"] = node["n"]["under"]
                #dict_node["其他"]= node["n"]["Others"]
                dict_node["就业率"] = node["n"]["workRate"]
            elif tag=="GoWork":
                node["n"]["goWorkRate"]=str(float(node["n"]["goWorkRate"])*100)[:5]+"%"
                dict_node["毕业生工作人数"] = node["n"]["gowork"]
                dict_node["毕业生工作率"] = node["n"]["goWorkRate"]
            elif tag=="GoStudy":
                node["n"]["goStudyRate"] = str(float(node["n"]["goStudyRate"]) * 100)[:5] + "%"
                node["n"]["studyAbroadRate"] = str(float(node["n"]["studyAbroadRate"]) * 100)[:5] + "%"
                node["n"]["studyDomesticRate"] = str(float(node["n"]["studyDomesticRate"]) * 100)[:5] + "%"
                dict_node["毕业生升学人数"] = node["n"]["goStudy"]
                dict_node["毕业生升学率"] = node["n"]["goStudyRate"]
                dict_node["毕业生境外升学人数"] = node["n"]["studyAbroad"]
                dict_node["毕业生境外升学率"] = node["n"]["studyAbroadRate"]
                dict_node["毕业生境内升学人数"] = node["n"]["studyDomestic"]
                dict_node["毕业生境内升学率"] = node["n"]["studyDomesticRate"]
            elif tag=="Company":
                dict_node["企业性质"] = node["n"]["sector"]
                dict_node["所处行业"] = node["n"]["field"]
                for cmp in company_data:
                    if Name==cmp["companyName"]:
                        dict_node["应届生工作人数"] =cmp["amount"]
            elif tag=="Industry":
                for ind in industry_data:
                    if Name==ind["industryName"]:
                        ind["industryRate"]=str(float(ind["industryRate"]) * 100)[:4] + "%"
                        dict_node["毕业生就业比例"] =ind["industryRate"]
            elif tag=="Nation":
                for nat in nation_data:
                    if Name==nat["nationName"]:
                        dict_node["出境国家人数"] =nat["amount"]
            elif tag=="ForeignSchool":
                for fs in foreign_data:
                    if Name==fs["schoolName"]:
                        dict_node["留学人数"] =fs["amount"]

            dict_node["id"] = Name
            dict_node["tag"] = tag
            dict_Node[Name] = (dict_node)
            # temp=("\""+Name+"\""+":" +(dict_node)).replace("\'", "")
            #print(temp)
            # temp_data= {Name: dict_Node}
            # print(temp_data)
            self.nodes.append(dict_Node[Name])
            dict_node = {}
        return self.nodes


if __name__ == "__main__":
    data_neo4j = Neo4jToJson2()
    print(data_neo4j.post())