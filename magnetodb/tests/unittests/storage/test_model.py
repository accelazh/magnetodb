# Copyright 2014 Symantec Inc.
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

import unittest

from magnetodb.storage import models


class ModelsTestCase(unittest.TestCase):
    """The test for Models."""

    def test_strset_to_json(self):
        value = models.AttributeValue.str_set(['Update', 'Help'])

        expected = (
            '{"__model__": "AttributeValue", '
            '"type": {"__model__": "AttributeType", '
            '"collection_type": "set", "element_type": "s"}, '
            '"value": ["Help", "Update"]}'
        )
        self.assertEqual(expected, value.to_json())