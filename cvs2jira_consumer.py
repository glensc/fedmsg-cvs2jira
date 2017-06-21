"""

Consumer to show how to write a service that does stuff in
response to message on the `fedmsg bus <http://fedmsg.rtfd.org>`_.
"""

import fedmsg.consumers
from api import *

class CVS2JiraConsumer(fedmsg.consumers.FedmsgConsumer):
    # cvs2jira_consumer_enabled must be set to True in the config in fedmsg.d/ for
    # this consumer to be picked up and run when the fedmsg-hub starts.
    config_key = "cvs2jira_consumer_enabled"

    def __init__(self, hub):
        super(CVS2JiraConsumer, self).__init__(hub)

        # I'm only interested in messages from CVS
        topic = self.hub.config.get('cvs2jira_topic')

        # create api client only once
        self.api = JiraApi()
        self.jira = self.api.jira

    def consume(self, msg):
        self.log.info("CVS[%(topic)s]: %(user)s: %(module)s: %(message)s" % {
            'topic': msg['topic'],
            'user': msg['body']['msg']['user'],
            'module': msg['body']['msg']['module'],
            'message': msg['body']['msg']['message'],
        })

        message = msg['body']['msg']['message']
        issues = self.api.getMatchedIssues(message)
        if not issues:
            # easy way out
            return

        links = self.api.getJiraLinks(msg['body']['msg'])
        for issue in issues:
            issue = self.jira.issue(issue)
            for link in links:
                self.jira.add_simple_link(issue, link)
