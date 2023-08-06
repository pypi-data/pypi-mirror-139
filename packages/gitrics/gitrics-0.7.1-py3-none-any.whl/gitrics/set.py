import networkx as nx

from gitrics.epic import gitricsEpic
from gitrics.issue import gitricsIssue
from gitrics.itemset import gitricsItemSet
from gitrics.user.user import gitricsUser

class gitricsItemSource:
    """
    gitricsItemSource is an abstraction of a GitLab aggregate concept specific to the requirements of the gitrics ecosystem.
    """

    def __init__(self, source, items):
        """
        Args:
            item (enum): gitrics<Object>
            type (enum): native GitLab object type
        """
        self.gitlab_type = list(source.keys())[0] if source else None

        # get api attrs if available
        connection = source[self.gitlab_type].connection if source and self.gitlab_type else None
        token = connection.token if connection else None
        users = source[self.gitlab_type].users if hasattr(source[self.gitlab_type], "users") else None
        version = connection.version if connection else None

        # set the item object
        setattr(self, self.gitlab_type, source[self.gitlab_type] if source else None)

        # initialize itemsets
        for key in items:

            setattr(self, "%ss" % key, gitricsItemSet(type=key, items=items[key], users=users, token=token, version=version))

    def determine_most_at_risk(self, items: list) -> list:
        """
        Determine which Epics are most at risk based on health status at_risk attributes.

        Args:
            items (list): classes of gitricsEpic

        Returns:
            A list of giticsEpic objects where each represents a GitLab Epic.
        """

        # generate maps of ids to scores
        atriskmap = { k.id: k.score_at_risk for k in items }

        # determine scoring ranks
        return [d for d in items if d.score_at_risk == atriskmap[max(atriskmap, key=atriskmap.get)]]

    def determine_most_on_track(self, items: list) -> list:
        """
        Determine which Epics are most on track based on health status on_track attributes.

        Args:
            items (list): classes of gitricsEpic

        Returns:
            A list of giticsEpic objects where each represents a GitLab Epic.
        """

        # generate maps of ids to scores
        ontrackmap = { k.id: k.score_on_track for k in items }

        # determine scoring ranks
        return [d for d in items if d.score_on_track == ontrackmap[max(ontrackmap, key=ontrackmap.get)]]

    def determine_top_blockers(self, graph: nx.DiGraph):
        """
        Determine which issues are blocking the most issues inside the group.

        Args:
            graph (DiGraph): networkx directional graph

        Returns:
            A list of gitricsIssue where each represents a GitLab Issue.
        """

        # calculate degree centrality
        degreecentralitymap = nx.degree_centrality(graph)

        # remove root node
        degreecentralitymap.pop(0)

        # get max value
        max_block_centrality = max(degreecentralitymap, key=degreecentralitymap.get)

        # update individual issues with score
        for i in self.issues.items:
            i.score_degree_centrality = degreecentralitymap[i.id] if i.id in degreecentralitymap else 0

        # get any nodes with max value
        # sort by nest level which assumes that nodes with an even score that the higher in the tree the more of a blocker it is
        return sorted([
            d for d in self.issues.items
            if d.score_degree_centrality > 0 and
            degreecentralitymap[d.id] == degreecentralitymap[max_block_centrality]
        ], key=lambda d: nx.descendants(graph, d.id), reverse=True)

    def initialize_epics(self, epics: list) -> list:
        """
        Initialize epics as gitrics objects.

        Args:
            epics (list): classes of GitlabEpic

        Returns:
            A tuple (0, 1) where 0 is a list of gitricsEpic objects where each represents a GitLab Epic and 1 is a networkx directional graph object representing the parent/child relationships in the set of epics.
        """

        graph = None
        items = None

        # build tuples of parent nodes
        parents = [(d.epic["parent_id"], d.id) for d in epics if d.epic["parent_id"]]

        # build tuples of unlinked nodes
        # i.e. direct children of root
        unlinked = [(0, d.id) for d in epics if d.epic["parent_id"] is None]

        # combine into list of links
        links = parents + unlinked

        # generate graph
        if links: graph = nx.DiGraph(links)

        # format result for gitrics
        items = [
            gitricsEpic(
                epic=d.epic,
                group_graph=graph,
                notes=d.notes if hasattr(d, "notes") else None,
                ownership=d.ownership if hasattr(d, "ownership") else None
            ) for d in epics
        ]

        return (items, graph)

    def initialize_issues(self, issues: list = None) -> list:
        """
        Initialize issues as gitrics objects.

        Args:
            issues (list): dictionaries of GitLab Issue

        Returns:
            A list of gitricsIssue objects where each represents a GitLab Issue.
        """

        graph = None
        items = None

        # generate gitrics objects
        issues = [
            gitricsIssue(issue=d)
            for d in issues
        ] if issues and isinstance(issues[0], dict) else issues

        # build blocker tuples
        blockers = [
            x for y in [
                [
                    (d.id, i["id"])
                    for i in d.links
                    if i["link_type"] == "blocks"
                ]
                for d in issues if d.links
            ] for x in y
        ] if issues else list()

        # build tuples of blockers which are unblocked themselves
        # i.e. these nodes are direct children of the root
        unblocked_blockers = [
            (0, d.id)
            for d in issues
            if d.links
            and len([
                i for i in d.links
                if i["link_type"] == "is_blocked_by"]) == 0
                and len([
                    i for i in d.links if i["link_type"] == "blocks"
                ]) > 0
        ] if issues else list()

        # build relates to tuples
        # issues with relates to connections and without other connection
        relates_to_linked = [
            x for y in [
                [
                    (d.id, i["id"])
                    for i in d.links
                    if i["link_type"] == "relates_to"
                ]
                for d in issues if d.links
            ] for x in y
        ] if issues else list()

        relates_to_unlinked = [(0, d[0]) for d in relates_to_linked]

        # build tuples for complete unlinked issues
        # i.e. nodes are direct children of the root
        unlinked = [(0, d.id) for d in issues if not d.links] if issues else list()

        # combine list
        links = blockers + unblocked_blockers + relates_to_linked + relates_to_unlinked + unlinked

        # generate graph
        if links: graph = nx.DiGraph(links)

        # format result for gitrics
        items = [
            gitricsIssue(
                issue=d.issue,
                group_graph=graph,
                notes=d.notes if hasattr(d, "notes") else None,
                ownership=d.ownership if hasattr(d, "ownership") else None
            ) for d in issues
        ]

        return (items, graph)

    def prune(self, items: list, param: dict, keep_matches: bool = True, query_starts_with: bool = False) -> list:
        """
        Prune data by provided parameter.

        Args:
            items (list): classes of gitricsEpic or GitlabIssue
            param (dict): key/value pairs where each key is an attribute to filter on and corresponding value is the desired query value
            keep_matches (boolean): TRUE if prune method retains items in set based on positive truthy results vice removing those items from set
            query_starts_with (boolean): TRUE if prune method tests provided params for startswith against param key

        Returns:
            A list of where each represents a gitricsEpic or GitlabIssue, depending on the input.
        """

        result = items

        # loop through param keys
        for key in param:

            # determine attribute type to filter against
            class_type = "user" if key == "ownership" else None

            # check param
            if keep_matches:

                # keep matches
                subset = [
                    d for d in result
                    if getattr(d, key)
                    and param[key] in [
                        getattr(x, class_type)["id"]
                        for x in getattr(d, key)
                    ]
                ]

            # remove matches
            else:

                # on class
                subset = [
                    d for d in items
                    if (
                        query_starts_with and (
                            (hasattr(d, key) and not getattr(d, key).startswith(param[key]))
                            or
                            (not hasattr(d, key) and not any(getattr(d, d.gitlab_type)[key].startswith(x) for x in param[key]))
                        )
                    )
                    or (
                        not query_starts_with and (
                            (hasattr(d, key) and getattr(d, key) not in param[key])
                            or
                            (not hasattr(d, key) and getattr(d, d.gitlab_type)[key] not in param[key])
                        )
                    )
                ]

            # update result
            result = subset

        return result
