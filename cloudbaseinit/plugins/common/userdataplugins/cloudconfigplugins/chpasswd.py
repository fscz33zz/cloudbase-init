# Copyright 2019 Cloudbase Solutions Srl
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import datetime
import os
import pytz
import six

from oslo_log import log as oslo_logging

from cloudbaseinit import conf as cloudbaseinit_conf
from cloudbaseinit import exception
from cloudbaseinit.osutils import factory as osutils_factory
from cloudbaseinit.plugins.common.userdataplugins.cloudconfigplugins import (
    base
)

CONF = cloudbaseinit_conf.CONF
LOG = oslo_logging.getLogger(__name__)


class ChPasswdPlugin(base.BaseCloudConfigPlugin):
    """Sets passwords for users given in the cloud-config format."""

    def __init__(self):
        self._osutils = osutils_factory.get_os_utils()

    def _set_pw(self, user_name, password, expires=False):
        self._osutils.set_user_password(user_name, password, password_expires=expires)

    def process(self, data):
        """Process the given data received from the cloud-config userdata.

        It knows to process only lists and dicts.
        """
        if not isinstance(data, dict):
            raise exception.CloudbaseInitException(
                "Can't process the type of data %r" % type(data))        

        if not "list" in data:
            LOG.warning("Parameter 'list' with user/pw information missing. Abort.")
        else:
            expires = data.get("expires") if "expires" in data else False
            for item in data.get("list"):
                sep = item.find(":")
                self._set_pw(item[:sep], item[sep+1:], expires=expires)

        return False
