"""Learner scaffold: complete the TODOs; this is intentionally not a solution."""
from typing import Literal, TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.types import Command

class Snippet(TypedDict):
    text: str
    source: str

class Memo(TypedDict):
    title: str
    body: str
    footnotes: list[str]

class Verdict(TypedDict):
    decision: Literal["accept", "revise"]
    reasons: list[str]

class State(TypedDict):
    topic: str
    snippets: list[Snippet]
    draft_memo: Memo | None
    review_verdict: Verdict | None
    turn_count: int
    summary: str
    status: str

def hand_off_to_researcher() -> Command:
    return Command(goto="researcher")

def hand_off_to_writer() -> Command:
    return Command(goto="writer")

def hand_off_to_reviewer() -> Command:
    return Command(goto="reviewer")

def supervisor(state: State) -> Command[Literal["researcher", "writer", "reviewer", "__end__"]]:
    # TODO: select only typed handoff tools, enforce 8 turns and 3 rejections,
    # update/persist state after each supervisor turn, handle completion/escalation.
    raise NotImplementedError("Implement supervisor routing and persistence")

def researcher(state: State) -> Command[Literal["supervisor"]]:
    # TODO: access search_corpus using a genuine MCP stdio client; return 3–5 cited snippets.
    raise NotImplementedError("Implement MCP researcher")

def writer(state: State) -> Command[Literal["supervisor"]]:
    # TODO: use only shared state; produce a 250–350 word memo and citations.
    raise NotImplementedError("Implement writer")

def reviewer(state: State) -> Command[Literal["supervisor"]]:
    # TODO: evaluate only the memo and static rubric; return a typed verdict.
    raise NotImplementedError("Implement reviewer")

def build_graph():
    graph = StateGraph(State)
    for name, node in [("supervisor", supervisor), ("researcher", researcher), ("writer", writer), ("reviewer", reviewer)]:
        graph.add_node(name, node)
    graph.add_edge(START, "supervisor")
    return graph.compile()

def run_topic(topic: str, topic_id: str) -> dict:
    """Implement adapter contract documented in EVALUATION.md."""
    # TODO: initialise/resume state, run graph, capture metrics and MCP evidence;
    # implement rolling-summary compaction and token counting.
    raise NotImplementedError("Implement run_topic adapter")
