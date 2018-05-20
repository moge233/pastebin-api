#!/usr/bin/env python

'''
Pastebin API wrapper using urllib

05/19/2018
'''


from collections import OrderedDict
from html.parser import HTMLParser
from http.client import HTTPException
from urllib.request import urlopen
from urllib.parse import urlencode


class Pastebin:
    '''
    A Pastebin API wrapper.

    attributes:
        api_key (bytes)
        user_key (bytes)

    methods:
        login
        create_paste
        create_logged_in_paste
        list_pastes
        list_trending_pastes
        delete_paste
    '''

    def __init__(self, api_key):
        self.api_key = bytes(api_key, encoding='utf-8')
        self.user_key = None

    def __repr__(self):
        return 'Pastebin(%s)'.format(self.api_key)

    def _request(self, url, data=None, **kwargs):
        '''
        A custom request method for the Pastebin API wrapper.

        args:
            url (str)

        kwargs:

        returns:
            http.client.HTTPResponse object

        raises:
            http.client.HTTPException if the response code is not 200
        '''
        response = urlopen(url, data=data)
        if response.status == 200:
            return response
        else:
            raise HTTPException

    def login(self, user_name, user_password):
        '''
        Use the Pastebin members system to login

        args:
            user_name (bytes): the user name to login to
            user_password (bytes): the user password to use to login

        returns:
           Pastebin API user key (bytes)
        '''
        data = {
            'api_dev_key' : self.api_key,
            'api_user_name' : user_name,
            'api_user_password' : user_password
        }
        data = urlencode(data)
        data = bytes(data, encoding='utf-8')
        response = self._request('https://pastebin.com/api/api_login.php',
                                 data=data)
        self.user_key = response.read()
        return self.user_key

    def create_paste(self, paste_code, user_key=None, paste_name=None,
                     paste_format=None, paste_private=0,
                     paste_expire_date=None):
        '''
        Create a new paste.

        args:
            paste_code (bytes): the code to paste to Pastebin

        kwargs:
            user_key (bytes): call the login() method to receive a user
                              key
            paste_name (bytes): this will be the name of the paste
            paste_format (bytes): the syntax highlighting value
            paste_private (int): default is 0; public=0, unlisted=1,
                                 private=2
            paste_expire_date (bytes):
                valid paste_expire_date options:
                    N = never
                    10M = 10 minutes
                    1H = 1 hour
                    1D = 1 day
                    1W = 1 week
                    2W = 2 weeks
                    1M = 1 month
                    6M = 6 months
                    1Y = 1 year

        returns:
            http.client.HTTPResponse object
        '''
        data = {
            'api_dev_key' : self.api_key,
            'api_option' : b'paste',
            'api_paste_code' : paste_code,
        }
        if user_key:
            data['api_user_key'] = user_key
        if paste_name:
            data['api_paste_name'] = paste_name
        if paste_format:
            data['api_paste_format'] = paste_format
        data['api_paste_private'] = paste_private
        if paste_expire_date:
            data['api_paste_expire_date'] = paste_expire_date
        data = urlencode(data)
        data = bytes(data, encoding='utf-8')
        response = self._request('https://pastebin.com/api/api_post.php',
                                 data=data)
        return response

    def create_logged_in_paste(self, paste_code, paste_name=None,
                               paste_format=None, paste_private=0,
                               paste_expire_date=None):
        '''
        Create a new logged in paste. Must call Pastebin.login first.
        Calls create_paste() method with user_key keyword set to
        self.user_key

        args:
            paste_code (bytes): the code to paste to Pastebin

        kwargs:
            paste_name (bytes): this will be the name of the paste
            paste_format (bytes): the syntax highlighting value
            paste_private (int): default is 0; public=0, unlisted=1,
                                 private=2
            paste_expire_date (bytes):
                valid paste_expire_date options:
                    N = never
                    10M = 10 minutes
                    1H = 1 hour
                    1D = 1 day
                    1W = 1 week
                    2W = 2 weeks
                    1M = 1 month
                    6M = 6 months
                    1Y = 1 year

        returns:
            http.client.HTTPResponse object

        raises:
            AttributeError if self.user_key is not set
        '''
        if not self.user_key:
            raise AttributeError('''user_key is not set. Login first to
                                 create a logged in paste.''')
        response = self.create_paste(paste_code, user_key=self.user_key,
                                     paste_name=paste_name,
                                     paste_format=paste_format,
                                     paste_private=paste_private,
                                     paste_expire_date=paste_expire_date
                                    )
        return response

    def list_pastes(self, results_limit=5, parse=False):
        '''
        List all the pastes created by a user.
        Must call Pastebin.login first.

        kwargs:
            results_limit (int): default is 5
            parse (bool): If this is true, a list of PastebinPastes
                          objects will be returned instead of the
                          usual HTTPResponse

        returns:
            http.client.HTTPResponse object
        '''
        if not self.user_key:
            raise AttributeError('''user_key is not set.
                                 Login first to create a logged
                                 in paste.''')
        data = {
            'api_dev_key' : self.api_key,
            'api_user_key' : self.user_key,
            'api_results_limit' : results_limit,
            'api_option' : b'list'
        }
        data = urlencode(data)
        data = bytes(data, encoding='utf-8')
        response = self._request('https://pastebin.com/api/api_post.php',
                                 data=data)
        if parse:
            response = response.read().decode(encoding='utf-8')
            parser = PastebinPasteListParser()
            pastes = parser.get_pastes(response)
            return pastes
        return response

    def list_trending_pastes(self, parse=False):
        '''
        List the 18 currently trending pastes.

        kwargs:
            parse (bool): If this is true, a list of PastebinPastes
                          objects will be returned instead of the
                          usual HTTPResponse

        returns:
            http.client.HTTPResponse object
        '''
        data = {
            'api_dev_key' : self.api_key,
            'api_option' : b'trends'
        }
        data = urlencode(data)
        data = bytes(data, encoding='utf-8')
        response = self._request('https://pastebin.com/api/api_post.php',
                                 data=data)
        if parse:
            response = response.read().decode(encoding='utf-8')
            parser = PastebinPasteListParser()
            pastes = parser.get_pastes(response)
            return pastes
        return response

    def delete_paste(self):
        '''
        Delete pastes created by a user.

        args:
            paste_key

        returns:
            http.client.HTTPResponse object
        '''
        if not self.user_key:
            raise AttributeError('''user_key is not set.
                                 Login first to delete a paste.''')
        data = {
            'api_dev_key' : self.api_key,
            'api_user_key' : self.user_key,
            'api_paste_key' : paste_key,
            'api_option' : b'delete'
        }
        data = urlencode(data)
        data = bytes(data, encoding='utf-8')
        response = self._request('https://pastebin.com/api/api_post.php',
                                 data=data)
        return response

    def get_user_information(self, parse=False):
        '''
        Obtain a user's personal information and settings.
        Must be logged in first.

        kwargs:
            parse (bool): If this is true, a PastebinUser
                          object will be returned instead of the
                          usual HTTPResponse

        returns:
            http.client.HTTPResponse object

        raises:
            AttributeError if self.user_key is not set
        '''
        if not self.user_key:
            raise AttributeError('''user_key is not set.
                                 Login first to delete a paste.''')
        data = {
            'api_dev_key' : self.api_key,
            'api_user_key' : self.user_key,
            'api_option' : b'userdetails'
        }
        data = urlencode(data)
        data = bytes(data, encoding='utf-8')
        response = self._request('https://pastebin.com/api/api_post.php',
                                 data=data)
        if parse:
            response = response.read().decode(encoding='utf-8')
            parser = PastebinUserParser()
            user = parser.get_user_information(response)
            return user
        return response


class PastebinPasteListParser(HTMLParser):
    '''
    A custom parser for the list_pastes method of the Pastebin API.
    Mostly for internal use on the Pastebin.list_pastes method when
    the parse flag is true.
    '''
    def __init__(self):
        HTMLParser.__init__(self)
        self._tups = []

    def get_pastes(self, data):
        self.feed(data)
        return self._get_pastes()

    def handle_data(self, data):
        tag = self.get_starttag_text()[1:-1]
        data = data
        if data != '\r\n':
            tup = (tag, data)
            self._tups.append(tup)

    def _get_pastes(self):
        if not self._tups:
            msg = '''please call the PastebinPasteListParser.feed(data)
                method to get a list of tuples from the
                Pastebin list_pastes API before using this method'''
            raise AttributeError(msg)
        pastes = []
        n_pastes = len(self._tups) // 10
        ind = 0
        while ind < n_pastes:
            paste = PastebinPaste(
                self._tups[10*ind + 0][1], # paste_key
                self._tups[10*ind + 1][1], # paste_date
                self._tups[10*ind + 2][1], # paste_title
                self._tups[10*ind + 3][1], # paste_size
                self._tups[10*ind + 4][1], # paste_expire_date
                self._tups[10*ind + 5][1], # paste_private
                self._tups[10*ind + 6][1], # paste_format_long
                self._tups[10*ind + 7][1], # paste_format_short
                self._tups[10*ind + 8][1], # paste_url
                self._tups[10*ind + 9][1]  # paste_hits
            )
            ind += 1
            pastes.append(paste)
        return pastes


class PastebinUserParser(HTMLParser):
    '''
    A custom parser for the get_ user_information method of the
    Pastebin API.
    Mostly for internal use on the Pastebin.get_ user_information
    method when the parse flag is true.
    '''
    def __init__(self):
        HTMLParser.__init__(self)
        self._user_dict = OrderedDict()

    def get_user_information(self, data):
        self.feed(data)
        return self._get_user_information()

    def handle_data(self, data):
        tag = self.get_starttag_text()[1:-1]
        data = data
        if data != '\r\n':
            self._user_dict[tag] = data

    def _get_user_information(self):
        user = PastebinUser(**self._user_dict)
        return user


class PastebinPaste:
    '''
    This class encapsulates a Pastebin paste

    attributes:
        paste_key (bytes)
        paste_date (bytes)
        paste_title (bytes)
        paste_size (int)
        paste_expire_date (bytes)
        paste_private (int)
        paste_format_long (byes)
        paste_format_short (bytes)
        paste_url (bytes)
        paste_hits (int)
    '''
    def __init__(self, paste_key, paste_date, paste_title, paste_size,
                 paste_expire_date, paste_private, paste_format_long,
                 paste_format_short, paste_url, paste_hits):
        self.paste_key = paste_key
        self.paste_date = paste_date
        self.paste_title = paste_title
        self.paste_size = paste_size
        self.paste_expire_date = paste_expire_date
        self.paste_private = paste_private
        self.paste_format_long = paste_format_long
        self.paste_format_short = paste_format_short
        self.paste_url = paste_url
        self.paste_hits = paste_hits

    def __repr__(self):
        _repr = 'PastebinPaste({}, {}, {}, {}, {}, {}, {}, {}, {}, {})'
        return _repr.format(*[getattr(self, str(key))
                              for key in self.__dict__.keys()])


class PastebinUser:
    '''
    This class encapsulates a Pastebin user.

    attributes:
        user_name (bytes)
        user_format_short (bytes)
        user_expiration (bytes)
        user_avatar_url (bytes)
        user_private (int)
        user_website (bytes)
        user_email (bytes)
        user_location (bytes)
        user_account_type (int)
    '''
    def __init__(self, user_name=None, user_format_short=None,
                 user_expiration=None,
                 user_avatar_url=None, user_private=None,
                 user_website=None, user_email=None,
                 user_location=None, user_account_type=None):
        self.user_name = user_name
        self.user_format_short = user_format_short
        self.user_expiration = user_expiration
        self.user_avatar_url = user_avatar_url
        self.user_private = user_private
        self.user_website = user_website
        self.user_email = user_email
        self.user_location = user_location
        self.user_account_type = user_account_type

    def __repr__(self):
        _repr = '''PastebinUser(user_name={}, user_format_short={}, user_expiration={}, user_avatar_url={}, user_private={}, user_website={}, user_email={}, user_location={}, user_account_type={})'''
        return _repr.format(*[getattr(self, str(key))
                              for key in self.__dict__.keys()])


__all__ = ['Pastebin', 'PastebinPasteListParser', 'PastebinPaste',
           'PastebinUserParser', 'PastebinUser']
