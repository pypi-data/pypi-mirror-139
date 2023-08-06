import datetime

import networkx as nx

from gitrics import configuration
from gitrics.epic import gitricsEpic
from gitrics.issue import gitricsIssue
from gitrics.project import gitricsProject
from gitrics.user.user import gitricsUser

from glapi.epic import GitlabEpic

class gitricsItemSet:
    """
    gitricsItemSet is an abstraction of a GitLab iterative concept specific to the requirements of the gitrics ecosystem.
    """

    def __init__(self, type: str, items: list = None, users: list = None, token: str = configuration.GITLAB_TOKEN, version: str = configuration.GITLAB_API_VERSION):
        """
        Args:
            items (list): classes of GitLab Epic
            token (string): GitLab personal access or deploy token
            type (enum): native GitLab object type
            users (list): dictionaries of GitLab User
            version (string): GitLab API version as base url
        """
        self.gitlab_type = type
        self.graph = None
        self.items = None
        self.users = users

        # generate default set of event action labels
        event_actions = configuration.ACTIVITY_TYPE_CODING + configuration.ACTIVITY_TYPE_COLLABORATION

        # generate gitrics objects
        if self.gitlab_type == "epic":
            self.items = [gitricsEpic(epic=d) for d in items] if items else None
        elif self.gitlab_type == "issue":
            self.items = [gitricsIssue(issue=d) for d in items] if items else None
        elif self.gitlab_type == "project":
            self.items = [gitricsProject(project=d, event_actions=event_actions, get_events=True, get_members=True, token=token, version=version) for d in items] if items else None

    def bin(self, bin: str, simple: bool = configuration.SIMPLE, visibility: str = configuration.VISIBILITY, membership: bool = configuration.MEMBERSHIP, personal: bool = configuration.PERSONAL) -> dict:
        """
        Organize objects by values of provided key.

        Args:
            bin (enum): access |
            membership (boolean): TRUE if api should query specific to the user ttached to the access token
            personal (boolean): TRUE if api should return namespace (personal) user projects only
            simple (boolean): TRUE if api return should be minimal
            visibility (enum): internal | private | public

        Returns:
            A dictionary where keys are the bin label and corresponding values are lists of dictionaries where each is a Gitlab project which fits the bin criteria.
        """

        result = dict()

        if bin == "access":

            # determine maximum access level
            max_level = int(max(configuration.USER_ACCESS_LEVELS.keys()) / 10)
            min_level = int(min(configuration.USER_ACCESS_LEVELS.keys()) / 10)

            result = dict()
            tracked = list()

            # determine what order to extract projects in
            # based on how gitlab exposes user access level
            # we have to loop through different queries to assemble by user access
            for digit in reversed(range(min_level, max_level + 1)):

                filtered = list()
                level = digit * 10

                # get projects user is a member of
                api_results = self.extract_projects(
                    access=level,
                    membership=membership,
                    personal=personal,
                    simple=simple,
                    visibility=visibility
                )

                # skip maximum level since all those project are valid to that access level
                if digit != max_level:

                    # remove projects of higher levels
                    filtered = [d for d in api_results if d["id"] not in tracked]

                # add ids to track
                for d in api_results:
                    if d["id"] not in tracked:
                        tracked.append(d["id"])

                # set value in map
                result[configuration.USER_ACCESS_LEVELS[level]] = api_results if digit == max_level else filtered

        return result

    def determine_ownership(self, items, graph: nx.DiGraph = None) -> list:
        """
        Determine opinionated ownership based on formal assignment via GitLab or highest note (comments) count.

        Args:
            graph (DiGraph): network x directional graph
            items (list): classes of gitrics<Object>

        Returns:
            A list of tuples (0,1) where 0 is a Gitlab user id; 1 is the initial ownership score based on the association of the user to the item.
        """

        result = None

        # loop through items
        for item in items:

            # assign intitial ownership
            item.ownership = self.initialize_ownership(item)

        # inherit ownership through graph descendants and ancestors
        result = self.inherit_ownership(items, graph) if graph else items

        # calculate degree centrality
        degreecentralitymap = nx.degree_centrality(graph) if graph else None

        # loop through items
        for item in result:

            # get existing tuple values
            values = item.ownership
            final_values = list()
            all_users = [gitricsUser(user=d) for d in item.membership] if hasattr(item, "membership") else self.users

            # update owner (user) scope based on weight for node centrality in the graph
            updated_values = [(d[0], self.score_ownership(d[1], degreecentralitymap[item.id])) for d in values] if graph else values

            # have to loop again since there are multiple of the same id with various scores based on ownership stakes across the graph
            for user in list(set([d[0] for d in updated_values])):

                # get values only for the user
                user_values = [d[1] for d in updated_values if d[0] == user]

                # average weighted score
                final_values.append((user, sum(user_values) / len(user_values)))

            # replace ids with full user objects
            full_users = [
                d for d in all_users
                if d.id in [x[0] for x in final_values]
            ] if all_users else list()

            # append ownership score to each GitlabUser object
            for user in full_users:
                user.score_ownership = [d for d in final_values if d[0] == user.id][0][1]

            # sort by ownership score
            item.ownership = sorted(full_users, key=lambda d: d.score_ownership, reverse=True)

        return result

    def determine_status(self, item: dict) -> str:
        """
        Determine human-readable opinionated status based on start/end/due dates and state.

        Args:
            item (dictionary): key/value pairs representing a GitLab Epic or Issue

        Returns:
            A string representing a status related to start/end time.
        """

        result = "ongoing"
        now = datetime.datetime.now()

        # opened
        if item["state"] == "opened":

            # ending date
            if "end_date" in item or "due_date" in item:

                # normalize between data types
                edate = item["end_date"] if "end_date" in item else item["due_date"]

                # end/due date in the past
                if edate and datetime.datetime.strptime(edate, configuration.DATE_ISO_8601) < now:
                    result = "past due"

            # starting date
            if "start_date" in item or "due_date" in item:

                # normalize between data types
                sdate = item["start_date"] if "start_date" in item else item["due_date"]

                # start date in the future
                if sdate and datetime.datetime.strptime(sdate, configuration.DATE_ISO_8601) > now:
                    result = "upcoming"

        # closed
        else:
            result = "complete"

        return result

    def inherit_ownership(self, items: list, graph: nx.DiGraph):
        """
        Determine the inherited ownership of an item based on its position in the graph of items.

        Args:
            graph (DiGraph): directional network x graph
            items (list): classes of gitrics<Object>

        Returns:
            A list of classes where each is a gitrics<Object>.
        """

        # map items to related nodes
        node_map = {
            d.id: [
                x for x in list(nx.descendants(graph, d.id)) + list(nx.ancestors(graph, d.id))
                if x != 0
            ] for d in items if [
                x for x in list(nx.descendants(graph, d.id)) + list(nx.ancestors(graph, d.id))
                if x != 0
            ]
        }

        # loop through items with ancestors or descendants
        for node_id in node_map:

            # get item from itemset that corresponds to the node id
            item = [d for d in items if d.id == node_id][0]

            # loop through subnodes (ancestor or decendants)
            for subnode_id in node_map[node_id]:

                # get subitem
                subitem = [d for d in items if d.id == subnode_id][0]

                # add item owners to subnode owners
                subitem.ownership = subitem.ownership + item.ownership if subitem.ownership else item.ownership

        return items

    def initialize_ownership(self, item) -> list:
        """
        Extract or set initial ownership based on formal assignment via GitLab, highest note (comments) count, or participation.

        Args:
            item (enum): gitricsEpic || GitlabIssue

        Returns:
            A list of tuples (0,1) where 0 is a Gitlab user id; 1 is the initial ownership score based on the association of the user to the item.
        """

        result = list()
        subitem = getattr(item, item.gitlab_type)

        # check for assignees
        if "assignees" in subitem and subitem["assignees"]:

            # add as assignee with score
            result = [(d["id"], 1) for d in subitem["assignees"]]

        # check for membership
        elif hasattr(item, "membership") and getattr(item, "membership"):

            # add as member with score
            result = [(d["id"], 1) for d in item.membership]

        # check for notes
        elif hasattr(item, "notes") and item.notes:

            # get author totals
            author_counts = Counter(d["author"]["id"] for d in item.notes)

            # assign ownership by comments with score based on percent of all notes
            result = [
                (k, author_counts[k] / sum(author_counts.values())) for k in author_counts
            ]

        # check for participants
        if hasattr(item, "participants") and item.participants:

            # because we can't determine level of participation
            # initialize all with lowest score
            result += [(d["id"], 0.1) for d in item.participants]

        return result

    def score_ownership(self, value: float, centrality: float):
        """
        Determine the weighted ownership score for each item in an ItemSet.

        Args:
            user (tuple): (0,1) 0 is a GitLab user id; 1 is an ownership score

        Returns:
            A float representing the weighted and normalized ownership.
        """

        result = 0
        weight = 1

        # any relationship other than explicit assignment
        if value != 1:

            # determine ownership weight based on participation and graph centrality
            weight = 1 - centrality

        # assign an ownership score to each user weighted toward assignment and notes
        # with the node degree centrality as a second weight in the itemsetgraph
        # if a user is assigned an item which is a lower level node the parent nodes up stream get smaller weights for that user
        result = value * weight

        return result
