import argparse
from pathlib import Path
from schemas import (
    AmbiguityType,
    ClaimType,
    FunctionalClaim,
    ProseAnalysis,
    SemanticClause,
    UncertaintyRecord,
)


def parse_prose_specification(spec_id: str, raw_text: str) -> ProseAnalysis:
    """
    Parses natural language requirements into structured clausal data.
    
    In the full loop, this delegates to the Hermes Agent runtime. This harness
    validates schema serialization and verifies file output paths for the Git audit trail.
    """
    lines = [line.strip() for line in raw_text.splitlines() if line.strip() and not line.startswith("#")]
    
    clauses = []
    for idx, line in enumerate(lines, start=1):
        clause_id = f"CLS-{idx:03d}"
        claims = []
        uncertainties = []

        # Rule-based heuristic simulation of qualitative reasoning
        if "must" in line.lower() or "shall" in line.lower():
            claims.append(
                FunctionalClaim(
                    claim_id=f"CLM-{idx:03d}-1",
                    clause_id=clause_id,
                    claim_type=ClaimType.POSTCONDITION,
                    statement=line,
                    logical_arguments=["Mandated by imperative phrasing ('must'/'shall')."]
                )
            )

        # Flag common under-specification keywords
        if any(term in line.lower() for term in ["gracefully", "quickly", "appropriate", "etc."]):
            uncertainties.append(
                UncertaintyRecord(
                    clause_id=clause_id,
                    ambiguity_type=AmbiguityType.UNDERSPECIFICATION,
                    source_text=line,
                    interpretation_assumptions=[
                        "Under-specified adjective detected; concrete threshold needed in formal model."
                    ]
                )
            )

        clauses.append(
            SemanticClause(
                clause_id=clause_id,
                raw_text=line,
                claims=claims,
                uncertainties=uncertainties
            )
        )

    return ProseAnalysis(spec_id=spec_id, clauses=clauses)


def run_agent_1(spec_path: Path, output_root: Path) -> Path:
    spec_id = spec_path.stem
    raw_content = spec_path.read_text(encoding="utf-8")

    analysis = parse_prose_specification(spec_id=spec_id, raw_text=raw_content)

    # Output to spec-defined directory: formalizations/{spec-id}/prose_analysis.md
    target_dir = output_root / "formalizations" / spec_id
    target_dir.mkdir(parents=True, exist_ok=True)

    markdown_file = target_dir / "prose_analysis.md"
    markdown_file.write_text(analysis.to_markdown(), encoding="utf-8")

    return markdown_file


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Agent 1: Prose Informal Reasoner Harness")
    parser.add_argument("--spec", type=str, required=True, help="Path to raw markdown spec file")
    parser.add_argument("--out", type=str, default=".", help="Root directory of repository")
    args = parser.parse_args()

    result_path = run_agent_1(Path(args.spec), Path(args.out))
    print(f"[Agent 1] Successfully generated: {result_path}")
