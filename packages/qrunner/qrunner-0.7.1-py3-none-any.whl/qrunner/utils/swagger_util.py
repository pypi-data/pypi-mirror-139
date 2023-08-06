# @Time    : 2022/2/11 9:00
# @Author  : kang.yang@qizhidao.com
# @File    : swagger.py
import sys

import requests
import urllib3
urllib3.disable_warnings()


def get_api_list(swagger_url):
    """
    通过swagger接口获取接口列表
    @param swagger_url:
    @return: [
        ['请求方法', '项目名', '接口所属子模块', '接口描述', '接口路径'],
        ...
    ]
    """
    # 请求url，获取返回的json
    res = requests.get(swagger_url, verify=False)
    # print(res.text)
    data_json: dict = res.json()
    # print(data_json)
    # 获取接口所属模块
    module: str = data_json.get('basePath')
    module = module.split('/')[1]
    # 获取tag名称和描述的映射关系
    tags = data_json.get('tags')
    tag_dict = {}
    for tag in tags:
        name = tag.get('name')
        des = tag.get('description')
        if name not in tag_dict:
            tag_dict[name] = des
    # print(tag_dict)
    # 获取接口信息
    paths = data_json.get('paths')
    api_list = []
    for path, value in paths.items():
        for method, content in value.items():
            tag = content['tags'][0]
            tag_name: str = tag_dict[tag]
            tag_name = tag_name.replace("'", "")
            tag_name = tag_name.replace('"', '')
            summary: str = content['summary']
            summary = summary.replace("'", "")
            summary = summary.replace('"', '')
            api_list.append([module, tag_name, summary, path])
    for index, api in enumerate(api_list):
        print(index, api)
    return api_list


if __name__ == '__main__':
    from mysql_util import ApiDB

    # url = 'https://www-test.qizhidao.com/api/qzd-bff-boss/v2/api-docs'
    # api_list = get_api_list(url)
    # for api in api_list:
    #     ApiDB().write_swagger(api)

    # 32个项目，获取每个项目的接口，写入数据库
    # urls = [
    #     'http://app-test.qizhidao.com/confuse/v2/api-docs',
    #     'http://app-test-lan.qizhidao.com/im-base/v2/api-docs',
    #     'http://app-test-lan.qizhidao.com/qzd-analysis/v2/api-docs',
    #     'http://app-test-lan.qizhidao.com/qzd-base-service/v2/api-docs',
    #     'http://app-test-lan.qizhidao.com/qzd-bff-app/v2/api-docs?group=企知道',
    #     'http://app-test-lan.qizhidao.com/qzd-bff-boss/v2/api-docs',
    #     'http://app-test-lan.qizhidao.com/qzd-bff-emp/v2/api-docs',
    #     'http://app-test-lan.qizhidao.com/qzd-bff-enterprise/v2/api-docs?group=企知道',
    #     'http://app-test-lan.qizhidao.com/qzd-bff-gcenter/v2/api-docs',
    #     'http://app-test-lan.qizhidao.com/qzd-bff-inner/v2/api-docs',
    #     'http://app-test-lan.qizhidao.com/qzd-bff-ipad/v2/api-docs',
    #     'http://app-test-lan.qizhidao.com/qzd-bff-ips/v2/api-docs?group=企知道',
    #     'http://app-test-lan.qizhidao.com/qzd-bff-marketing/v2/api-docs?group=企知道',
    #     'http://app-test-lan.qizhidao.com/qzd-bff-operation/v2/api-docs?group=企知道',
    #     'http://app-test-lan.qizhidao.com/qzd-bff-patent/v2/api-docs?group=企知道',
    #     'http://app-test-lan.qizhidao.com/qzd-bff-pcweb/v2/api-docs?group=企知道',
    #     'http://app-test-lan.qizhidao.com/qzd-cms/v2/api-docs',
    #     'http://app-test-lan.qizhidao.com/qzd-cmsauto/v2/api-docs',
    #     'http://app-test-lan.qizhidao.com/qzd-customer/v2/api-docs',
    #     'http://app-test-lan.qizhidao.com/qzd-enterprise/v2/api-docs',
    #     'http://app-test-lan.qizhidao.com/qzd-mms/v2/api-docs',
    #     'http://app-test-lan.qizhidao.com/qzd-patent/v2/api-docs?group=企知道',
    #     'http://app-test-lan.qizhidao.com/qzd-shop-ams/v2/api-docs',
    #     'http://app-test-lan.qizhidao.com/qzd-shop-cart/v2/api-docs',
    #     'http://app-test-lan.qizhidao.com/qzd-shop-pay/v2/api-docs',
    #     'http://app-test-lan.qizhidao.com/qzd-ucs/v2/api-docs?group=企知道',
    #     'http://app-test-lan.qizhidao.com/shop-order/v2/api-docs',
    #     'http://app-test-lan.qizhidao.com/shop-search/v2/api-docs?group=企知道',
    #     'http://app-test-lan.qizhidao.com/wz-marketing/v2/api-docs',
    #     'http://app-test-lan.qizhidao.com/wzqzd-bff-operation/v2/api-docs',
    #     'http://app-api-test-lan.qizhidao.com/wzqzd-bff-wechat/v2/api-docs?group=企知道',
    #     'http://app-test-lan.qizhidao.com/wzqzd-expert/v2/api-docs?group=企知道'
    # ]
    # results = []
    # for url in urls:
    #     try:
    #         data = get_api_list(url)
    #     except Exception as e:
    #         print(f'获取接口数据异常: {e}')
    #         sys.exit()
    #     results.extend(data)
    # print(results[-1])
    # print(f'接口总数: {len(results)}')
    #
    # for index, api in enumerate(results):
    #     print(index, end=',')
    #     ApiDB().write_api(api)

    # 从excel获取信息然后写入数据库
    # from excel import Excel
    # el = Excel('swagger.xlsx')
    # doc_data = el.read_all()
    # for doc_info in doc_data:
    #     ApiDB().write_doc(doc_info)










