from enum import StrEnum
from typing import List
from pydantic import BaseModel, Field


class AmbiguityType(StrEnum):
    UNDERSPECIFICATION = "underspecification"
    BOUNDARY_OMISSION = "boundary_omission"
    CONFLICTING_RULES = "conflicting_rules"
    LEXICAL_AMBIGUITY = "lexical_ambiguity"


class UncertaintyRecord(BaseModel):
    clause_id: str = Field(..., description="Unique ID of the clause containing ambiguity.")
    ambiguity_type: AmbiguityType = Field(..., description="Classification of the ambiguity.")
    source_text: str = Field(..., description="Exact excerpt from the raw requirements text.")
    interpretation_assumptions: List[str] = Field(
        ..., description="Assumptions made by the reasoner to resolve the ambiguity."
    )


class ClaimType(StrEnum):
    PRECONDITION = "precondition"
    POSTCONDITION = "postcondition"
    INVARIANT = "invariant"
    BEHAVIORAL = "behavioral"


class FunctionalClaim(BaseModel):
    claim_id: str = Field(..., description="Unique identifier for the claim (e.g., CLM-001).")
    clause_id: str = Field(..., description="Associated clause identifier.")
    claim_type: ClaimType = Field(..., description="Mathematical/logical role of the claim.")
    statement: str = Field(..., description="Normalized claim statement.")
    logical_arguments: List[str] = Field(
        default_factory=list,
        description="Premises or reasoning paths supporting this claim."
    )


class SemanticClause(BaseModel):
    clause_id: str = Field(..., description="Clause identifier (e.g., CLS-001).")
    raw_text: str = Field(..., description="The original prose segment.")
    claims: List[FunctionalClaim] = Field(default_factory=list)
    uncertainties: List[UncertaintyRecord] = Field(default_factory=list)


class ProseAnalysis(BaseModel):
    spec_id: str = Field(..., description="Identifier of the target specification.")
    version: str = Field(default="1.0.0")
    clauses: List[SemanticClause] = Field(default_factory=list)

    def to_markdown(self) -> str:
        """Renders the structured analysis into the Git audit trail markdown artifact."""
        lines = [
            f"# Prose Analysis Report: {self.spec_id}",
            f"**Schema Version:** {self.version}\n",
            "## 1. Extracted Semantic Clauses & Claims",
        ]
        for c in self.clauses:
            lines.append(f"### Clause `{c.clause_id}`")
            lines.append(f"> {c.raw_text}\n")
            if c.claims:
                lines.append("**Functional Claims:**")
                for clm in c.claims:
                    lines.append(f"- **[{clm.claim_id}]** (`{clm.claim_type.value}`): {clm.statement}")
                    for arg in clm.logical_arguments:
                        lines.append(f"  - *Arg:* {arg}")
            lines.append("")

        lines.append("## 2. Uncertainty Record (Ambiguities & Under-specifications)")
        uncertainties = [u for c in self.clauses for u in c.uncertainties]
        if not uncertainties:
            lines.append("_No ambiguities identified._")
        else:
            for u in uncertainties:
                lines.append(f"- **Clause `{u.clause_id}`** [{u.ambiguity_type.value}]:")
                lines.append(f"  - *Source text:* \"{u.source_text}\"")
                lines.append("  - *Assumptions made:*")
                for assumption in u.interpretation_assumptions:
                    lines.append(f"    - {assumption}")

        return "\n".join(lines)
