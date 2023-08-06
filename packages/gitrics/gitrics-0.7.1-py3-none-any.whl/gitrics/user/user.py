from gitrics import configuration

from glapi.connection import GitlabConnection
from glapi.user import GitlabUser

class gitricsUser(GitlabUser):
    """
    gitricsUser is a Gitlab User with opinionated enrichment for the gitrics ecosystem.
    """

    def __init__(self, id: str = None, user: dict = None, projects: list = None, connection: GitlabConnection = None, token: str = configuration.GITLAB_TOKEN, version: str = configuration.GITLAB_API_VERSION):
        """
        Args:
            connection (GitlabConnection): glapi connection
            id (string): GitLab Epic id
            projects (list): classes of GitlabProject
            token (string): GitLab personal access, ci, or deploy token
            user (dictionary): GitLab User
            version (string): GitLab API version as base url
        """

        # initialize inheritance
        super(gitricsUser, self).__init__(
            connection=connection,
            id=id,
            token=token,
            user=user,
            version=version
        )
