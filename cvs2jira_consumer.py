"""

Consumer to show how to write a service that does stuff in
response to message on the `fedmsg bus <http://fedmsg.rtfd.org>`_.
"""

import fedmsg.consumers
from api import *

class CVS2JiraConsumer(fedmsg.consumers.FedmsgConsumer):
    # cvs2jira.consumer.enabled must be set to True in the config in fedmsg.d/ for
    # this consumer to be picked up and run when the fedmsg-hub starts.
    config_key = "cvs2jira.consumer.enabled"

    def __init__(self, hub):
        # I'm only interested in messages from CVS
        self.topic = self.abs_topic(hub.config, "cvs.commit")

        super(CVS2JiraConsumer, self).__init__(hub)

        # create api client only once
        self.api = JiraApi()
        self.jira = self.api.jira

    # no proper way to configure just topic suffix
    # https://github.com/fedora-infra/fedmsg/pull/428
    def abs_topic(self, config, topic):
        """
        prefix topic with topic_prefix and environment config values
        """
        topic_prefix = config.get('topic_prefix')
        environment = config.get('environment')
        return "%s.%s.%s" % (topic_prefix, environment, topic)

    def consume(self, msg):
        self.log.info("CVS2Jira[%(topic)s]: %(user)s: %(message)s" % {
            'topic': msg['topic'],
            'user': msg['body']['msg']['user'],
            'message': msg['body']['msg']['message'],
        })
        msg = msg['body']['msg']

        message = msg['message']
        issues = self.api.getMatchedIssues(message)
        self.log.info("CVS2Jira: issues: %s" % issues)
        if not issues:
            # easy way out
            return

        links = self.api.getJiraLinks(msg)
        for issue in issues:
            issue = self.jira.issue(issue)
            for link in links:
                self.log.info("CVS2Jira: add link[%s]: %s" % (issue, link))
                self.jira.add_simple_link(issue, link)
