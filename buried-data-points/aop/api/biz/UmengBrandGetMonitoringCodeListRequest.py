# -*- coding: utf-8 -*-
from aop.api.base import BaseApi

class UmengBrandGetMonitoringCodeListRequest(BaseApi):
    """批量获取营销活动下对应单元的监测链接

    References
    ----------
    https://open.1688.com/api/api.htm?ns=com.umeng.brand&n=umeng.brand.getMonitoringCodeList&v=1&cat=default

    """

    def __init__(self, domain=None):
        BaseApi.__init__(self, domain)
        self.campaignId = None
        self.pageNum = None
        self.pageSize = None

    def get_api_uri(self):
        return '1/com.umeng.brand/umeng.brand.getMonitoringCodeList'

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
