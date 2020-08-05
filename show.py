from networkx import nx
import sys
from pyecharts import options as opts
from pyecharts.charts import Graph
from networkx.readwrite import json_graph

def graph_node(all):
    function_graph = nx.DiGraph() #创建一个图,函数调用图
    file_graph=nx.DiGraph() #文件调用图
    class_graph=nx.DiGraph()
    all_function_graph=nx.DiGraph()#多余的,方便输出
    for filename in all.keys():
        # print(filename)
        # file_graph.add_node(filename,name=filename,class_graph=class_graph,isfunc=0)
        for classname in all[filename].keys():
            # class_graph.add_node(filename+classname,name=classname,function_graph=function_graph)
            for funcname in all[filename][classname]:
                all_function_graph.add_node(filename + ":-:" + classname+ ":-:" + funcname.split(":-:")[0],#这里添加\n方便显示
                                            name=filename + ":-\n:" + classname + ":-\n:" + funcname.split(":-:")[0]) #删掉.split(":-:")[0]可以显示具体内容
                # if "def:-:" in funcname:
                #     class_graph.node[filename+classname]["isfunc"]=1
                # else:
                #     function_graph.add_node(filename+classname+funcname.split(":-:")[0],name=funcname.split(":-:")[0])
    return all_function_graph
    #图的顶点id是字符串直接相加
def is_class(content,c_file,c_class):#content是函数的内容由.分割出来的列表的一个元素
    #从内容中得到最后一个字符，判断是不是类
    aa=content.strip().split(" ")#空格分割

    for filename,class_name in zip(c_file,c_class):
        if aa[-1].strip() ==class_name.replace("class ",""):#找到返回类名,只是检查类名，不包含不同文件相同类的情况
            return class_name
    if "self"==aa[-1].strip():#前面是self
        return "self"
    return ""


def get_function_class(all_function_graph,content_from,content,funcname_list,class_list):#这里只处理得到一个类名
    #content_from是content来自的filename + ":-\n:" + classname + ":-\n:" + funcname.split(":-:")[0]  'def:-:\ntf.disable_v2_behavior()\nmatplotlib.use(\'Agg\')'
    #一个函数的内容，所有函数的列表，所有类的列表
    #funcname_list= '../Unsupervised-Features-Learning-For-Binary-Similarity/binary_similarity/s2v_trainer.py:-:S2VTrainer:-:S2VTrainer'#这里是处理过的函数名
    #class_list='../Unsupervised-Features-Learning-For-Binary-Similarity/binary_similarity/s2v_trainer.py:-:S2VTrainer'#里面只包含类名，不包含函数名
    content=content.strip()#先处理函数内容
    list_from_point_s=content.split(" ")
    list_from_point=[]
    for item in list_from_point_s:
        for y_ in item.split("\n"):
            for point_ in y_.split("."):
                if point_.strip()=="":
                    continue
                list_from_point.append(point_.strip())#按空格和换行切割切割数据，然后去掉空的元素，去掉前后的空
    print(list_from_point[0])
    f1=[]
    f2=[]
    f3=[]
    for item in funcname_list:
        f1.append(item.split(":-:")[0])
        f2.append(item.split(":-:")[1])
        f3.append(item.split(":-:")[2])

    c1=[]
    c2=[]
    for item in class_list:
        c1.append(item.split(":-:")[0])
        c2.append(item.split(":-:")[1])

    if content_from.split(":-:")[1]=="main":
        aa=0
    for list_from_point_index in range(1,len(list_from_point),1):#0一定是函数名或类名
        if "(" in list_from_point[list_from_point_index]:#初步判断这一段里面有函数,这里不考虑使用函数时函数名和括号中间有空格 func ()
            for filename_f ,classname_f,funcname_f in zip(f1,f2,f3):#对于import aaa as bbb这种不能扫描到
                if funcname_f =="def":#让funcname始终是某个函数名
                    funcname=classname_f
                else:
                    funcname=funcname_f
                if  funcname+"(" in list_from_point[list_from_point_index]:#找到函数

                    #需要开始寻找类

                    last_is_class=is_class(list_from_point[list_from_point_index - 1],c1,c2 )

                    if last_is_class!="" :#这个函数前面是一个类
                        if last_is_class=="self":#处理self，
                            if "def:-:" in content_from :#这里不考虑定义类和使用类没在同一个文件，作为函数参数传进去的self  如trainer.train(self)
                                continue
                            else:
                                class_name=content_from.split(":-:")[1]#得到类名

                                ss=filename_f + ":-:"+classname_f + ":-:"+funcname_f
                                all_function_graph.add_edge(content_from, filename_f + ":-:"+classname_f + ":-:"+funcname_f)

                        else:#是某个函数的类
                            all_function_graph.add_edge(content_from, filename_f +":-:"+ last_is_class +":-:"+ funcname_f)
                    else:#是某个单独的函数（前面没
                        all_function_graph.add_edge(content_from, filename_f +":-:"+ classname_f +":-:"+ funcname_f)

                    # if
                    #
                    # for filename_c, classname in c:
                    #     if list_from_point_index>0 and classname in list_from_point[list_from_point_index-1] and filename_c==filename_f: #前面是个类名
                    #         all_function_graph.add_edge(content_from,filename_f+classname+funcname)

                        # if classname_f.replace("def ","")==funcname:#类下的函数和非类下的函数
                        #     all_function_graph.add_edge(content_from, filename_f +":-:"+ classname_f +":-:"+ "def")
                        # else:#不是一个函数
                        #     all_function_graph.add_edge(content_from, filename_f + classname_f +funcname)
    return all_function_graph







def graph_edge(all,all_function_graph):
    funcname_list=[]
    class_list=[]
    # class_list列表里面是所有类的名字，不包括函数名
    #funcname_list包含所有函数的名字
    for filename in all.keys():
        for classname in all[filename].keys():
            for funcname in all[filename][classname]:
                # aa=""
                # if  "def:-:" in funcname :
                #     aa=classname
                # else:
                #     aa=funcname
                if filename + ":-:" + classname in class_list:
                    pass
                else:
                    class_list.append(filename + ":-:" + classname)
                funcname_list.append(filename + ":-:" + classname + ":-:" + funcname.split(":-:")[0])
                #     funcname_list.append(classname)
                # else:
                #     funcname_list.append(funcname)
    for filename in all.keys():  # 不同文件里面相同的函数名也会被识别
        for classname in all[filename].keys():
            for funcname_content in all[filename][classname]:#某个函数下的内容
                all_function_graph = get_function_class(all_function_graph,filename + ":-:" + classname + ":-:" + funcname_content.split(":-:")[0],
                                                        funcname_content,funcname_list,class_list)

    return all_function_graph,funcname_list
def show_graph(function_graph,savename):
    guolv=0



    g_data = json_graph.node_link_data(function_graph)
    eg = Graph(init_opts=opts.InitOpts(width="1400px", height="800px"))
    eg.add('Devices', nodes=g_data['nodes'], links=g_data['links'], repulsion=3000, edge_symbol=['circle', 'arrow'],
           symbol_size=5, edge_symbol_size=5)
    eg.set_global_opts(title_opts=opts.TitleOpts(title="Graph-基本示例"))
    eg.render(savename+".html")
    eg

def show_sub_graph(function_graph,funcname_list):
    print(funcname_list)
    id=[]
    guolv_func_name = "Network"
    for func_id in funcname_list.keys():
        if guolv_func_name == funcname_list[func_id].split(":-\n:")[1].replace("def","").strip() \
            or guolv_func_name == funcname_list[func_id].split(":-\n:")[2].replace("def","").strip():
            id.append(func_id)

    if len(id) == 0:
        return

    for c in nx.weakly_connected_components(function_graph):
        for func_id in id:
            if func_id in c:
                sub_graph = function_graph.subgraph(c)
                show_graph(sub_graph,str(func_id))
    #     if guolv_func_name in c:
    #         sub[i]=c
    #         i+=1
    # for item in sub.keys():
    #     sub_graph = function_graph.subgraph(sub[item])
    #     show_graph(sub_graph)




