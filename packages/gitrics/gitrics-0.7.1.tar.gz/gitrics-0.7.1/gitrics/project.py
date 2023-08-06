from gitrics import configuration

from glapi.project import GitlabProject

class gitricsProject(GitlabProject):
    """
    gitricsProject is a Gitlab Project with opinionated enrichment for the gitrics ecosystem.
    """

    def __init__(self, id: str = None, project: dict = None, event_actions: list = None, ownership: list = None, get_events: bool = False, get_members: bool = False, token: str = configuration.GITLAB_TOKEN, version: str = configuration.GITLAB_API_VERSION):
        """
        Args:
            get_events (bool): TRUE if should pull events
            get_members (bool): TRUE if should pull user membership
            event_actions (list): strings of Gitlab User contribution types https://docs.gitlab.com/ee/user/index.html#user-contribution-events
            id (string): GitLab Project id
            ownership (list): classes of GitlabUser
            project (dictionary): GitLab Project
            token (string): GitLab personal access, ci, or deploy token
            version (string): GitLab API version as base url
        """
        self.gitlab_type = "project"
        self.ownership = ownership

        # initialize inheritance
        super(gitricsProject, self).__init__(
            event_actions=event_actions,
            get_events=get_events,
            get_members=get_members,
            project=project,
            token=token,
            version=version
        )
