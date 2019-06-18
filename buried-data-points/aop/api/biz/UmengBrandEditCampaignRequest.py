# -*- coding: utf-8 -*-
from aop.api.base import BaseApi

class UmengBrandEditCampaignRequest(BaseApi):
    """当前用户下，根据营销活动id，编辑活动的开始、结束时间及名称。

    References
    ----------
    https://open.1688.com/api/api.htm?ns=com.umeng.brand&n=umeng.brand.editCampaign&v=1&cat=default

    """

    def __init__(self, domain=None):
        BaseApi.__init__(self, domain)
        self.campaignId = None
        self.campaignName = None
        self.startDay = None
        self.endDay = None
        self.customizeInfos = None

    def get_api_uri(self):
        return '1/com.umeng.brand/umeng.brand.editCampaign'

    def get_required_params(self):
        return ['campaignId']

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
