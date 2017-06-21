"""

Consumer to show how to write a service that does stuff in
response to message on the `fedmsg bus <http://fedmsg.rtfd.org>`_.
"""

import fedmsg.consumers
from api import *

class CVS2JiraConsumer(fedmsg.consumers.FedmsgConsumer):
    # my_consumer_enabled must be set to True in the config in fedmsg.d/ for
    # this consumer to be picked up and run when the fedmsg-hub starts.
    config_key = "cvs2jira_consumer_enabled"

    # I'm only interested in messages from CVS
    topic = "net.ed.prod.cvs.commit*"

    def consume(self, message):
        links = cvs2link(message['body']['msg'])
        if not links:
            # easy way out
            return

        from pprint import pprint
        for link in links:
            pprint(link)
