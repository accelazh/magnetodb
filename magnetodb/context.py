# Copyright 2011 OpenStack Foundation
# Copyright 2010 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
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

import copy

from oslo_context import context

from magnetodb.openstack.common import local
from magnetodb.openstack.common import log as logging
from magnetodb import policy


LOG = logging.getLogger(__name__)


class RequestContext(context.RequestContext):
    """Security context and request information.

    Represents the user taking a given action within the system.

    """
    def __init__(self, user, tenant, is_admin=None, roles=None,
                 project_name=None, request_id=None, auth_token=None,
                 overwrite=True, service_catalog=None, domain=None,
                 user_domain=None, project_domain=None, **kwargs):
        """Initialize RequestContext.

        :param overwrite: Set to False to ensure that the greenthread local
            copy of the index is not overwritten.

        :param kwargs: Extra arguments that might be present, but we ignore
            because they possibly came in from older rpc messages.
        """

        super(RequestContext, self).__init__(auth_token=auth_token,
                                             user=user,
                                             tenant=tenant,
                                             domain=domain,
                                             user_domain=user_domain,
                                             project_domain=project_domain,
                                             is_admin=is_admin,
                                             request_id=request_id)
        self.roles = roles or []
        self.project_name = project_name
        if overwrite or not hasattr(local.store, 'context'):
            self.update_store()

        if service_catalog:
            # Only include required parts of service_catalog
            self.service_catalog = [s for s in service_catalog
                                    if s.get('type') in ('object-store',)]
        else:
            # if list is empty or none
            self.service_catalog = []

        # We need to have RequestContext attributes defined
        # when policy.check_is_admin invokes request logging
        # to make it loggable.
        if self.is_admin is None:
            self.is_admin = policy.check_is_admin(self.roles)
        elif self.is_admin and 'admin' not in self.roles:
            self.roles.append('admin')

    def update_store(self):
        local.store.context = self

    def to_dict(self):
        default = super(RequestContext, self).to_dict()
        extra = {'user': self.user,
                 'tenant': self.tenant,
                 'project_name': self.project_name,
                 'domain': self.domain,
                 'roles': self.roles,
                 'service_catalog': self.service_catalog}
        return dict(default.items() + extra.items())

    @classmethod
    def from_dict(cls, values):
        return cls(**values)

    def elevated(self, read_deleted=None, overwrite=False):
        """Return a version of this context with admin flag set."""
        context = self.deepcopy()
        context.is_admin = True

        if 'admin' not in context.roles:
            context.roles.append('admin')

        if read_deleted is not None:
            context.read_deleted = read_deleted

        return context

    def deepcopy(self):
        return copy.deepcopy(self)


def get_admin_context(read_deleted="no"):
    return RequestContext(user=None,
                          tenant=None,
                          is_admin=True,
                          read_deleted=read_deleted,
                          overwrite=False)
