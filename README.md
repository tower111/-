# 说明
给出一个目录生成目录下所有文件的函数调用链

现在还是只支持python，分析结果仅供参考

aaa.html文件为生成示例。

bug：对于import aaa as bbb这种导入还不能识别。

输出结果如图
![](images/2020-08-05-15-39-51.png)有更好的展示结果建议欢迎联系。362058670@qq.com

# 使用方式

修改get_image_from_file.py文件里的路径名。
```python
import show
if __name__=="__main__":
    file_list=scan_for_file("../Unsupervised-Features-Learning-For-Binary-Similarity/binary_similarity")
    all=init_struct.init_all_file_list(file_list)
```

运行
```python
python3 get_image_from_file.py
```
最好是把文件放到一个目录下，图上显示的路径会比较短