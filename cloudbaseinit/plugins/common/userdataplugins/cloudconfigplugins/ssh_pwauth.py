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
import re

from oslo_log import log as oslo_logging

from cloudbaseinit import conf as cloudbaseinit_conf
from cloudbaseinit import exception
from cloudbaseinit.osutils import factory as osutils_factory
from cloudbaseinit.plugins.common.userdataplugins.cloudconfigplugins import (
    base
)

CONF = cloudbaseinit_conf.CONF
LOG = oslo_logging.getLogger(__name__)


class SSHPwAuthPlugin(base.BaseCloudConfigPlugin):
    """Sets passwords for users given in the cloud-config format."""

    def __init__(self):
        self._osutils = osutils_factory.get_os_utils()

    def _set_ssh_pw_auth_allowed(self, answer):
        with open("C:/ProgramData/ssh/sshd_config", 'r') as f:
            sshd_config = f.read()
        sshd_config_new = re.sub(".*PasswordAuthentication.*",
                                 "PasswordAuthentication %s" % answer,
                                 sshd_config)
        with open("C:/ProgramData/ssh/sshd_config", 'w') as f:
            f.write(sshd_config_new)

    def process(self, data):
        """Process the given data received from the cloud-config userdata.

        It knows to process only lists and dicts.
        """
        if not isinstance(data, bool):
            raise exception.CloudbaseInitException(
                "Can't process the type of data %r" % type(data))

        self._set_ssh_pw_auth_allowed("yes" if data else "no")

        return False
