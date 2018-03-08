
from urllib import  request
import  re


class Spider ():
    url = 'https://www.panda.tv/cate/kingglory'
    data_deal_patten = '<div class="video-info">([\s\S]*?)</div>'
    name_refine_patten = '</i>([\s\S]*?)</span>'
    number_refine_patten = '<span class="video-number">([\s\S]*?)</span>'

    def __get_htmlData(self):

        '''

        该方法将全部的网页请求数据返回
        '''
        htmls = request.urlopen(Spider.url)

        data_origin = htmls.read()
        data_origin_str = str(data_origin , encoding='utf-8')
        return data_origin_str

    def __data_deal(self,data_str):

        '''

        该方法截取主播名称及人气所需要的部分内容
        '''
        data_str_source =  re.findall(Spider.data_deal_patten,data_str)
        return data_str_source

    def __data_refine(self,data_list):

        '''

        该方法将相应的主播名字及人气值通过字典列表返回
        '''
        data_refine_list = []
        for data in data_list:
            name =  re.findall(Spider.name_refine_patten,data)
            name_str = name[0]
            number = re.findall(Spider.number_refine_patten,data)
            number_str = number[0]
            data_dict = {'name':name_str.strip(),'number':number_str.strip()}
            data_refine_list.append(data_dict)
        return data_refine_list


    def __data_sort(self,data_list):

        '''

        该方法将字典列表中的数据排序返回
        '''
        list = sorted(data_list,key=self.__sort_seed,reverse=True)
        return list

    def __sort_seed(self,data_dict):

        '''

        该方法将字典中的人气按数量大小排序
        '''
        r = re.findall('\d*',data_dict['number'])
        number = float(r[0])
        if '万' in data_dict['number']:
            number *=10000

        return number


    def __show(self,data_list):
        '''

        该方法用于输出对应内容
        '''
        print('熊猫TV主播人气榜单排行')
        for data in  data_list:

            print('主播名称:'+data['name']+'      ' + '人气值:' + data['number'])

    def go(self):
        '''

        外部公共调用方法
        '''
        data_origin =  self.__get_htmlData()
        data_str_source = self.__data_deal(data_origin)
        data_list = self.__data_refine(data_str_source)
        data_list = self.__data_sort(data_list)
        self.__show(data_list)


spider = Spider ()
spider.go()