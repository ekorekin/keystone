# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from keystone.common import validation
from keystone.common.validation import parameter_types


# NOTE(lhcheng): the max length is not applicable since it is specific
# to the SQL backend, LDAP does not have length limitation.
_identity_name = {
    'type': 'string',
    'minLength': 1,
    'pattern': '[\S]+'
}

# Schema for Identity v2 API

_user_properties_v2 = {
    'description': validation.nullable(parameter_types.description),
    'enabled': parameter_types.boolean,
    'tenantId': validation.nullable(parameter_types.id_string),
    'name': _identity_name,
    'username': _identity_name,
    'password': {
        'type': ['string', 'null']
    }
}

user_update_v2 = {
    'type': 'object',
    'properties': _user_properties_v2,
    'minProperties': 0,
    'additionalProperties': True
}

# Schema for Identity v3 API

_user_properties = {
    'default_project_id': validation.nullable(parameter_types.id_string),
    'description': validation.nullable(parameter_types.description),
    'domain_id': parameter_types.id_string,
    'enabled': parameter_types.boolean,
    'name': _identity_name,
    'password': {
        'type': ['string', 'null']
    }
}

user_create = {
    'type': 'object',
    'properties': _user_properties,
    'required': ['name'],
    'additionalProperties': True
}

user_update = {
    'type': 'object',
    'properties': _user_properties,
    'minProperties': 1,
    'additionalProperties': True
}

_group_properties = {
    'description': validation.nullable(parameter_types.description),
    'domain_id': parameter_types.id_string,
    'name': _identity_name
}

group_create = {
    'type': 'object',
    'properties': _group_properties,
    'required': ['name'],
    'additionalProperties': True
}

group_update = {
    'type': 'object',
    'properties': _group_properties,
    'minProperties': 1,
    'additionalProperties': True
}

enable_user_v2 = {
    'type': 'object',
    'properties': {'enabled': parameter_types.boolean},
    'required': ['enabled'],
    'additionalProperties': True
}
