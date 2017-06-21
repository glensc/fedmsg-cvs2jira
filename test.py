#!/usr/bin/python
import sys
from pprint import pprint
from jira import JIRA
from api import *

msg = {
    'body': {
        u'i': 1,
        u'msg': {
            u'commitid': u'fXLcfrr9z2xPDgWz',
            u'files': [
                {
                    u'commitid': u'fXLcfrr9z2xPDgWz',
                    u'filename': u'meh',
                    u'new_rev': u'1.79',
                    u'old_rev': u'1.78',
                    u'urls': {
                        u'diff_url': u'https://cvs.example.net/test/jira/meh?r1=1.78&r2=1.79&f=h',
                        u'log_url': u'https://cvs.example.net/test/jira/meh?r1=1.79#rev1.79',
                        u'new_url': u'https://cvs.example.net/test/jira/meh?view=markup&revision=1.79',
                        u'old_url': u'https://cvs.example.net/test/jira/meh?view=markup&revision=1.78',
                    },
                },
            ],
            # add stuff to this issue:
            # https://pycontribs.atlassian.net/browse/Z3E79A974A-4
            u'message': u'some very useful commit message, Z3E79A974A-4, Z3E79A974A-4.',
            u'module': u'test/jira',
            u'user': u'glen',
        },
        u'msg_id': u'2017-74a9b728-cf9c-4998-b1dd-a9871a08152c',
        u'timestamp': 1498067689,
        u'topic': u'net.ed.prod.cvs.commit',
        u'username': u'root',
    },
    'topic': u'net.ed.prod.cvs.commit',
}

api = JiraApi()
jira = api.jira

message = msg['body']['msg']['message']
issues = api.getMatchedIssues(message)
pprint(issues)
links = api.getJiraLinks(msg['body']['msg'])
pprint(links)
for issue in issues:
    issue = jira.issue(issue)
    for link in links:
        jira.add_simple_link(issue, link)
