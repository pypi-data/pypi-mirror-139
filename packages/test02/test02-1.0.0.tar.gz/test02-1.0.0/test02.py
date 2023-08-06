fa_movies = ["Test1","Test2",2022,["Test_Arr01","Test_Arr02","Test_Arr03"],"Test3"]

fa_movies.insert(3,"TestAdd1");
fa_movies.insert(4,"TestAdd2");
fa_movies.append("Test_tail");


for var_each in fa_movies:
    if isinstance(var_each,list):
        for child_each in var_each:
             print(child_each);
    else:
        print(var_each);

"""定义一个方法，递归查找展示列表数据"""
"""def print_cycle(var_list):
    if isinstance(var_list,list):
        for var in var_list:
            print_cycle(var);
    else:
        print(var_list);


print_cycle(fa_movies);"""


def print_cycle(var_list,level):
    for item in var_list:
        if isinstance(item,list):
            print_cycle(item,level+1);
        else:
            for tab_stop in range(level):
                print("\t",end='')
            print(item);
                      
print_cycle(fa_movies,0);                      
"""import sys;
print(sys.path);"""
