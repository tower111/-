import os
import time
import init_struct


def scan_for_file( start):#扫描一个目录里面包含某个字符的所有文件，返回文件目录+文件名
    file_list = []
    # Scan recursively all the subdirectory
    directories = os.listdir(start)
    for item in directories:
        item = os.path.join(start, item)
        if os.path.isdir(item):
            file_list.extend(scan_for_file(item + os.sep))
        elif os.path.isfile(item) and item.endswith('.py'):
            file_list.append(item)
    return file_list

def find_all(a_str, sub): #返回一个列表，列表包含一个文件中包含某个字符串的所有位置
    #a_str是被扫描字符串, sub需要识别的字符串
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1: return
        yield start
        start += len(sub) # use start += 1 to find overlapping matches

def is_main(content):#对main函数进一步判断
    list_f=["def","class","from","import"]
    for item in list_f:
        if item in content[0:6]:
            return 0
        else:
            if content[0]=="\t" or content[0]==" ":
                return 0
            else:
                if "__main__" in content:#如果是手动定义的main函数返回1
                    return 1
                else:#没有明确定义的main返回2
                    return 2


#获取文件信息
# all{文件名1{类名1:【函数名1，函数名2......】，类名2...文件下的函数名1[def]，文件下的函数名2...}，文件名2...}
#不足:没有定义main函数的不能识别，必须要main函数显示定义
def get_func(file_content,file_name,all): #获取所有的函数信息

    filecontent_list=file_content.split("\n")
    last_class_key=""
    last_func_name = ""
    for  filecontent_line in filecontent_list:
        file_content_line=""
        if "import " in filecontent_line or "from" in filecontent_line:#对import处理
            continue
        for item in  filecontent_line:#对#处理
            if item == "#":
                break
            file_content_line+=item
        filecontent_line=file_content_line
        if filecontent_line == " "or filecontent_line.strip()=="" :
            continue
        # print(filecontent_line)


        if "class" in filecontent_line[0:5]:
            class_index=filecontent_line.find("class ")#放进去类，不包含class，不包含(和参数,前面后面不包含空格
            kuohao_index = filecontent_line.find("(")
            if kuohao_index == -1:
                kuohao_index=filecontent_line.find(":")
            all[file_name][filecontent_line[class_index+len("class "):kuohao_index].strip()] = [] # 找到文件下的函数
            last_class_key=filecontent_line[class_index+len("class "):kuohao_index].strip()
        elif "def" in  filecontent_line.strip()[0:3]:#定位def
            def_index=filecontent_line.find("def ")
            if def_index ==0:
                kuohao_index=filecontent_line.find("(")
                if kuohao_index==-1:
                    continue
                all[file_name][filecontent_line[def_index+len("def ") :kuohao_index].strip()]=["def:-:"] #找到文件下的函数
                last_func_name=file_name+":-:"+filecontent_line[def_index+len("def ") :kuohao_index].strip()+":-:"+"def:-:" #
            else:#如果def开头有tab认为是类下的函数
                # print("aaaa"+all[file_name][last_class_key])
                kuohao_index = filecontent_line.find("(")
                if kuohao_index==-1:
                    continue
                if last_class_key=="":
                    continue
                all[file_name][last_class_key].append(filecontent_line[def_index+len("def "):kuohao_index].
                                                      replace("__init__",last_class_key).replace("class ","").strip()+":-:")#把__init__函数替换为类名字
                last_func_name = file_name+":-:"+last_class_key+":-:"+filecontent_line[def_index+len("def "):kuohao_index].replace("__init__",last_class_key).\
                    replace("class ","").strip()+":-:"#更新最后一个函数的
        else :
            if is_main(filecontent_line)!=0:#如果main函数是手动定义的

                if "main" in all[file_name].keys():#如果main函数已经定义
                    pass
                else:
                    all[file_name]["main"] = ["def:-:"]
                last_func_name = file_name + ":-:" + "main" + ":-:" + "def"
            #处理不带函数名的函数内容行
            if last_func_name !="":
                current_class_name=last_func_name.split(":-:")[1]
                current_func_name = last_func_name.split(":-:")[2]
                for i in range(len(all[file_name][current_class_name])):
                    if all[file_name][current_class_name][i].split(":-:")[0]==current_func_name:
                        all[file_name][current_class_name][i]+="\n"+filecontent_line

    return all




    # return func_name_list,func_content_list


"""
main_list=list(find_all(file_content, "if __name__ == '__main__'"))
        class_list=list(find_all(file_content, 'class '))
        """
#测试函数




import show
if __name__=="__main__":
    file_list=scan_for_file("../Unsupervised-Features-Learning-For-Binary-Similarity/binary_similarity")
    all=init_struct.init_all_file_list(file_list)
    # print(file_list)

    for file_name in file_list:
        # print(file_name)
        f1 = open(file_name, "r")  # ,encoding='utf-8')#,encoding='ISO-8859-1')
        file_content = f1.read()
        f1.close()
        all=get_func(file_content,file_name,all)  # 获取定义的函数和它的内容  func_name_content{定义的函数名：函数对应的内容}

    all_function_graph= show.graph_node(all)
    all_function_graph,funcname_list=show.graph_edge(all,all_function_graph)
    show.show_graph(all_function_graph,"aaa")
        # show.show_sub_graph(all_function_graph,funcname_list)
        # print(all_function_graph)
    print(all)