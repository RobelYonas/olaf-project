import argparse
import subprocess
import sys
from pathlib import Path
from agent_1_harness import run_agent_1
from agent_2_harness import run_agent_2
from agent_3_harness import run_agent_3


def run_git_command(args: list[str], cwd: Path) -> str:
    res = subprocess.run(["git"] + args, cwd=cwd, capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"Git command failed: {' '.join(args)}\n{res.stderr}")
    return res.stdout.strip()


def execute_bounded_tick(spec_id: str, repo_root: Path) -> None:
    spec_path = repo_root / "specs" / f"{spec_id}.md"
    if not spec_path.exists():
        raise FileNotFoundError(f"Specification not found: {spec_path}")

    print(f"=== [Tick Start] Executing OAIF bounded unit of work for {spec_id} ===")

    # 1. Ensure Git identity is established for the audit trail
    run_git_command(["config", "user.name", "OAIF Ephemeral Worker"], cwd=repo_root)
    run_git_command(["config", "user.email", "worker@oaif.local"], cwd=repo_root)

    # 2. Agent 1: Informal Prose Reasoner
    print("\n--- Running Agent 1 (Prose Informal Reasoner) ---")
    prose_path = run_agent_1(spec_path, repo_root)
    print(f"Agent 1 generated: {prose_path}")

    # 3. Agent 2: Executable Specification Synthesizer
    print("\n--- Running Agent 2 (Executable Spec Synthesizer) ---")
    model_path = run_agent_2(spec_id, repo_root)
    print(f"Agent 2 generated & verified: {model_path}")

    # 4. Agent 3: Tri-Consistency & Meta-Evaluator
    print("\n--- Running Agent 3 (Tri-Consistency Evaluator) ---")
    eval_path = run_agent_3(spec_id, repo_root)
    print(f"Agent 3 generated: {eval_path}")

    # 5. Git-Ops Audit Trail: Stage and commit all generated artifacts
    print("\n--- Finalizing Git-Ops Audit Commit ---")
    run_git_command(["add", "formalizations/", "agent_configs/skills/"], cwd=repo_root)

    status = run_git_command(["status", "--porcelain"], cwd=repo_root)
    if status:
        commit_msg = f"audit({spec_id}): complete formalization loop and consistency evaluation"
        run_git_command(["commit", "-m", commit_msg], cwd=repo_root)
        commit_hash = run_git_command(["rev-parse", "--short", "HEAD"], cwd=repo_root)
        print(f"Committed tick artifacts to Git audit trail: [{commit_hash}] {commit_msg}")
    else:
        print("No filesystem changes detected; working tree clean.")

    print(f"=== [Tick Complete] Worker finished bounded unit of work for {spec_id} ===")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="OAIF Bounded Tick Runner")
    parser.add_argument("--spec-id", type=str, required=True, help="Target spec ID")
    parser.add_argument("--repo-root", type=str, default=".", help="Root of Git repository")
    args = parser.parse_args()

    execute_bounded_tick(args.spec_id, Path(args.repo_root).resolve())
