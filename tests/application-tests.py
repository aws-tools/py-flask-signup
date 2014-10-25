# Copyright 2013. Amazon Web Services, Inc. All Rights Reserved.
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import application
import unittest

import flask
from flask import current_app, request, Response


class AppTestCase(unittest.TestCase):
    """ Main test cases for our application """

    def setUp(self):
        app.testing = True

        with app.app_context():
            self.app=app.test_client()

    def test_load_config(self):
        """ Test that we can load our config properly """
        assertTrue(1)

    def test_get_test(self):
        """ Test hitting /test and that we get a correct HTTP response """
        assertTrue(1)

    def test_get_form(self):
        """ Test that we can get a signup form """
        assertTrue(1)

    def test_get_user(self):
        """ Test that we can get a user context """
        assertTrue(1)

    def test_login(self):
        """ Test that we can authenticate as a user """
        assertTrue(1)


if __name__ == '__main__':
    unittest.main()
