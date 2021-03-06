# Copyright 2013 OpenStack Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""Keystone PKI Token Provider."""

import subprocess  # nosec : used to catch subprocess exceptions

from keystoneclient.common import cms
from oslo_log import log
from oslo_log import versionutils
from oslo_serialization import jsonutils

from keystone.common import utils
import keystone.conf
from keystone import exception
from keystone.i18n import _, _LE
from keystone.token.providers import common


CONF = keystone.conf.CONF

LOG = log.getLogger(__name__)


@versionutils.deprecated(
    as_of=versionutils.deprecated.MITAKA,
    what='the PKI token provider',
    in_favor_of='the Fernet or UUID token providers')
class Provider(common.BaseProvider):
    def _get_token_id(self, token_data):
        try:
            # force conversion to a string as the keystone client cms code
            # produces unicode.  This can be removed if the client returns
            # str()
            # TODO(ayoung): Make to a byte_str for Python3
            token_json = jsonutils.dumps(token_data, cls=utils.PKIEncoder)
            token_id = str(cms.cms_sign_token(token_json,
                                              CONF.signing.certfile,
                                              CONF.signing.keyfile))
            return token_id
        except subprocess.CalledProcessError:
            LOG.exception(_LE('Unable to sign token'))
            raise exception.UnexpectedError(_(
                'Unable to sign token.'))

    @property
    def _supports_bind_authentication(self):
        """Return if the token provider supports bind authentication methods.

        :returns: True
        """
        return True

    def needs_persistence(self):
        """Should the token be written to a backend."""
        return True
