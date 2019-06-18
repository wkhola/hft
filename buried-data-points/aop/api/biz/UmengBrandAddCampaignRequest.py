# -*- coding: utf-8 -*-
from aop.api.base import BaseApi

class UmengBrandAddCampaignRequest(BaseApi):
    """创建营销活动，传入活动名称，活动开始、结束时间及自定义的相关字段

    References
    ----------
    https://open.1688.com/api/api.htm?ns=com.umeng.brand&n=umeng.brand.addCampaign&v=1&cat=default

    """

    def __init__(self, domain=None):
        BaseApi.__init__(self, domain)
        self.campaignName = None
        self.startDay = None
        self.endDay = None
        self.convertType = None
        self.ipType = None
        self.customizeInfos = None

    def get_api_uri(self):
        return '1/com.umeng.brand/umeng.brand.addCampaign'

    def get_required_params(self):
        return ['campaignName', 'startDay', 'endDay']

    def get_multipart_params(self):
        return []

    def need_sign(self):
        return True

    def need_timestamp(self):
        return True

    def need_auth(self):
        return False

    def is_inner_api(self):
        return False
