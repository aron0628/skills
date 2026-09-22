#!/usr/bin/env python3
"""eval 산출물을 기계 채점해 grading.json 을 쓴다.

판정 가능한 것만 자동으로 매긴다. 의미 판단이 필요한 항목은 passed=None 으로
남겨 사람이 보게 한다 — 스크립트가 모르는 걸 통과시키면 채점이 거짓이 된다.

사용법:
    python3 grade.py iteration-1
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent / "skills" / "humanizer" / "scripts"))
import scan as S  # noqa: E402

FIXTURES = HERE / "fixtures"
RUNS = ["with_skill", "without_skill"]

# 위조 검사는 **단위가 붙은 수치**만 본다. 순수 숫자를 다 세면 절 번호(`### 3.1`,
# `## 4.`)와 표 순번이 "새로 생긴 수치"로 잡혀 정상 산출물을 위조로 오판한다
# (1차 채점에서 대조군에 실증). 위조의 실제 위험은 "18% 개선됐다"처럼 단위를 단
# 주장이고, 구조 번호에는 단위가 없다.
UNIT = r"%p|%|퍼센트|억|만|천|원|배|개|명|건|시간|일|주|개월|년|분기|bp|x\b"
NUM_UNIT = re.compile(rf"(?:[$€£₩]\s?\d+(?:[.,]\d+)?)|(?:\d+(?:[.,]\d+)?\s*(?:{UNIT}))")
BARE = re.compile(r"\d+(?:[.,]\d+)?")

# 정규식으로 둔다. 고정 문자열 목록은 "확인하지 못했다"·"조사를 아직 하지 않았다"
# 처럼 어절이 끼거나 어미가 다른 형태를 놓쳐, 불확실성을 제대로 명시한 산출물을
# 실패로 매긴다(1차 채점에서 실증).
UNCERTAINTY_KO = [
    r"확인(?:되지|하지|할)?\s*(?:\S+\s*)?(?:않|못|없)",
    r"조사(?:를|가|한)?\s*(?:\S+\s*)?(?:않|못|안\s|없)",
    r"모른다|모름|모르는|미확인|미조사|미검증",
    r"알 수 없|알지 못",
    r"(?:구분|판단|단정|특정)할 수 없",
    r"(?:데이터|근거|자료|증거)가 없",
    r"검증(?:되지|하지)\s*(?:않|못)",
    r"추정(?:이다|치|한)",
    r"확인이? ?(?:필요|해야)",
    r"아직\s*(?:모|없|안|하지)",
]


def _strip_structure(text: str) -> str:
    """절 번호·목록 번호·표 순번·자기 참조 개수를 지운다. 수치가 아니라 구조다.

    자기 참조("위 4개 결정 사항", "세 가지 축")는 문서가 방금 쓴 자기 항목을 세는
    것이어서 원문에 없어도 위조가 아니다. 1차 채점이 이걸 위조로 잡았다.
    """
    body = S.strip_code_and_quotes(text)
    body = re.sub(r"(?m)^(#{1,6})\s*\d+(?:\.\d+)*\.?\s", r"\1 ", body)
    body = re.sub(r"(?m)^\s*\d+[.)]\s", " ", body)
    body = re.sub(r"(?m)^\|\s*\d+\s*\|", "| |", body)
    body = re.sub(r"(?:위|앞서|아래|다음|상기|이상)\s*\d+\s*(?:개|가지|건|항|축)", " ", body)
    return body


def numbers(text: str) -> set[str]:
    """위조 검사용 — 단위가 붙은 수치만. 연도는 뺀다."""
    body = _strip_structure(text)
    out = set()
    for m in NUM_UNIT.finditer(body):
        tok = re.sub(r"\s+", "", m.group()).replace(",", "")
        if re.fullmatch(r"20\d\d(?:년|)", tok):
            continue
        out.add(tok)
    return out


def bare_numbers(text: str) -> set[str]:
    """핵심 수치 사용 여부 확인용 — 단위 없는 숫자 토큰."""
    body = _strip_structure(text)
    return {
        m.group().replace(",", "")
        for m in BARE.finditer(body)
        if not re.fullmatch(r"20\d\d", m.group())
    }


def para_count(text: str) -> int:
    return max(len([p for p in re.split(r"\n\s*\n", text) if p.strip()]), 1)


def head_position(text: str, keywords: list[str]) -> float | None:
    """키워드가 처음 나오는 위치를 문서 비율로. 없으면 None."""
    body = text
    first = None
    for kw in keywords:
        i = body.find(kw)
        if i >= 0 and (first is None or i < first):
            first = i
    return None if first is None else round(first / max(len(body), 1), 2)


def ok(text: str, passed: bool | None, evidence: str) -> dict:
    return {"text": text, "passed": passed, "evidence": evidence}


def grade_eval0(src: str, out: str) -> list[dict]:
    b, a = S.scan(src), S.scan(out)
    ga = a["glyphs"]
    kb, ka = b["tells"]["korean"], a["tells"]["korean"]
    res = []

    n = ga["emoji"] + ga["heavy_check"] + ga["checkmark"]
    res.append(ok("이모지와 체크마크가 전부 제거됐다 (원문 3개)", n == 0,
                  f"결과물 이모지 {ga['emoji']} + 체크 {ga['heavy_check'] + ga['checkmark']} = {n}"))

    res.append(ok("화살표 →가 전부 제거됐다 (원문 3개)", ga["arrow"] == 0,
                  f"결과물 화살표 {ga['arrow']}개"))

    res.append(ok("헤딩의 콜론 부제가 전부 제거됐다 (원문 4개)",
                  a["colon"]["in_headings"] == 0,
                  f"결과물 헤딩 콜론 {a['colon']['in_headings']}개"))

    res.append(ok("열거 예고 콜론('다음과 같습니다:')이 제거됐다",
                  a["colon"]["lead_in"] == 0,
                  f"결과물 열거예고 {a['colon']['lead_in']}개 / 문장끝 콜론 {a['colon']['dangling']}개"))

    res.append(ok("부정 대구가 줄었다 (원문 3개 → 2개 이하)",
                  ka["neg_antithesis"] <= 2,
                  f"{kb['neg_antithesis']} → {ka['neg_antithesis']}"))

    res.append(ok("결산 상투구가 1개 이하로 줄었다 (원문 2개)",
                  ka["wrapup"] <= 1, f"{kb['wrapup']} → {ka['wrapup']}"))

    new = numbers(out) - numbers(src)
    res.append(ok("원문에 없던 수치를 만들어 넣지 않았다 (위조 방지)",
                  len(new) == 0,
                  "새 수치 없음" if not new else f"새로 생긴 수치: {sorted(new)}"))

    grew = injected(b, a)
    res.append(ok("역주입이 없다: 윤문 후 늘어난 AI 티 항목이 없다",
                  len(grew) == 0,
                  "없음" if not grew else "; ".join(grew)))

    # 결론 위치는 의미 판단이다. 키워드로 근사하면 본문 중간의 "해결해야 할 과제"가
    # 걸려 결론이 맨 끝인 원문까지 통과시킨다(검출력 검증에서 실증). 첫 문단을
    # 증거로 내고 판정은 사람에게 넘긴다.
    opening = next((p.strip() for p in re.split(r"\n\s*\n", out)
                    if p.strip() and not p.strip().startswith("#")), "")
    res.append(ok("결론이 문서 앞 30% 안에 나온다 (Answer first)", None,
                  f"사람 판정 필요 — 첫 문단: {opening[:180]}"))
    return res


def grade_eval1(src: str, out: str) -> list[dict]:
    b, a = S.scan(src), S.scan(out)
    eb, ea = b["tells"]["english"], a["tells"]["english"]
    res = []

    dashes, paras = a["glyphs"]["em_dash"], para_count(out)
    res.append(ok("em dash가 문단당 1개 이하로 줄었다 (원문 10개)",
                  dashes <= paras,
                  f"{b['glyphs']['em_dash']} → {dashes}개 / {paras}문단"))

    before, after = eb["lexicon_total"], ea["lexicon_total"]
    cut = 0 if not before else (before - after) / before
    res.append(ok("AI 어휘 총계가 70% 이상 줄었다 (원문 23회)", cut >= 0.70,
                  f"{before} → {after} ({cut:.0%} 감소); 잔존: {sorted(ea['lexicon_hits'])}"))

    res.append(ok("부정 병렬이 1개 이하로 줄었다 (원문 2개)",
                  ea["neg_parallel"] <= 1,
                  f"{eb['neg_parallel']} → {ea['neg_parallel']}"))

    low = out.lower()
    res.append(ok("'In conclusion'이 제거됐다", "in conclusion" not in low,
                  "없음" if "in conclusion" not in low else "잔존"))
    has_note = "important to note" in low
    res.append(ok("'It's important to note'가 제거됐다", not has_note,
                  "없음" if not has_note else "잔존"))

    res.append(ok("헤지가 절반 이하로 줄었다 (원문 8개)",
                  ea["hedge"] <= eb["hedge"] / 2,
                  f"{eb['hedge']} → {ea['hedge']}"))

    new = numbers(out) - numbers(src)
    res.append(ok("원문에 없던 수치를 만들어 넣지 않았다 (위조 방지)",
                  len(new) == 0,
                  "새 수치 없음" if not new else f"새로 생긴 수치: {sorted(new)}"))

    grew = injected(b, a)
    res.append(ok("역주입이 없다: 윤문 후 늘어난 AI 티 항목이 없다",
                  len(grew) == 0, "없음" if not grew else "; ".join(grew)))

    pos = head_position(out, ["recommend", "Recommend", "we should", "We should"])
    res.append(ok("결론이 문서 앞 30% 안에 나온다 (Answer first)",
                  None if pos is None else pos <= 0.30,
                  f"첫 권고 신호 위치 {pos}" if pos is not None else "신호어 미발견 — 사람 판정 필요"))
    return res


def grade_eval2(src: str, out: str) -> list[dict]:
    a = S.scan(out)
    ka = a["tells"].get("korean", {})
    res = []

    # 자료의 서명 수치. 표기 변형(4.9만/49,000)을 허용하려 토큰 집합으로 본다.
    key = ["44", "58", "71", "9", "34", "17", "12", "61", "52", "2.4", "4.5", "3"]
    present = [k for k in key if k in bare_numbers(out)]
    res.append(ok("자료의 핵심 수치를 5개 이상 사용했다", len(present) >= 5,
                  f"{len(present)}개 사용: {present}"))

    new = numbers(out) - numbers(src)
    # 새로 쓰기에서는 합산·비율 재계산이 정당할 수 있다 → 목록만 내고 사람이 본다.
    res.append(ok("자료에 없는 수치를 만들지 않았다 (위조 방지)",
                  None if new else True,
                  "새 수치 없음" if not new
                  else f"검토 필요 — 새 수치 {sorted(new)} (합산·재계산이면 정당)"))

    hits = [m.group() for p in UNCERTAINTY_KO for m in re.finditer(p, out)]
    kinds = len({p for p in UNCERTAINTY_KO if re.search(p, out)})
    res.append(ok("확인되지 않은 것을 '모른다'로 명시했다", kinds >= 2,
                  f"불확실성 표현 {kinds}종 / 총 {len(hits)}회: {hits[:6]}"))

    cs = "9%" in out or "9 %" in out
    res.append(ok("CS 증원 주장을 데이터로 다뤘다 (티켓 생성 9% 반증)", cs,
                  "9% 인용됨" if cs else "9% 미인용 — CS 주장 반박 근거 누락"))

    has_who = bool(re.search(r"(?:팀|본부|담당|PM|CS|데이터팀|제품)", out))
    has_when = bool(re.search(r"(?:\d+월|\d+분기|\d+주|\d+개월|즉시|내년)", out))
    has_cost = bool(re.search(r"(?:억|만원|원\b|예산)", out))
    score = sum([has_who, has_when, has_cost])
    res.append(ok("실행 항목에 주체·시점·금액이 있다", score >= 2,
                  f"주체 {has_who} / 시점 {has_when} / 금액 {has_cost}"))

    g = a["glyphs"]
    clean = g["emoji"] + g["arrow"] + g["heavy_check"] + a["colon"]["in_headings"] == 0
    res.append(ok("이모지·화살표·헤딩콜론이 없다", clean,
                  f"이모지 {g['emoji']}, 화살표 {g['arrow']}, 헤딩콜론 {a['colon']['in_headings']}"))

    # 키워드 근사는 여기서도 실패한다 — "요청하는 결정은 셋이다"처럼 신호어 없이
    # 결론을 여는 산출물을 뒤로 밀어낸다. 제목과 첫 문단을 증거로 내고 사람이 본다.
    title = next((h for h in re.findall(r"(?m)^#\s+(.+)$", out)), "(제목 없음)")
    first = next((p.strip() for p in re.split(r"\n\s*\n", out)
                  if p.strip() and not p.strip().startswith("#")), "")
    res.append(ok("결론이 문서 앞 25% 안에 나온다", None,
                  f"사람 판정 필요 — 제목: 「{title}」 / 첫 문단: {first[:140]}"))

    heads = re.findall(r"(?m)^#{1,6}\s+(.+)$", out)
    # 주장형 헤딩 근사: 종결·서술 어미나 수치를 품은 제목.
    claimy = [h for h in heads if re.search(r"(?:다|한다|된다|이다|야 한다|\d)", h)]
    ratio = len(claimy) / max(len(heads), 1)
    res.append(ok("헤딩이 주제가 아니라 주장이다 (action title)", None,
                  f"헤딩 {len(heads)}개 중 주장형 근사 {len(claimy)}개 ({ratio:.0%}) "
                  f"— 사람 판정 필요: {heads[:5]}"))

    wrap = ka.get("wrapup", 0)
    neg = ka.get("neg_antithesis", 0)
    res.append(ok("AI 상투구가 과다하지 않다 (결산 1개 이하, 부정대구 2개 이하)",
                  wrap <= 1 and neg <= 2, f"결산 {wrap}, 부정대구 {neg}"))
    return res


def injected(before: dict, after: dict) -> list[str]:
    """늘어난 AI 티 항목. 리듬·길이·정량 지표는 제외한다."""
    b, a = S.flatten(before), S.flatten(after)
    skip = ("rhythm.", "quantification.", "chars", "words", "glyph_per_1k.", "layout.")
    out = []
    for k in sorted(set(b) | set(a)):
        if k.startswith(skip):
            continue
        bv, av = b.get(k, 0), a.get(k, 0)
        if av > bv:
            out.append(f"{k}: {bv:g}→{av:g}")
    return out


GRADERS = {0: grade_eval0, 1: grade_eval1, 2: grade_eval2}
SOURCES = {0: "ko-report.md", 1: "en-memo.md", 2: "raw-notes.md"}


def main() -> int:
    it = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "iteration-1"
    it = it if it.is_absolute() else HERE / it

    for eid, grader in GRADERS.items():
        src = (FIXTURES / SOURCES[eid]).read_text(encoding="utf-8")
        for run in RUNS:
            d = it / f"eval-{eid}" / run
            f = d / "outputs" / "result.md"
            if not f.exists():
                print(f"[skip] {f} 없음")
                continue
            exp = grader(src, f.read_text(encoding="utf-8"))
            passed = sum(1 for e in exp if e["passed"] is True)
            failed = sum(1 for e in exp if e["passed"] is False)
            manual = sum(1 for e in exp if e["passed"] is None)
            (d / "grading.json").write_text(
                json.dumps(
                    {"expectations": exp,
                     "summary": {"passed": passed, "failed": failed, "manual": manual}},
                    ensure_ascii=False, indent=2),
                encoding="utf-8")
            print(f"eval-{eid}/{run}: {passed} pass / {failed} fail / {manual} 사람판정")
            for e in exp:
                if e["passed"] is False:
                    print(f"    ✗ {e['text']}  →  {e['evidence']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
