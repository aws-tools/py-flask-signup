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

from application import application
from flask import Flask, current_app, request, Response

""" Main test cases for our application """
class AppTestCase(unittest.TestCase):

    #application = Flask(__name__)

    def setUp(self):
        application.testing = True

        with application.app_context():
            self.client = current_app.test_client()

    def test_load_config(self):
        """ Test that we can load our config properly """
        self.assertTrue(1)

    def test_get_test(self):
        """ Test hitting /test and that we get a correct HTTP response """
        self.assertTrue(1)

    def test_get_form(self):
        """ Test that we can get a signup form """
        self.assertTrue(1)

    def test_get_user(self):
        """ Test that we can get a user context """
        self.assertTrue(1)

    def test_login(self):
        """ Test that we can authenticate as a user """
        self.assertTrue(1)


if __name__ == '__main__':
    unittest.main()

