# skills

Claude Code 개인 스킬 모음. 스킬 하나가 `skills/<이름>/` 폴더 하나다.

## 수록 스킬

| 스킬 | 하는 일 |
|---|---|
| [`humanizer`](skills/humanizer/) | AI가 쓴 글을 20년차 맥킨지 컨설턴트 문체로 고쳐 쓰거나 처음부터 쓴다. 한국어·영어. 결론 먼저(Minto 피라미드), 반박 가능한 단언, 정량 근거로 재구성하고 AI 특유의 특수문자·상투구·헤지 중첩을 걷어낸다. |

## 설치

클론한 뒤 쓰려는 스킬을 `~/.claude/skills/` 에 심볼릭 링크로 건다. 링크로 걸어야
저장소에서 고친 내용이 바로 반영되고 사본이 어긋나지 않는다.

```bash
git clone https://github.com/aron0628/skills.git ~/dev/skills
ln -s ~/dev/skills/skills/humanizer ~/.claude/skills/humanizer
```

새 세션에서 확인한다. 자연어로 요청하면 발동한다 — 예: "이 보고서 AI 티 좀 없애줘",
"임원 보고용으로 다듬어줘", "이 메모 정리해서 이사회 문서로 만들어줘".

제거는 링크만 지우면 된다.

```bash
rm ~/.claude/skills/humanizer
```

## 구조

```
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

`humanizer` 의 한국어 패턴 자료는 MIT 라이선스인 외부 프로젝트
[Humanize KR](https://github.com/epoko77-ai/im-not-ai)의 분류 체계를 참조했다.
출처와 원본 라이선스 고지는 [`NOTICE.md`](NOTICE.md) 에 있다.
