# 영어 AI 티와 처방

`scan.py` 의 `[영어 AI 티]` 항목이 여기 대응한다.

**먼저 읽을 것**: 어떤 단어도 그 자체로 죄는 아니다. 사람은 ChatGPT 이전에도 "delve"를
썼다. PubMed 2,750만 건 분석에서 이른바 "AI 어휘"의 증가는 2020년에 시작했고, 이는
ChatGPT 출현보다 이르다. 신호는 **밀도와 동시 출현**이다. 한 페이지에 하나는 소음,
한 문단에 넷은 판정이다.

가장 신뢰할 만한 신호는 어휘가 아니라 구조다 — 출처 없는 주장, 일반적이기만 한 사례,
주제를 설명하지만 기여하지 않는 산문.

## 어휘 — 대체어 표

모델이 "사려 깊게 들리고 싶을 때" 꺼내는 단어들이다.

| 걷어낼 것 | 쓸 것 |
|---|---|
| delve into, dive into | examine, look at, 또는 그냥 본론으로 |
| utilize | use |
| leverage (동사) | use, draw on |
| robust | 구체적으로: reliable, well-tested, handles X |
| seamless, seamlessly | 삭제하거나 무엇이 매끄러운지 명시 |
| multifaceted, nuanced | 삭제. 몇 개의 면인지 말한다 |
| holistic, comprehensive | 삭제하거나 범위를 명시 |
| showcase (동사) | show, demonstrate |
| foster, fostering | build, encourage, 또는 구체 행위 |
| underscore, highlight (비유) | 삭제. 왜 중요한지 직접 쓴다 |
| harness, unlock | use, enable |
| streamline | 무엇을 몇 단계로 줄이는지 |
| embark on a journey | start |
| navigating (비유) | 삭제 |
| landscape, realm, space, ecosystem | market, industry, 또는 구체 명사 |
| tapestry | 거의 항상 삭제 |
| paradigm, synergy | 삭제 |
| cutting-edge, game-changer | 무엇이 어떻게 다른지 |
| ever-evolving, ever-changing | 삭제. 무엇이 변했는지 |
| pivotal, crucial, vital | 삭제. 중요도는 배치로 표현 |
| testament to | evidence of, 또는 삭제 |
| meticulous, intricate | 삭제 |
| transformative, groundbreaking, innovative | 결과를 수치로 |
| furthermore, moreover | and, also, 또는 삭제 |
| In conclusion | 삭제. 결론은 맨 앞에 있어야 한다 |
| It is important to note that | 삭제. 중요하면 그냥 쓴다 |
| It is worth mentioning | 삭제 |
| In today's fast-paced world | 삭제. 아무 문서에나 붙는 문장이다 |
| At the end of the day | 삭제 |

## 부정 병렬 — 가장 강한 구조 신호

`It's not just X, it's Y` 계열. 아무도 갖지 않았던 오해를 정정하는 척하면서 수사적
무게만 얻는다. 한국어의 `A가 아니라 B` 와 정확히 같은 수사이고, 두 언어에서 독립적으로
실측 확인됐다.

변종: `not merely` · `not simply` · `not only X but Y` · `more than just` ·
`isn't just` · `No A, no B, just C` · `While X may seem Y, in reality it's Z`

- `Retention is not just a metric, it's a reflection of product-market fit`
  → `Retention measures product-market fit`
- `This isn't merely a meeting, it's a turning point` → 대개 삭제

**전멸시키지 않는다.** 대비가 실제로 논지인 글에서는 이 구조가 일한다. 장식인 것만
걷어낸다. 판별: 그 문장을 지웠을 때 논지가 손실되는가.

## 균형 사칭 구문

양쪽을 저울질하는 척하지만 실제로는 채움재인 것들.

- `On the one hand... on the other hand...` — 짧은 글에서 두 번째가 착지하지 못할 때
- `While there are no silver bullets` — 삭제
- `It could be argued that` — 누가 주장하는가. 저자면 그냥 주장한다
- `Rather than X, we should consider Y` — Y를 하자고 쓴다

## 출처 없는 귀속

`studies show` · `research suggests` · `experts say` · `it is widely believed` ·
`the data suggests`

이름과 날짜를 붙이거나 삭제한다. 원문에 출처가 없으면 **만들지 않는다**.
`The data suggests that...` 는 어떤 데이터인지 쓸 수 없으면 주장 자체를 낮춘다.

## False range

`ranging from X to Y` — 구체적으로 들리지만 아무것도 전달하지 않는다.

- `benefits ranging from cost savings to improved morale` → 실제 항목 둘을 쓰거나 삭제

## Rule of three 형용사 삼중

`innovative, transformative, and groundbreaking` · `complex, multifaceted, and
ever-evolving`

세 개 다 같은 말이거나 세 개 다 내용이 없다. 하나만 남기거나 넷으로 늘려 비대칭을
만든다. 삼중 대칭 자체가 리듬 신호다.

## 표면 분석

사실 뒤에 붙는 알맹이 없는 논평.

`highlighting the importance of` · `illustrating the need for` ·
`demonstrating the value of` · `reflecting the growing trend toward`

- `Churn rose 12%, highlighting the importance of retention` →
  `Churn rose 12%. At that rate we lose a full cohort every eight months.`

무엇이 왜 중요한지 쓸 수 없으면 사실만 남기고 논평을 지운다.

## 섹션 요약

앞 내용을 다시 말하는 마지막 문단. `In summary` `To summarize` `As we have seen`

삭제한다. 마지막 자리는 가장 값비싼 자리이므로 결정 사항이나 요구를 놓는다.

## 헤지

`may` · `might` · `could potentially` · `perhaps` · `somewhat` · `relatively` ·
`tend to` · `generally speaking` · `it seems` · `arguably`

중첩이 진짜 문제다. `may be somewhat relatively effective` 는 판단이 아니라 습관이다.

판별식은 SKILL.md 「헤지를 걷는 판별식」을 따른다. **저자의 추정을 단정으로 바꾸지
않는다.** `revenue may have grown 12%` 를 `revenue grew 12%` 로 바꾸는 건 위조다.
중첩만 걷는다.

## 수치 없는 강조

`significantly` · `substantially` · `dramatically` · `considerably` · `vastly` ·
`markedly` · `greatly`

- `significantly improved early-stage engagement` → `raised 7-day activation from 34% to 51%`

원문에 숫자가 없으면 강조어만 지운다.

## 수동태

행위자를 숨기는 문장은 책임을 숨긴다.

- `Next steps will be circulated separately` → `I'll send next steps by Friday`
- `The decision was made to proceed` → `The steering committee approved it on 3 March`
- `Mistakes were made` → 누가 무엇을 했는지

스캔의 `수동태` 항목이 셈한다. 행위자가 정말 불명이거나 무관할 때만 남긴다.

## 편지투 잔재

`I hope this helps!` · `Let me know if you have any questions!` · `Great question!` ·
`Certainly!` · `Here's a breakdown of...`

프롬프트 응답의 껍데기가 문서에 남은 것이다. 전부 삭제한다.

## 리듬

- **문장 길이 변동계수 0.4 미만** — 다 같은 길이다. 짧은 문장을 섞는다.
- **문단 길이 균일** — 3문장 문단이 연속 여섯 개면 기계적이다.
- **모든 문단이 topic sentence 로 시작** — 영어 작문 교본 공식이다. 일부 문단은
  사례나 숫자로 시작한다.
- **em dash 밀도** — 문단당 1개 이하. 근거는 AI 판별이 아니라 맥킨지 문체다
  (SKILL.md 「특수문자 규칙」의 단서 참조).

## 빠진 것을 더한다

패턴 제거만으로는 사람 글이 되지 않는다. 표면을 다 고쳐도 알맹이가 없으면 여전히
AI처럼 읽힌다. 다음이 하나라도 있어야 한다 — 단, **원문이나 주어진 자료 안에서만**
조달한다.

1. **저자가 싸워서 지킬 문장 하나.** 누군가 반대할 수 있는 주장. 없으면 글에 저자가
   없는 것이다.
2. **이름과 날짜가 붙은 수치.** `44% as of August 2026` 는 검증 가능하고 `low` 는 아니다.
3. **구체적인 1차 사례.** 검색으로 나오지 않는 세부. 자료에 있으면 끌어올린다.
4. **첫 200단어 안의 직답.** 독자의 질문에 바로 답한다.

없는 것을 만들어 채우지 않는다. 자료에 없으면 무엇을 확인해야 하는지를 쓴다.

## 손대지 않는 것

- 발화 표지가 붙은 직접 인용 (`according to`, `said`, `wrote`)
- 고유명사·제품명·기관명
- 수치·날짜·통화 — 반올림도 금지
- 업계 표준 용어 — API, prompt, token, EBITDA, CAGR, churn
- 법률 조문·계약 문구
- 코드 블록 안 전체
