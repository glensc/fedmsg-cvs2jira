#!/usr/bin/python

import re
import jira

class JiraApi():
    # Default JIRA URL
    JIRA_URL = 'https://pycontribs.atlassian.net'

    def __init__(self):
        self.jira = self.getClient()

    def getClient(self):
        arguments = self.buildClientArguments()
        return jira.JIRA(**arguments)

    # build arguments for creating JIRA client
    # mostly loading values from environment.
    # arguments are compatible for JIRA() constructor:
    # https://jira.readthedocs.io/en/master/api.html#jira
    def buildClientArguments(self):
        from os import environ as env
        args = {
            'server': env.get('JIRA_URL', self.JIRA_URL),
        }
        if env.get('JIRA_AUTH_USER'):
            args['basic_auth'] = (
                env['JIRA_AUTH_USER'],
                env['JIRA_AUTH_PW'],
            )
        return args

    def getMatchedIssues(self, message):
        pattern = self.getJiraProjectPattern()
        issues = list(set(pattern.findall(message)))
        return issues

    # get pattern for matching project keys
    # project keys are fetched from JIRA
    def getJiraProjectPattern(self):
        projectKeys = [project.key for project in self.jira.projects()]
        pattern = '(?P<issue>(?:%s)-\d+)' % '|'.join(projectKeys)
        return re.compile(pattern)

    # convert cvs commit payload from fedmsg
    # to structure usable for adding remote issue link in jira
    # https://developer.atlassian.com/jiradev/jira-platform/guides/other/guide-jira-remote-issue-links/jira-rest-api-for-remote-issue-links
    #
    # - This hook should add link (with diff) to jira issue, that contains file path and commit message.
    # - It its becomes problematic (technically) to add link, comment should be used. Never both!
    #
    # Due the way CVS works, the method returns link structure for each file, not whole commit
    def getJiraLinks(self, commit):
        links = []

        for f in commit['files']:
            path = "%s/%s" % (f['module'], f['file'])
            link = {
                "url": f['diff_url'],
                "title": path,
                "summary": commit['message'],
            }
            links.append(link)

        return links
