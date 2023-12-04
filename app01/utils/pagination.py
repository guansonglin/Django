"""
自定义的分页组件，以后如果想要使用这个分页组件，你需要做如下几件事：

在视图函数中：
    def pretty_list(request):

        # 1.根据自己的情况去筛选自己的数据
        queryset = models.PrettyNum.objects.all()

        # 2.实例化分页对象
        page_object = Pagination(request, queryset)

        context = {
            "queryset": page_object.page_queryset,  # 分完页的数据
            "page_string": page_object.html(),       # 生成页码
            "error" :  page_object.error            #搜索框的错误
        }
        return render(request, 'pretty_list.html', context)

在HTML页面中

    {% for obj in queryset %}
        {{obj.xx}}
    {% endfor %}

    <ul class="pagination">
        {{ page_string }}
    </ul>
    <span><a style="color: red;">{{ error }}</a></span>

"""


from django.utils.safestring import mark_safe
        

import copy

class Pagination(object):
    def __init__(self,request,queryset,page_data = 10,page_param = "page" , con =4):

        get_object  = copy.deepcopy(request.GET) #获取get请求的中的数据 后面进行判断是否正确
        # print("get_object:",get_object)
        get_object._mutable = True
        self.get_object = get_object
        
        page = request.GET.get(page_param,"1")
        if page.isdecimal():
            page = int(page)
        else:
            page = 1

        # 拿出数据库中的所有数据个数 <class 'int'> int型  算出所需要的页数
        self.amount_data = queryset.count()
        all_page,div = divmod(self.amount_data,page_data)
        if div:
            all_page = all_page + 1   
        self.all_page = all_page

        # 判断页面搜索框是否输入符合的值
        if page > all_page:
            self.error = "超过最大页数{}".format(all_page)
            page = all_page
        elif page < 1:
            self.error = "输入不能小于1"
            page = 1
        else:
            self.error = ''


        self.page = page
        self.page_data = page_data

        self.star_data = (page-1) * page_data
        self.end_data = page * page_data

        self.page_queryset = queryset[self.star_data:self.end_data]
        



        self.con = con


    # 分页的html
    def html(self):
        if self.page <= self.con and self.all_page >= 2*self.con:
            star_num_page = 1
            end_num_page = 2*self.con
        elif self.page >= (self.all_page - self.con) and self.all_page >= 2*self.con:
            star_num_page = self.all_page -2*self.con
            end_num_page = self.all_page
        elif self.all_page < 2*self.con:
            star_num_page = 1
            end_num_page = self.all_page
        else:
            star_num_page = self.page - self.con
            end_num_page = self.page + self.con
        

        #页码
        page_str_list = []
        self.get_object.setlist('page',[1])
        ele = '<li><a href="?{}" aria-label="Next"><span aria-hidden="true">首页</span></a></li>'.format(self.get_object.urlencode()) 
        page_str_list.append(ele)
        if self.page == 1:
            self.get_object.setlist('page',[1])            
            sls = '<li><a href="?{}" aria-label="Next"><span aria-hidden="true">上一页</span></a></li>'.format(self.get_object.urlencode())
        else:
            self.get_object.setlist('page',[self.page - 1]) 
            sls = '<li><a href="?{}" aria-label="Next"><span aria-hidden="true">上一页</span></a></li>'.format(self.get_object.urlencode())

        page_str_list.append(sls)

        for i in range(star_num_page,end_num_page+1):
            self.get_object.setlist('page',[i])
            if self.page == i:
                ele = '<li class="active"><a href="?{}">{}</a></li>'.format(self.get_object.urlencode(),i)
            else:
                ele = '<li><a href="?{}">{}</a></li>'.format(self.get_object.urlencode(),i)
            page_str_list.append(ele)

        if self.page == self.all_page:
            self.get_object.setlist('page',[self.page])
            sls = '<li><a href="?{}" aria-label="Next"><span aria-hidden="true">下一页</span></a></li>'.format(self.get_object.urlencode())
        else:
            self.get_object.setlist('page',[self.page+1])
            sls = '<li><a href="?{}" aria-label="Next"><span aria-hidden="true">下一页</span></a></li>'.format(self.get_object.urlencode())
        page_str_list.append(sls)
        self.get_object.setlist('page',[self.all_page])
        ele = '<li><a href="?page={}" aria-label="Next"><span aria-hidden="true">尾页</span></a></li>'.format(self.get_object.urlencode())
        page_str_list.append(ele)




        search_string = """
                <li>
                    <form style="float: left;margin-left: -1px" method="get">
                        <input name="page"
                            style="position: relative;float:left;display: inline-block;width: 80px;border-radius: 0;"
                            type="text" class="form-control" placeholder="页码">
                        <button style="border-radius: 0" class="btn btn-default" type="submit">跳转</button>
                    </form>
                </li>
                """
        page_str_list.append(search_string)
        page_string = mark_safe("".join(page_str_list))

        return page_string

        


