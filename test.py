#!/usr/bin/python
import sys
from pprint import pprint
from jira import JIRA
from api import *

msg = {
    'body': {
        u'i': 1,
        u'msg': {
            u'files': [{u'diff_url': u'https://cvs.example.net/test/testing?r1=1.62&r2=1.63&f=h',
            u'file': u'testing',
            u'log_url': u'https://cvs.example.net/test/testing?r1=1.63#rev1.63',
            u'module': u'test',
            u'new_rev': u'1.63',
            u'new_url': u'https://cvs.example.net/test/testing?view=markup&revision=1.63',
            u'old_rev': u'1.62',
            u'old_url': u'https://cvs.example.net/test/testing?view=markup&revision=1.62',
            u'url': u'https://cvs.example.net'}],
            u'message': u'some very useful commit message, ED-13',
            u'module': u'test',
            u'user': u'glen'
        },
        u'msg_id': u'2017-e729a2e2-7e36-482f-81f8-8d27afcfad85',
        u'timestamp': 1497985536,
        u'topic': u'net.ed.prod.cvs.commit',
        u'username': u'root'
    },
    'topic': u'net.ed.prod.cvs.commit'
}

links = cvs2link(msg['body']['msg'])

jira = JiraClient().getClient()
# add stuff to this issue:
# https://pycontribs.atlassian.net/browse/Z3E79A974A-4
issue = jira.issue('Z3E79A974A-4')

for link in links:
    jira.add_simple_link(issue, link)
