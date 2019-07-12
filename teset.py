from py2neo import Graph
import json
if __name__ == '__main__':
    # db = Database("bolt://localhost:11001")
    #graph=Graph(host="localhost")
    graph = Graph("bolt://localhost:11011")
    nodes=graph.run('MATCH (n) RETURN n').data()
    print(nodes)
    links = graph.run('MATCH p=(source)-[r]->(target) RETURN source.Name as source,target.Name as target').data()
    neo4j_data = {'nodes': nodes,'links': links,}
    neo4j_data_json = json.dumps(neo4j_data, ensure_ascii=False).replace(u'\xa0', u'')
    print((neo4j_data_json))
    # fw=open('../graduate/starwar2.json','w',encoding='utf-8')
    # fw.write(json.dumps(neo4j_data, ensure_ascii=False).replace(u'\xa0', u''))
    # fw.close()

