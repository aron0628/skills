#!/usr/bin/env python3
"""grading.json 들을 모아 benchmark.json / benchmark.md 를 만든다.

사람 판정 항목(passed=null)은 pass_rate 분모에서 뺀다. 자동 판정이 모르는 것을
통과로 세면 비율이 부풀고, 실패로 세면 스킬이 억울해진다.

사용법: python3 make_benchmark.py iteration-1
"""

from __future__ import annotations

import datetime as dt
import json
import statistics
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CONFIGS = ["with_skill", "without_skill"]


def agg(vals: list[float]) -> dict:
    if not vals:
        return {"mean": 0, "stddev": 0, "min": 0, "max": 0}
    return {
        "mean": round(statistics.mean(vals), 3),
        "stddev": round(statistics.pstdev(vals), 3) if len(vals) > 1 else 0.0,
        "min": round(min(vals), 3),
        "max": round(max(vals), 3),
    }


def main() -> int:
    it = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "iteration-1"
    it = it if it.is_absolute() else HERE / it

    runs, by_cfg = [], {c: {"pr": [], "t": [], "tok": []} for c in CONFIGS}

    for eval_dir in sorted(it.glob("eval-*")):
        meta_f = eval_dir / "eval_metadata.json"
        meta = json.loads(meta_f.read_text(encoding="utf-8")) if meta_f.exists() else {}
        for cfg in CONFIGS:
            gf = eval_dir / cfg / "grading.json"
            if not gf.exists():
                continue
            g = json.loads(gf.read_text(encoding="utf-8"))
            exp = g.get("expectations", [])
            auto = [e for e in exp if e.get("passed") is not None]
            passed = sum(1 for e in auto if e["passed"])
            failed = len(auto) - passed
            pr = passed / len(auto) if auto else 0.0

            tf = eval_dir / cfg / "timing.json"
            tm = json.loads(tf.read_text(encoding="utf-8")) if tf.exists() else {}
            secs = tm.get("total_duration_seconds", 0) or (tm.get("duration_ms", 0) / 1000)
            toks = tm.get("total_tokens", 0)

            runs.append({
                "eval_id": meta.get("eval_id"),
                "eval_name": meta.get("eval_name", eval_dir.name),
                "configuration": cfg,
                "run_number": 1,
                "result": {
                    "pass_rate": round(pr, 3),
                    "passed": passed,
                    "failed": failed,
                    "manual": len(exp) - len(auto),
                    "total": len(auto),
                    "time_seconds": round(secs, 1),
                    "tokens": toks,
                    "errors": 0,
                },
                "expectations": exp,
            })
            by_cfg[cfg]["pr"].append(pr)
            if secs:
                by_cfg[cfg]["t"].append(secs)
            if toks:
                by_cfg[cfg]["tok"].append(toks)

    summary: dict[str, dict] = {
        c: {
            "pass_rate": agg(by_cfg[c]["pr"]),
            "time_seconds": agg(by_cfg[c]["t"]),
            "tokens": agg(by_cfg[c]["tok"]),
        }
        for c in CONFIGS
    }
    w, o = summary["with_skill"], summary["without_skill"]
    summary["delta"] = {
        "pass_rate": f"{w['pass_rate']['mean'] - o['pass_rate']['mean']:+.3f}",
        "time_seconds": f"{w['time_seconds']['mean'] - o['time_seconds']['mean']:+.1f}",
        "tokens": f"{w['tokens']['mean'] - o['tokens']['mean']:+.0f}",
    }

    # 비판별 assertion 찾기 — 양쪽 구성에서 똑같이 통과하면 스킬 가치를 못 재는 항목.
    notes = []
    per_text: dict[str, dict[str, list[bool]]] = {}
    for r in runs:
        for e in r["expectations"]:
            if e.get("passed") is None:
                continue
            per_text.setdefault(e["text"], {}).setdefault(r["configuration"], []).append(e["passed"])
    for text, cfgs in per_text.items():
        wv, ov = cfgs.get("with_skill", []), cfgs.get("without_skill", [])
        if wv and ov and all(wv) and all(ov):
            notes.append(f"비판별: '{text[:60]}' 는 양쪽 다 통과 — 스킬 가치를 재지 못한다")

    bench = {
        "metadata": {
            "skill_name": "humanizer",
            "skill_path": str(HERE.parent.parent / "skills" / "humanizer"),
            "timestamp": dt.datetime.now(dt.timezone.utc).isoformat(),
            "evals_run": sorted({r["eval_id"] for r in runs if r["eval_id"] is not None}),
            "runs_per_configuration": 1,
        },
        "runs": runs,
        "run_summary": summary,
        "notes": notes,
    }
    (it / "benchmark.json").write_text(
        json.dumps(bench, ensure_ascii=False, indent=2), encoding="utf-8")

    L = ["# humanizer benchmark", "", "| eval | 구성 | 통과율 | pass | fail | 사람판정 |",
         "|---|---|---|---|---|---|"]
    for r in runs:
        x = r["result"]
        L.append(f"| {r['eval_name']} | {r['configuration']} | {x['pass_rate']:.0%} "
                 f"| {x['passed']} | {x['failed']} | {x['manual']} |")
    L += ["", "## 요약", "",
          f"- with_skill 통과율 평균 **{w['pass_rate']['mean']:.0%}** "
          f"(±{w['pass_rate']['stddev']:.0%})",
          f"- without_skill 통과율 평균 **{o['pass_rate']['mean']:.0%}** "
          f"(±{o['pass_rate']['stddev']:.0%})",
          f"- 차이 **{summary['delta']['pass_rate']}**"]
    if notes:
        L += ["", "## 관찰", ""] + [f"- {n}" for n in notes]
    (it / "benchmark.md").write_text("\n".join(L) + "\n", encoding="utf-8")

    print("\n".join(L))
    return 0


if __name__ == "__main__":
    sys.exit(main())
