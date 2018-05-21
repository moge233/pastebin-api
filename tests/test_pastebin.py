#!/usr/bin/env python

'''
test_pastebin.py

Provides automated tests for the Pastebin API wrapper.
'''


from unittest import TestCase, TestSuite


class RequestTestCase(TestCase):
    pass

class LoginTestCase(TestCase):
    pass

class CreatePasteTestCase(TestCase):
    pass

class CreateLoggedInPasteTestCase(TestCase):
    pass

class ListPastesTestCase(TestCase):
    pass

class ListTrendingPastesTestCase(TestCase):
    pass

class DeletePasteTestCase(TestCase):
    pass

class GetUserInformationTestCase(TestCase):
    pass


tests = [
    RequestTestCase, LoginTestCase, CreatePasteTestCase,
    CreateLoggedInPasteTestCase, ListPastesTestCase,
    ListTrendingPastesTestCase, DeletePasteTestCase,
    GetUserInformationTestCase
]


if __name__ == '__main__':
    unittest.main()
