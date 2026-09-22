# skills

Claude Code 개인 스킬 모음. 스킬 하나가 `skills/<이름>/` 폴더 하나다.

## 수록 스킬

| 스킬 | 하는 일 |
|---|---|
| [`humanizer`](skills/humanizer/) | AI가 쓴 글을 20년차 맥킨지 컨설턴트 문체로 고쳐 쓰거나 처음부터 쓴다. 한국어·영어. 결론 먼저(Minto 피라미드), 반박 가능한 단언, 정량 근거로 재구성하고 AI 특유의 특수문자·상투구·헤지 중첩을 걷어낸다. |

## 설치

Claude Code 에서 두 줄이면 된다. **스킬마다 별개 플러그인이라 필요한 것만 골라 받는다** —
안 쓰는 스킬이 딸려 오지 않는다.

```
/plugin marketplace add aron0628/skills
/plugin install humanizer@skills
```

첫 줄은 한 번만 하면 된다. 다른 스킬을 더 쓰고 싶으면 두 번째 줄만 그 이름으로 반복한다.
설치한 스킬은 `/plugin` 메뉴에서 끄거나 지울 수 있다.

업데이트:

```
/plugin marketplace update skills
```

새 세션에서 확인한다. 자연어로 요청하면 발동한다 — 예: "이 보고서 AI 티 좀 없애줘",
"임원 보고용으로 다듬어줘", "이 메모 정리해서 이사회 문서로 만들어줘".

### 직접 설치 (스킬을 고쳐 가며 쓸 때)

심볼릭 링크로 걸면 저장소에서 고친 내용이 바로 반영된다.

```bash
git clone https://github.com/aron0628/skills.git ~/dev/skills
ln -s ~/dev/skills/skills/humanizer ~/.claude/skills/humanizer
```

제거는 링크만 지우면 된다.

```bash
rm ~/.claude/skills/humanizer
```

## 구조

```
.claude-plugin/
└── marketplace.json    ← 어떤 스킬을 어떤 플러그인으로 내놓을지 선언

skills/                 ← Claude Code 가 읽는 스킬 본체. 이 아래만 링크한다
└── humanizer/
    ├── SKILL.md            진입점 (frontmatter 의 description 이 발동 조건)
    ├── references/         필요할 때만 읽는 상세 문서
    └── scripts/            결정적 계산용 스크립트

dev/                    ← 스킬 개발·검증 자료. 설치에는 불필요
└── humanizer/
    ├── fixtures/           테스트 입력 (AI 티가 심한 글 2개 + 거친 메모 1개)
    ├── evals/              평가 케이스 정의
    ├── trigger-eval.json   발동 조건 테스트용 20문항
    ├── grade.py            산출물 기계 채점
    ├── make_benchmark.py   채점 결과 집계
    └── iteration-1/        1차 검증 결과 (스킬 적용 대 대조군)
```

## 새 스킬 추가

1. `skills/<이름>/SKILL.md` 를 만든다
2. `.claude-plugin/marketplace.json` 의 `plugins` 배열에 항목을 추가한다

```json
{
  "name": "<이름>",
  "description": "언제 이 스킬을 쓰는지. 설치 목록에 이 문장이 보인다",
  "source": "./",
  "strict": false,
  "skills": ["./skills/<이름>"]
}
```

**2번을 빼먹으면 폴더가 있어도 `/plugin install` 목록에 뜨지 않는다.** 스킬을 하나씩
골라 받게 하는 대가다. 전부 한 덩어리로 내놓을 거라면 항목 하나에 `skills` 배열을
여러 개 담거나 배열 자체를 빼면 되지만, 그러면 받는 쪽이 고를 수 없다.

추가 후 검증한다.

```bash
claude plugin validate .
```

## 개발

스킬을 고친 뒤 검증하려면 `dev/<스킬명>/` 에서 돌린다.

```bash
cd dev/humanizer
python3 grade.py iteration-1        # 산출물 채점
python3 make_benchmark.py iteration-1   # 집계
```

`humanizer` 의 스캐너는 단독으로도 쓴다. 글 하나의 AI 티를 세거나, 고치기 전후를
비교해 **고치는 과정에서 새 AI 티를 심지 않았는지** 확인한다.

```bash
python3 skills/humanizer/scripts/scan.py 초안.md
python3 skills/humanizer/scripts/scan.py 원본.md --diff 결과물.md
```

### 채점기를 고칠 때

판정 기준을 바꿨으면 **검출력부터 증명한다.** 원문을 그대로 "결과물"로 놓고 채점해
대부분 FAIL 이 나와야 한다. 통과해 버리면 그 채점은 아무것도 재지 못한다.

```bash
mkdir -p /tmp/dt/eval-0/with_skill/outputs
cp fixtures/ko-report.md /tmp/dt/eval-0/with_skill/outputs/result.md
python3 grade.py /tmp/dt     # 6 fail 이 나와야 정상
```

1차 개발에서 이 절차가 채점기 결함 네 건을 잡았다. 자기 참조 개수("위 4개 항목")를
수치 위조로 오판한 것, 결론 위치를 키워드로 근사해 결론이 맨 끝인 원문까지 통과시킨 것
등이다.

## 라이선스

MIT. [`LICENSE`](LICENSE) 참고.

### 제3자 저작물

`skills/humanizer/references/ai-tells-korean.md` 의 한국어 AI 티 자료는 아래 프로젝트에서
가져왔다. 코드는 가져오지 않았다 — `scan.py` 는 새로 작성했다.

> **Humanize KR** · https://github.com/epoko77-ai/im-not-ai
> Copyright (c) 2026 epoko77-ai · MIT License

가져온 범위는 패턴 분류 체계, 실측 분리도(연결어미 뒤 쉼표 4.84배 · 부정 대구 9.2배 ·
사람 글 532편 중 31편 출현 등), 과윤문 가드(변경률 30%/50%)와 역주입 금지·전멸 금지
원칙, 그리고 일부 예문이다. 이 수치들의 원출처는 다시 KatFish(Park et al., 인간 470편
대 LLM 1,624편), Toral(2019) post-editese, 한국 번역학계 번역투 연구(이영옥 2001 ·
김정우 2007 · 김도훈 2009 · 김혜영 2019 등)다.

MIT 조건에 따라 위 저작권 고지를 유지한다. 이 저장소를 재배포하는 쪽도 같다.

<details>
<summary>원본 MIT 라이선스 전문</summary>

```
MIT License

Copyright (c) 2026 epoko77-ai

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

</details>

### 참고 문헌 (직접 인용 아님)

`skills/humanizer/references/mckinsey-voice.md` 의 피라미드 구조·SCQA·MECE 는
Barbara Minto, *The Minto Pyramid Principle* (1987 / 1996 / 2009) 의 공개된 개념을
정리한 것으로 원문을 인용하지 않았다. em dash 밀도 수치는 E. M. Freeburg (2026)
preprint — 12개 instruction-tuned 모델 약 240,000단어 대 인간 기준선 57,232단어 —
에서 인용했다.
