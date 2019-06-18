# -*- coding: utf-8 -*-
from aop.api.base import BaseApi

class UmengBrandAddMonitoringRequest(BaseApi):
    """当前用户下，在某个营销活动下面创建监测单元

    References
    ----------
    https://open.1688.com/api/api.htm?ns=com.umeng.brand&n=umeng.brand.addMonitoring&v=1&cat=default

    """

    def __init__(self, domain=None):
        BaseApi.__init__(self, domain)
        self.campaignId = None
        self.landingPageUrl = None
        self.mediaType = None
        self.mediaName = None
        self.terminalType = None
        self.positionType = None
        self.positionName = None
        self.creativityName = None
        self.customizeInfos = None

    def get_api_uri(self):
        return '1/com.umeng.brand/umeng.brand.addMonitoring'

    def get_required_params(self):
        return ['campaignId', 'landingPageUrl', 'mediaType', 'mediaName', 'terminalType', 'positionType', 'positionName', 'creativityName']

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
