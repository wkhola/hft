# -*- coding: utf-8 -*-
from aop.api.base import BaseApi

class UmengBrandGetMonitoringDataRequest(BaseApi):
    """根据用户id返回该用户下所有符合查询条件的监测单元数据的指标

    References
    ----------
    https://open.1688.com/api/api.htm?ns=com.umeng.brand&n=umeng.brand.getMonitoringData&v=1&cat=default

    """

    def __init__(self, domain=None):
        BaseApi.__init__(self, domain)
        self.campaignId = None
        self.mediaId = None
        self.mId = None
        self.startDate = None
        self.endDate = None
        self.pageNum = None
        self.pageSize = None

    def get_api_uri(self):
        return '1/com.umeng.brand/umeng.brand.getMonitoringData'

    def get_required_params(self):
        return ['startDate', 'endDate']

    def get_multipart_params(self):
        return []

    def need_sign(self):
        return True

    def need_timestamp(self):
        return False

    def need_auth(self):
        return False

    def is_inner_api(self):
        return False
