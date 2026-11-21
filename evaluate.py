"""Run comparable topics; errors and unknown rubric outcomes remain explicit."""
import argparse
import json
import re
from pathlib import Path
import baseline

ROOT = Path(__file__).resolve().parent
VALID_IDS = {f"P{i:02d}" for i in range(1, 13)}

def assess(memo):
    """Automated checks cannot determine factual support or professional tone."""
    count = len(re.findall(r"\b[\w'-]+\b", memo))
    ids = re.findall(r"\[(P\d{2})\]", memo)
    checks = {"word_count": count, "length_pass": 250 <= count <= 350,
              "citation_present": bool(ids), "invalid_citations": sorted(set(ids) - VALID_IDS)}
    checks["automatic_checks_pass"] = checks["length_pass"] and checks["citation_present"] and not checks["invalid_citations"]
    checks["rubric_pass"] = None  # Human review must assess grounding, tone and all claims.
    return checks

def run_one(fn, topic):
    try:
        result = fn(topic["topic"], topic["id"])
        if not isinstance(result, dict) or not isinstance(result.get("memo"), str):
            raise ValueError("Adapter must return a dict with memo text")
        result["checks"] = assess(result["memo"])
        return result
    except Exception as exc:
        # Avoid exposing provider error bodies, which may contain private data.
        return {"topic_id": topic["id"], "status": "error", "error_type": type(exc).__name__,
                "checks": {"rubric_pass": None}}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="results/evaluation.json")
    args = parser.parse_args()
    topics = json.loads((ROOT / "topics.json").read_text(encoding="utf-8"))
    try:
        from team import run_topic as team_run
    except ImportError:
        def team_run(topic, topic_id):
            raise RuntimeError("Install starter requirements to run the team")
    output = {"note": "Complete manual rubric review and compute ratio as described in EVALUATION.md.",
              "baseline": [run_one(baseline.run_topic, t) for t in topics],
              "multi_agent": [run_one(team_run, t) for t in topics]}
    path = Path(args.output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(output, indent=2), encoding="utf-8")
    print(f"Wrote {path}. Review status and error_type for each run; see EVALUATION.md.")

if __name__ == "__main__":
    main()
