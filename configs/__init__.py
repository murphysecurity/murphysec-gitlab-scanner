# coding=utf8
import datetime
import github
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import redis
import configparser
from datetime import datetime
import json
import os

config = configparser.ConfigParser()
path = os.path.split(os.path.realpath(__file__))[0]
config.read(path + "/conf.ini", encoding="utf-8")


class GitLab:
    def __init__(self):
        self.address = config.get('gitlab', 'GITLABADDRESS')
        self.token = config.get('gitlab', 'GITLABTOKEN')

    def get_address(self):
        return self.address

    def get_token(self):
        return self.token


class Murphy:
    def __init__(self):
        self.token = config.get('gitlab', 'MURPHYSECTOKEN')

    def get_token(self):
        return self.token


gitlab = GitLab()
murphy = Murphy()

GITLABADDRESS = config.get('gitlab', 'GITLABADDRESS')
GITLABTOKEN = config.get('gitlab', 'GITLABTOKEN')
MURPHYSECTOKEN = config.get('gitlab', 'MURPHYSECTOKEN')
