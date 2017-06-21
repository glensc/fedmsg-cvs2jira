"""

This is a config file that must appear in ./fedmsg.d/ alongside the other
config files from the fedmsg development checkout.

In production, this should go into /etc/fedmsg.d/ but for development it can
just live in your cwd/pwd.

"""

config = {
    'cvs2jira_consumer_enabled': True,
    'cvs2jira_topic' : 'net.ed.prod.cvs.commit*',
}
