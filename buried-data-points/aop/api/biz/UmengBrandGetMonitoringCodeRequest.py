# -*- coding: utf-8 -*-
from aop.api.base import BaseApi

class UmengBrandGetMonitoringCodeRequest(BaseApi):
    """当前用户下，在某个营销活动下面创建监测单元。

    References
    ----------
    https://open.1688.com/api/api.htm?ns=com.umeng.brand&n=umeng.brand.getMonitoringCode&v=1&cat=default

    """

    def __init__(self, domain=None):
        BaseApi.__init__(self, domain)
        self.monitoringId = None

    def get_api_uri(self):
        return '1/com.umeng.brand/umeng.brand.getMonitoringCode'

    def get_required_params(self):
        return ['monitoringId']

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
