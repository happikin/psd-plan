from __future__ import annotations

from typing import Set

from models import GraphEdge, GraphNode, GraphPayload
from relationship_service import coauthor_edges
from repository import Repository


def build_graph_payload(repository: Repository) -> GraphPayload:
    nodes: list[GraphNode] = []
    edges: list[GraphEdge] = []
    seen_nodes: Set[str] = set()

    def add_node(node: GraphNode) -> None:
        if node.id not in seen_nodes:
            seen_nodes.add(node.id)
            nodes.append(node)

    authors_by_key = {a.name.lower(): a for a in repository.all_authors()}

    for paper in repository.all_papers():
        paper_id = f"paper:{paper.id}"
        add_node(GraphNode(id=paper_id, label=paper.title, type="paper"))

        for author in paper.authors:
            author_key = author.lower()
            author_obj = authors_by_key.get(author_key)
            author_id = f"author:{author_key}"
            add_node(
                GraphNode(
                    id=author_id,
                    label=author,
                    type="author",
                    score=author_obj.credibility_score if author_obj else 0,
                )
            )
            edges.append(GraphEdge(source=author_id, target=paper_id, relationship="written_by"))

        for keyword in paper.keywords:
            keyword_id = f"keyword:{keyword}"
            add_node(GraphNode(id=keyword_id, label=keyword, type="keyword"))
            edges.append(GraphEdge(source=paper_id, target=keyword_id, relationship="tagged_with"))

    for left, right in coauthor_edges(repository):
        edges.append(
            GraphEdge(
                source=f"author:{left.lower()}",
                target=f"author:{right.lower()}",
                relationship="coauthor",
            )
        )

    return GraphPayload(nodes=nodes, edges=edges)
