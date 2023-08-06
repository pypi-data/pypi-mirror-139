import datetime

from collections import Counter

import networkx as nx

from gitrics import configuration
from gitrics.epic import gitricsEpic
from gitrics.issue import gitricsIssue
from gitrics.itemset import gitricsItemSet
from gitrics.user.user import gitricsUser

from glapi.group import GitlabGroup

class gitricsGroup(GitlabGroup):
    """
    gitricsGroup is an abstraction of the GitLab Group data object specific to the requirements of the gitrics ecosystem.
    """

    def __init__(self, id: str = None, group: dict = None, epics: gitricsItemSet = None, issues: gitricsItemSet = None, users: list = None, date_start: str = None, date_end: str = None, token: str = configuration.GITLAB_TOKEN, version: str = configuration.GITLAB_API_VERSION):
        """
        Args:
            date_end (string): iso 8601 date value
            date_start (string): iso 8601 date value
            group (dict): key/values representing a Gitlab Group
            id (string): GitLab Group id
            epics (gitricsItemSet): classes of gitricsEpic
            issues (gitricsItemSet): classes of gitricsIssue
            token (string): GitLab personal access or deploy token
            users (list): dictionaries of GitLab User
            version (string): GitLab API version as base url
        """

        self.date_end = date_end
        self.date_start = date_start

        # initialize inheritance
        super(gitricsGroup, self).__init__(
            group=group,
            id=id,
            token=token,
            version=version
        )

        self.epics = epics if epics else gitricsItemSet("epics")
        self.issues = issues if issues else gitricsItemSet("issues")

        # get users
        self.users = [gitricsUser(user=d) for d in users] if users else [gitricsUser(user=d) for d in self.extract_users()]
