#!/usr/bin/env python3
"""표면 AI 티를 센다. 판정은 하지 않는다.

이 스크립트가 존재하는 이유: LLM 은 개수를 못 센다. "em dash 를 다 없앴다"고
믿으면서 3개를 남긴다. 그래서 세는 일은 코드가 하고, 무엇을 고칠지는 사람과
모델이 판단한다. 출력은 근거이지 명령이 아니다.

사용법:
    python3 scan.py draft.md                 # 리포트
    python3 scan.py draft.md --json          # 기계 판독용
    python3 scan.py before.md --diff after.md  # 윤문 전후 비교 (역주입 검출)
"""

from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
import unicodedata
from pathlib import Path

# ── 타이포그래피: 양 언어 공통 ──────────────────────────────────────────────
# 문자 자체가 죄는 아니다. 밀도가 신호다. 임계는 references/typography.md 근거.
GLYPHS = {
    "em_dash": "—",          # —
    "en_dash": "–",          # –
    "middot": "·",           # ·  한국어 AI 글의 최빈 장식
    "bullet_char": "•",      # •
    "arrow": "→",            # →
    "ellipsis_char": "…",    # …
    "lquote_d": "“",         # "
    "rquote_d": "”",         # "
    "lquote_s": "‘",         # '
    "rquote_s": "’",         # '
    "nbsp": " ",             # 비단절 공백
    "checkmark": "✓",        # ✓
    "heavy_check": "✅",      # ✅
}

# ── 영어 AI 어휘 ────────────────────────────────────────────────────────────
# PubMed 14.2M 초록 실측에서 2023 이후 급증한 어휘 + 편집자 합의 목록.
EN_LEXICON = [
    "delve", "delving", "tapestry", "realm", "landscape", "leverage",
    "leveraging", "robust", "seamless", "seamlessly", "multifaceted",
    "showcase", "showcasing", "foster", "fostering", "underscore",
    "underscores", "underscoring", "meticulous", "meticulously", "intricate",
    "ever-evolving", "ever-changing", "embark", "harness", "harnessing",
    "unlock", "unlocking", "paradigm", "synergy", "cutting-edge",
    "game-changer", "pivotal", "testament", "holistic", "streamline",
    "utilize", "utilizing", "furthermore", "moreover", "navigating",
    "in conclusion", "it is important to note", "it's important to note",
    "in today's fast-paced", "at the end of the day", "dive into",
    "crucial", "vital", "transformative", "groundbreaking", "innovative",
]

# 부정 병렬 — 영어 조사·한국어 조사 모두 같은 수사. 실측상 가장 강한 신호군.
EN_NEG_PARALLEL = [
    r"\bnot just\b", r"\bnot merely\b", r"\bnot simply\b",
    r"\bnot only\b[^.]{0,80}\bbut\b", r"\bmore than just\b",
    r"\bisn't just\b", r"\bit's not\b[^.]{0,60}\bit's\b",
]

# 수치 없는 강조 — 맥킨지 문체가 가장 싫어하는 축. "상당히"는 데이터가 아니다.
EN_VAGUE_INTENSIFIER = [
    r"\bsignificantly\b", r"\bsubstantially\b", r"\bdramatically\b",
    r"\bconsiderably\b", r"\bvastly\b", r"\bmarkedly\b", r"\bgreatly\b",
]
EN_HEDGE = [
    r"\bmay\b", r"\bmight\b", r"\bcould potentially\b", r"\bperhaps\b",
    r"\bit could be argued\b", r"\bsomewhat\b", r"\brelatively\b",
    r"\btend to\b", r"\bgenerally speaking\b",
]

# ── 한국어 AI 티 ────────────────────────────────────────────────────────────
# humanize-korean v2.3 taxonomy 에서 실측 분리도가 확인된 항목만 옮겼다.
KO_PATTERNS = {
    # C-11: 단일 지표 최강 분리도 4.84배 (KatFish, 인간 4.10% vs AI 19.83%)
    "conj_comma": r"(?:고|며|지만|면서|아서|어서|는데|으며|이며|거나|든지),",
    # C-8: 부정 대구. AI 5.8 vs 인간 0.6 = 9.2배 (G²=41.7, p<0.0001)
    "neg_antithesis": r"(?:이|가|은|는|것이|것은)?\s*아니라|것은 아니다|라기보다",
    # D-1: 결산 lexicon. 3회 초과부터 신호
    "wrapup": r"결론적으로|이를 통해|그러므로|요약하면|정리하자면|종합하면",
    # A-7 / A-8: 직역 및 이중 피동
    "have_literal": r"가지고 있(?:다|으며|는)",
    "double_passive": r"되어진|되어졌|지게 된다",
    # A-2 / A-3: 대표 번역투
    "via_through": r"를 통(?:해|하여)|을 통(?:해|하여)",
    "in_regard": r"에 있어(?:서)?|에 대(?:해|하여)서?",
    # A-10: 완곡 반복 (4회+ 부터 리듬 지배).
    # "할 수 있"으로 좁히면 "검토될 수 있습니다"·"효과적일 수 있습니다"를 놓친다.
    "can_do": r"[가-힣]\s?수\s?있",
    # D-4: hype 어휘
    "hype": r"혁신적|획기적|압도적|파격적|폭발적|전례 없는|괄목할",
    # D-2: 의의 과장
    "significance": r"시사하는 바가 크|주목할 만하|매우 중요하|의미가 크",
    # F-5: "~적 N" 추상 체인
    "jeok_chain": r"[가-힣]적 [가-힣]{2,}",
    # I-2 / I-3 / D-8: 형식명사 분열문
    "cleft": r"(?:필요한|중요한|핵심은|문제는|관건은)[^.]{0,30}(?:것은|점은|것이다|점이다)",
    # H-1: 문두 접속사
    "opener_conj": r"(?:^|\n)\s*(?:또한|따라서|즉|나아가|아울러|게다가|더욱이|한편)",
    # D-6: 결말 공식
    "closing_formula": r"할 때(?:입니다|이다)|시점(?:입니다|이다)|순간(?:입니다|이다)",
    # 수치 없는 강조
    "vague_intensifier": r"상당히|크게|대폭|현저히|눈에 띄게|비약적으로",
}

CJK = re.compile(r"[가-힣]")


def read(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def is_korean(text: str) -> bool:
    """한글 음절이 전체 문자의 10%를 넘으면 한국어로 본다."""
    if not text:
        return False
    return len(CJK.findall(text)) / max(len(text), 1) > 0.10


def strip_code_and_quotes(text: str) -> str:
    """코드 블록과 발화 표지가 붙은 직접 인용은 집계에서 뺀다.

    인용문 안의 em dash 는 원저자의 것이고, 코드 안의 화살표는 문법이다.
    이걸 세면 고치라고 보고하게 되고, 고치면 원문이 훼손된다.
    """
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"`[^`]*`", " ", text)
    return text


def sentences(text: str) -> list[str]:
    """문장 단위로 쪼갠다. 줄바꿈도 경계로 쓴다.

    마침표만 경계로 삼으면 불릿 목록 다섯 줄이 한 문장으로 뭉쳐 "최장 477자"
    같은 허위 리듬 지표가 나온다. 리듬 판정이 그 수치를 보고 "장단 혼합이
    충분하다"고 오판하므로, 각 행을 독립 단위로 본다.
    """
    out: list[str] = []
    for line in text.split("\n"):
        line = re.sub(r"^\s*(?:[-*+•]\s+|#{1,6}\s+|\d+[.)]\s+)", "", line).strip()
        if not line:
            continue
        for part in re.split(r"(?<=[.!?。])\s+", line):
            part = part.strip()
            if len(part) > 1:
                out.append(part)
    return out


def words(text: str) -> int:
    return max(len(text.split()), 1)


def count_emoji(text: str) -> int:
    return sum(
        1
        for ch in text
        if unicodedata.category(ch) == "So" and ord(ch) > 0x2100
    )


def scan(raw: str) -> dict:
    body = strip_code_and_quotes(raw)
    sents = sentences(body)
    n_words = words(body)
    per_1k = 1000.0 / n_words
    korean = is_korean(body)

    glyphs = {name: body.count(ch) for name, ch in GLYPHS.items()}
    glyphs["emoji"] = count_emoji(body)

    # 콜론 종결 — 사용자가 지목한 "끝에 : 붙이는 것".
    # 열거를 예고하는 콜론과 시각·비율 콜론(10:30, 3:1)을 구분한다.
    colon_dangling = len(re.findall(r"[^\s\d]:\s*(?:\n|$)", body))
    colon_lead_in = len(
        re.findall(r"(?:다음과 같|아래와 같|as follows|the following)[^.\n]{0,12}:", body)
    )

    bold = len(re.findall(r"\*\*[^*\n]+\*\*", body))
    bullets = len(re.findall(r"(?:^|\n)\s*[-*+•]\s+", body))
    headings = re.findall(r"(?:^|\n)#{1,6}\s+(.+)", body)
    colon_headings = sum(1 for h in headings if ":" in h or "：" in h)

    lengths = [len(s) for s in sents] or [0]
    rhythm = {
        "sentences": len(sents),
        "mean_len": round(statistics.mean(lengths), 1),
        "stdev_len": round(statistics.pstdev(lengths), 1) if len(lengths) > 1 else 0.0,
        "max_len": max(lengths),
        # 길이 분산이 죽으면 메트로놈처럼 읽힌다. 인간 산문은 보통 0.45 이상.
        "cv": round(statistics.pstdev(lengths) / statistics.mean(lengths), 2)
        if len(lengths) > 1 and statistics.mean(lengths)
        else 0.0,
        "comma_sentence_ratio": round(
            sum(1 for s in sents if "," in s) / max(len(sents), 1), 2
        ),
    }

    lang: dict[str, dict] = {}
    if korean:
        lang["korean"] = {
            k: len(re.findall(p, body)) for k, p in KO_PATTERNS.items()
        }
    low = body.lower()
    en_lex = {w: low.count(w) for w in EN_LEXICON if low.count(w)}
    lang["english"] = {
        "lexicon_hits": en_lex,
        "lexicon_total": sum(en_lex.values()),
        "neg_parallel": sum(
            len(re.findall(p, low)) for p in EN_NEG_PARALLEL
        ),
        "vague_intensifier": sum(
            len(re.findall(p, low)) for p in EN_VAGUE_INTENSIFIER
        ),
        "hedge": sum(len(re.findall(p, low)) for p in EN_HEDGE),
        # 조동사와 분사 사이에 부사가 끼는 게 흔하다("are somewhat overwhelmed").
        # 부사 한 개를 허용하고 be 원형도 포함한다("will be circulated").
        "passive": len(
            re.findall(
                r"\b(?:is|are|was|were|be|been|being)\s+(?:\w+ly\s+)?\w+(?:ed|en)\b",
                low,
            )
        ),
    }

    # 수치 밀도 — 맥킨지 문체의 유일한 정량 대리 지표.
    # 주장만 있고 숫자가 없으면 "so what" 이 비어 있다는 뜻이다.
    # 통화 기호는 숫자 앞에 오고($25M), 기간·배수는 뒤에 온다(30 days, 3x).
    numerals = len(
        re.findall(
            r"[$€£₩]\s?\d|"
            r"\d+(?:[.,]\d+)?\s*(?:%|퍼센트|배|억|만|천|원|bp|x\b|배수)|"
            r"\d+\s*(?:days?|weeks?|months?|years?|hours?|일|주|개월|년|시간|명|건)\b",
            body,
            flags=re.I,
        )
    )

    return {
        "language": "korean" if korean else "english",
        "chars": len(raw),
        "words": n_words,
        "glyphs": glyphs,
        "glyph_per_1k": {
            k: round(v * per_1k, 2) for k, v in glyphs.items() if v
        },
        "colon": {
            "dangling": colon_dangling,
            "lead_in": colon_lead_in,
            "in_headings": colon_headings,
        },
        "layout": {
            "bold": bold,
            "bullets": bullets,
            "headings": len(headings),
            "bold_per_1k": round(bold * per_1k, 1),
        },
        "rhythm": rhythm,
        "tells": lang,
        "quantification": {
            "numeric_claims": numerals,
            "per_1k": round(numerals * per_1k, 1),
        },
    }


def flatten(d: dict, prefix: str = "") -> dict[str, float]:
    """diff 비교용으로 중첩 카운트를 평평하게 만든다."""
    out: dict[str, float] = {}
    for k, v in d.items():
        key = f"{prefix}{k}"
        if isinstance(v, dict):
            out.update(flatten(v, f"{key}."))
        elif isinstance(v, (int, float)):
            out[key] = v
    return out


def report(r: dict) -> str:
    L: list[str] = []
    L.append(f"언어: {r['language']}  |  {r['chars']}자 / {r['words']}어")
    L.append("")

    g = {k: v for k, v in r["glyphs"].items() if v}
    L.append("[타이포그래피]")
    L.append("  " + (", ".join(f"{k}={v}" for k, v in g.items()) if g else "검출 없음"))
    c = r["colon"]
    L.append(
        f"  콜론: 문장끝 {c['dangling']} / 열거예고 {c['lead_in']} / 헤딩 {c['in_headings']}"
    )
    lay = r["layout"]
    L.append(
        f"  볼드 {lay['bold']}회 ({lay['bold_per_1k']}/1000어), "
        f"불릿 {lay['bullets']}행, 헤딩 {lay['headings']}개"
    )
    L.append("")

    rh = r["rhythm"]
    L.append("[리듬]")
    L.append(
        f"  {rh['sentences']}문장, 평균 {rh['mean_len']}자, 편차 {rh['stdev_len']}, "
        f"변동계수 {rh['cv']}, 최장 {rh['max_len']}자"
    )
    L.append(f"  쉼표 포함 문장 비율 {rh['comma_sentence_ratio']}")
    L.append("")

    if "korean" in r["tells"]:
        hits = {k: v for k, v in r["tells"]["korean"].items() if v}
        L.append("[한국어 AI 티]")
        L.append("  " + (", ".join(f"{k}={v}" for k, v in hits.items()) if hits else "검출 없음"))
        L.append("")

    en = r["tells"]["english"]
    if en["lexicon_total"] or en["neg_parallel"] or en["vague_intensifier"]:
        L.append("[영어 AI 티]")
        if en["lexicon_hits"]:
            top = sorted(en["lexicon_hits"].items(), key=lambda x: -x[1])[:12]
            L.append("  어휘: " + ", ".join(f"{w}={n}" for w, n in top))
        L.append(
            f"  부정병렬 {en['neg_parallel']}, 막연강조 {en['vague_intensifier']}, "
            f"헤지 {en['hedge']}, 수동태 {en['passive']}"
        )
        L.append("")

    q = r["quantification"]
    L.append(f"[정량] 수치 주장 {q['numeric_claims']}건 ({q['per_1k']}/1000어)")
    return "\n".join(L)


def diff_report(before: dict, after: dict) -> str:
    """윤문이 새 AI 티를 만들지 않았는지 본다.

    실측 근거: humanize-korean v2.6.3 회차에서 오염쌍 28편 중 2편이 윤문 **후**
    연결어미 쉼표가 오히려 늘었다(2→3, 4→7). 문장을 다시 쓰는 동안 편집 모델이
    같은 습관을 재현한다. 총량이 줄어도 새로 심은 것이 있으면 실패다.
    """
    b, a = flatten(before), flatten(after)
    rows: list[tuple[str, int, int, int]] = []
    for k in sorted(set(b) | set(a)):
        bv, av = int(b.get(k, 0)), int(a.get(k, 0))
        if bv or av:
            rows.append((k, bv, av, av - bv))

    L = ["[윤문 전후 비교]  (+ 는 새로 심은 것 = 역주입)", ""]
    injected = [r for r in rows if r[3] > 0 and not r[0].startswith(("rhythm.", "quantification.", "chars", "words"))]
    improved = [r for r in rows if r[3] < 0]

    if injected:
        L.append("⚠ 늘어난 항목 (재작성 필요):")
        for k, bv, av, d in sorted(injected, key=lambda x: -x[3]):
            L.append(f"    {k}: {bv} → {av}  (+{d})")
    else:
        L.append("✓ 역주입 없음")
    L.append("")
    L.append(f"줄어든 항목 {len(improved)}개:")
    for k, bv, av, d in sorted(improved, key=lambda x: x[3])[:20]:
        L.append(f"    {k}: {bv} → {av}  ({d})")

    # 과윤문 가드. 원문 대비 길이가 크게 흔들리면 내용이 드리프트했을 수 있다.
    bl, al = b.get("chars", 0), a.get("chars", 0)
    if bl:
        L.append("")
        L.append(f"길이: {bl} → {al}자 ({(al - bl) / bl * 100:+.1f}%)")
    return "\n".join(L)


def main() -> int:
    ap = argparse.ArgumentParser(description="표면 AI 티 카운터")
    ap.add_argument("file")
    ap.add_argument("--diff", metavar="AFTER", help="윤문본과 비교")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    before = scan(read(args.file))

    if args.diff:
        after = scan(read(args.diff))
        if args.json:
            print(json.dumps({"before": before, "after": after}, ensure_ascii=False, indent=2))
        else:
            print(diff_report(before, after))
        return 0

    if args.json:
        print(json.dumps(before, ensure_ascii=False, indent=2))
    else:
        print(report(before))
    return 0


if __name__ == "__main__":
    sys.exit(main())
