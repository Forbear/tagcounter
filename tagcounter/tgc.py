import urllib.request
import re
import sqlite3
import time
import pickle
import yaml
import os
import argparse
from bs4 import BeautifulSoup


class TagCounter:
    def __init__(self, *args):
        self.__tags = {}
        self.__sc = {}
        self.arguments = self.parse_arguments(*args)
        self.test_time = time.strftime('%H:%M:%S')
        self.test_date = time.strftime('%a %d.%b')
        self.table_fields = 'date text, site text, uri text, tags text'
        self.connection = None
        self.cursor = None
        self.load_sc()

    def __str__(self):
        return f"{vars(self.arguments),}"

    def __del__(self):
        try:
            if self.connection:
                self.connection.close()
        except AttributeError:
            return None

    def connect(self):
        if not os.path.exists(self.arguments.directory):
            os.makedirs(self.arguments.directory)
            print(f"Directory {self.db_dir} was created.")
        if self.connection:
            self.connection.close()
        try:
            self.connection = sqlite3.connect(self.db_file)
            self.cursor = self.connection.cursor()
        except AttributeError:
            print('Connection to table error.')
            self.connection = None
            self.cursor = None
        except sqlite3.OperationalError:
            print('SQLite operational error.')
            self.connection = None
            self.cursor = None

    def __update_time(self):
        self.test_time = time.strftime('%H:%M:%S')

    def __update_date(self):
        self.test_date = time.strftime('%a %d.%b')

    @staticmethod
    def parse_arguments(*args):
        parser = argparse.ArgumentParser()
        parser.add_argument('command', help='Command to execute.')
        parser.add_argument('command_args', help='Arguments for a command.', nargs='*')
        parser.add_argument('--debug', help='Enable debug mode.', action='store_true')
        parser.add_argument('-uri', help='URI path of the request.', default='/3/')
        parser.add_argument('-website', help='Website/shortcut.', default='docs.python.org')
        parser.add_argument('-sc', help='Shortcuts file.', default='shortcuts.yaml')
        parser.add_argument('-table', help='Table name in DB.', default='default_table')
        parser.add_argument('-directory', help='Directory for DB.', default='databases')
        return parser.parse_args(*args)

    @property
    def uri(self):
        return self.arguments.uri

    @uri.setter
    def uri(self, uri):
        self.arguments.uri = uri

    @property
    def website(self):
        if self.arguments.website in self.__sc:
            return self.__sc[self.arguments.website]
        else:
            return self.arguments.website

    @website.setter
    def website(self, website):
        self.arguments.website = website

    @property
    def table_name(self):
        return self.arguments.table

    @table_name.setter
    def table_name(self, name):
        self.arguments.table = name

    @property
    def db_dir(self):
        return self.arguments.directory

    @db_dir.setter
    def db_dir(self, directory):
        self.arguments.directory = directory

    @property
    def url(self):
        return f"https://{self.website}{self.uri}"

    @property
    def db_file(self):
        return f"{self.db_dir}/{self.website}_{self.test_date}.db"

    @property
    def date_time(self):
        return f"{self.test_date} {self.test_time}"

    @property
    def tags(self):
        return self.__tags

    @property
    def pickled_tags(self):
        return str(pickle.dumps(self.__tags))

    @property
    def table_content(self):
        return self.date_time, self.website, self.uri, self.pickled_tags

    @property
    def table_exists(self):
        query = "SELECT count(name) FROM sqlite_master WHERE type='table' AND name=?"
        # sqlite qmark usage.
        try:
            self.cursor.execute(query, (self.table_name,))
            if self.cursor.fetchone()[0] == 1:
                return True
            else:
                return False
        except AttributeError:
            print(f"Get table from '{self.db_file}' failed.")

    @property
    def sc_file(self):
        return self.arguments.sc

    @sc_file.setter
    def sc_file(self, sc):
        self.arguments.sc = sc

    @property
    def connected(self):
        if self.cursor:
            return True
        else:
            return False

    @property
    def command(self):
        return self.arguments.command

    @command.setter
    def command(self, c):
        self.arguments.command = c

    def create_table(self):
        if self.table_exists:
            return True
        else:
            # For some reason qmark style does not work here.
            query = f"CREATE TABLE {self.table_name} ({self.table_fields})"
            self.cursor.execute(query)
            self.connection.commit()

    def print_table_content(self):
        self.connect()
        if self.table_exists:
            # For some reason qmark style does not work here.
            query = f"SELECT * FROM {self.table_name}"
            result = self.cursor.execute(query).fetchall()
            return '\n'.join(str(result).split(','))

    def register_tags(self):
        # Drop current tags before count.
        self.__tags = {}
        # Define regex to check link.
        regex_str = r'https?://(www)?[^/]*/'
        compiled_regex = re.compile(regex_str)
        # Check link
        match_result = compiled_regex.match(self.url)
        if not match_result:
            return None
        # Get HTML content and decode from bytes.
        response = urllib.request.urlopen(self.url)
        web_content = response.read().decode('utf-8')
        # Parse HTML content with the help of BeautifulSoup.
        soup = BeautifulSoup(web_content, 'html.parser')
        # Count tags.
        for tag in soup.find_all(True):
            if tag.name in self.__tags:
                self.__tags[tag.name] += 1
            else:
                self.__tags[tag.name] = 1

    def push_to_table(self):
        if self.table_exists:
            # For some reason qmark style does not work here.
            query = f"INSERT INTO {self.table_name} VALUES {self.table_content}"
            self.cursor.execute(query)
            self.connection.commit()

    def load_sc(self, *_):
        try:
            with open(self.sc_file, 'r') as f:
                shortcuts = yaml.load(f, Loader=yaml.FullLoader)
            self.__sc = shortcuts
            return self.__sc
        except FileNotFoundError:
            print(f"File '{self.sc_file}' was not found. Error.")
            return None

    def sc_list(self, *_):
        return self.__sc

    def add_shortcut(self, *_):
        if self.arguments.command_args is not None:
            if len(self.arguments.command_args) % 2 == 0:
                k = self.arguments.command_args[0::2]
                v = self.arguments.command_args[1::2]
                new_sc = dict(zip(k, v))
                with open(self.sc_file, 'a') as f:
                    yaml.dump(new_sc, f)
            return self.load_sc()

    def rm_shortcut(self, *_):
        if self.arguments.command_args is not None:
            try:
                with open(self.sc_file, 'r') as f:
                    sc = yaml.load(f, Loader=yaml.FullLoader)
                    for k in self.arguments.command_args:
                        del sc[k]
                with open(self.sc_file, 'w') as f:
                    yaml.dump(sc, f)
                return self.load_sc()
            except FileNotFoundError:
                return f"File '{self.sc_file}' was not found. Error."
            except KeyError as e:
                return f"Shortcut '{e.args[0]}' was not found. Error."

    def count_and_push(self, *_):
        self.connect()
        self.create_table()
        self.register_tags()
        self.push_to_table()
        return self.tags

    def synthetic(self, *_):
        self.register_tags()
        return self.__tags

    @property
    def callable(self):
        return {'add_sc': self.add_shortcut,
                'rm_sc': self.rm_shortcut,
                'print_table': self.print_table_content,
                'exec': self.count_and_push,
                'load_sc': self.load_sc,
                'synthetic': self.synthetic}

    @staticmethod
    def get_commands():
        return 'add_sc', 'rm_sc', 'print_table', 'exec', 'load_sc', 'synthetic'

    def execute(self):
        if self.arguments.command in self.callable:
            return self.callable[self.arguments.command]()
        else:
            return f"{self.arguments.command} is not valid command."
