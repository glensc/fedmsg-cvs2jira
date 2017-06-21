#!/usr/bin/python

# convert cvs commit payload from fedmsg
# to structure usable for adding remote issue link in jira
# https://developer.atlassian.com/jiradev/jira-platform/guides/other/guide-jira-remote-issue-links/jira-rest-api-for-remote-issue-links
#
# - This hook should add link (with diff) to jira issue, that contains file path and commit message.
# - It its becomes problematic (technically) to add link, comment should be used. Never both!
#
# Due the way CVS works, the method returns link structure for each file, not whole commit
def cvs2link(commit):
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
