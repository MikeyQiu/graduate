# coding=utf-8
from flask import Flask,jsonify,render_template,url_for,redirect,request
from py2neo import Graph
from flask_bootstrap import Bootstrap
import json
from DataManipulator1 import Neo4jToJson
from DataManipulator1_2 import Neo4jToJson1_2
from DataManipulator1_3 import Neo4jToJson1_3
from DataManipulator2 import Neo4jToJson2
from DataManipulator3 import Neo4jToJson3
from DataManipulator4 import Neo4jToJson4

app = Flask(__name__)
#使用bolt连接Neo4j数据库
graph = Graph("bolt://localhost:11011")
Bootstrap(app)

@app.route('/')
#启动路径
def index():
    return render_template('home.html')

@app.route('/work_graph')
def work_graph():
    return render_template('index1_1work_graph.html')

@app.route('/study_graph')
def study_graph():
    return render_template('index2_1study_graph.html')

@app.route('/school_graph')
def school_graph():
    return render_template('index3_1school_graph.html')

@app.route('/get_scale',methods=['GET','POST'])
def get_scale():
    return render_template('index3_2graduates.html')
    # if request.method=="GET":
    #     request.args.values()
    # else:
    #     #写KEY,写form action=post
    #     request.form.get()


@app.route('/get_study')
def get_study():
    return render_template('index3_3graduateGo.html')

@app.route('/get_industry')
def get_industry():
    return render_template('index1_3industry.html')

@app.route('/get_company')
def get_company():
    return render_template('index1_2company.html')

@app.route('/get_nation')
def get_nation():
    return render_template('index2_3nation.html')

@app.route('/get_school')
def get_school():
    return render_template('index2_2foreignScool.html')

@app.route('/get_local')
def get_local():
    return render_template('index3_4local.html')

@app.route('/graph')
def get_graph():
    neo4jtoJson=Neo4jToJson()
    return neo4jtoJson.post()

@app.route('/graph1_2')
def get_graph1_2():
    neo4jtoJson=Neo4jToJson1_2()
    return neo4jtoJson.post()

@app.route('/graph1_3')
def get_graph1_3():
    neo4jtoJson=Neo4jToJson1_3()
    return neo4jtoJson.post()

@app.route('/allInfo')
def get_graph2():
    neo4jtoJson = Neo4jToJson2()
    return neo4jtoJson.post()

@app.route('/graduateScale')
def get_statics1():
    neo4jtoJson=Neo4jToJson3()
    return neo4jtoJson.post()


@app.route('/studyRate')
def get_statics2():
    nodes_data =graph.run(
        "match (n:GoStudy) return n.Name as SchoolName, n.goStudyRate  as goStudyRate,n.studyDomesticRate as studyDomesticRate,n.studyAbroadRate as studyAbroadRate order by goStudyRate").data()
    neo4j_data = {"result": nodes_data}
    neo4j_data_json = json.dumps(neo4j_data, ensure_ascii=False).replace(u'\xa0', u'')
    return neo4j_data_json

@app.route('/companyNumber')
def get_statics3():
    nodes_data =graph.run(
        "MATCH (gs:GoWork)-[r]->(c:Company) return c.Name as companyName,sum(toInt(r.Amount))as amount order by amount DESC Limit 25").data()
    neo4j_data = {"result": nodes_data}
    neo4j_data_json = json.dumps(neo4j_data, ensure_ascii=False).replace(u'\xa0', u'')
    return neo4j_data_json

@app.route('/schoolNumber')
def get_statics4():
    nodes_data =graph.run(
        "MATCH (gs:GoStudy)-[r]->(c:ForeignSchool) return c.Name as schoolName,sum(toInt(r.Amount))as amount order by amount DESC Limit 25").data()
    neo4j_data = {"result": nodes_data}
    neo4j_data_json = json.dumps(neo4j_data, ensure_ascii=False).replace(u'\xa0', u'')
    return neo4j_data_json

@app.route('/graduateNumber')
def get_statics5():
    neo4jtoJson=Neo4jToJson4()
    return neo4jtoJson.post()

@app.route('/nationNumber')
def get_statics6():
    nodes_data =graph.run(
        "MATCH (gs:GoStudy)-[r]->(n:Nation) return n.Name as nationName,sum(toInt(r.Amount))as amount order by amount DESC Limit 20").data()
    neo4j_data = {"result": nodes_data}
    neo4j_data_json = json.dumps(neo4j_data, ensure_ascii=False).replace(u'\xa0', u'')
    return neo4j_data_json

@app.route('/industryRate')
def get_statics7():
    nodes_data =graph.run(
        "MATCH (gs:GoWork)-[r]->(ind:Industry) return ind.Name as industryName,avg(toFloat(r.IndustryRate))as industryRate order by industryRate DESC Limit 20").data()
    neo4j_data = {"result": nodes_data}
    neo4j_data_json = json.dumps(neo4j_data, ensure_ascii=False).replace(u'\xa0', u'')
    return neo4j_data_json

@app.route('/localRate')
def get_statics8():
    nodes_data =graph.run(
        "MATCH (gs:GoWork)-[r]->(re:Region) return re.Name as regionName,avg(toFloat(r.workLocalRate))as workLocalRate order by workLocalRate DESC Limit 20").data()
    neo4j_data = {"result": nodes_data}
    neo4j_data_json = json.dumps(neo4j_data, ensure_ascii=False).replace(u'\xa0', u'')
    return neo4j_data_json



if __name__ == '__main__':
    app.run(debug = True)


