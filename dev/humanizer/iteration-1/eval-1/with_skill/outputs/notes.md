# 고친 내용

## 1. 무엇이 바뀌었나

**구조**: 결론을 맨 앞으로 올렸다. 원문은 "현황 → 요인 5개 → 접근법 → 결론" 순서로 쌓아 올라가서 마지막 문단까지 읽어도 무엇을 결정해야 하는지 나오지 않았다. 제목을 주장으로 바꾸고(`Navigating the Evolving Landscape of Customer Retention` → `Retention turns on the first 30 days`), 도입을 SCQA 한 문단으로 줄이고, 헤딩 3개를 전부 주장 문장으로 다시 썼다. 마지막 자리는 앞 내용 재진술(`In Conclusion`) 대신 요청 사항으로 채웠다.

**표면 정리**: em dash 10개 → 0, 볼드 8회 → 0, 문장 끝 콜론 2개 → 0, 수동태 2건 → 0, AI 어휘 23건 → 0 (`delve` `holistic` `multifaceted` `robust` `showcase` `leveraging` `foster` `underscore` `ever-evolving` `landscape` 등), 헤지 8건 → 2, 수치 없는 강조 2건 → 0 (`significantly` `considerably`), 빈 수사 삭제 (`In today's fast-paced business environment`, `a testament to the multifaceted nature of the challenge`, `While there are no silver bullets`, `The journey will not be without obstacles, but the destination is worth the effort`).

## 2. 스캔 전후

| 항목 | 원문 | 결과 |
|---|---|---|
| em dash | 10 | 0 |
| AI 어휘 | 23 | 0 |
| 볼드 | 8회 (21.1/1000어) | 0 |
| 불릿 | 5행 | 3행 |
| 문장 끝 콜론 | 2 | 0 |
| 헤지 | 8 | 2 |
| 수치 없는 강조 | 2 | 0 |
| 수동태 | 2 | 0 |
| 문장 길이 변동계수 | 0.51 | 0.64 |
| 분량 | 2,636자 / 380어 | 2,433자 / 405어 |

역주입 검증: **`✓ 역주입 없음`** — 새로 심은 AI 티 0건. 분량 변화 -7.7% (드리프트 경계 30% 이내).

## 3. 판단이 필요한 지점

- **원문에 반박 가능한 주장이 없었다.** 결론부에 올린 "첫 30일에 집중하고, 5개 개별 수정이 아니라 하나의 프로그램으로 편성한다"는 원문이 가장 가깝게 암시한 주장을 제가 정점으로 끌어올린 것이다. 원문의 권고(통합 접근 + 30일 활성화 지표)를 뒤집지는 않았지만, 이 문장이 원문에 그대로 있던 것은 아니다.

- **원문 내부에 모순이 있다.** "온보딩은 robust 하다"와 "온보딩 friction 이 이탈 요인이다"가 같은 문서에 함께 있다. 어느 쪽도 지우지 않고 "온보딩 개선이 중기 이탈까지 닿지 않았다"로 배치했지만, 실제로 온보딩이 잘 돌아가는지는 임원 보고 전에 결정해야 한다.

- **숫자를 만들지 않았다.** 원문의 유일한 수치는 "30일"이다. 그래서 강조어(`significantly improved`, `considerably more likely`)는 숫자로 바꾸지 않고 그냥 걷어냈다. 대신 `activation threshold`가 아무 곳에도 정의돼 있지 않다는 사실을 본문 앞으로 올렸다 — 이게 이 메모의 가장 큰 공백이고, 임원이 먼저 물어볼 지점이다.

- **출처 없는 귀속을 삭제하지 않고 공백으로 명시했다.** 원문 `The data suggests`는 어떤 데이터인지 밝히지 않는다. 지어내지 않고 "우리 데이터가 한 방향을 가리킨다"로 두되, 뒤에 "여기서 우리가 아는 것이 끝난다"를 붙여 근거의 한계를 드러냈다.

- **닫는 문장에 담당자와 기한이 없다.** 원문이 `Next steps and detailed timelines will be circulated separately`로 끝나서 능동태로만 바꿨다(`I will circulate...`). 날짜를 지어내지 않았다. 임원 보고라면 여기에 담당자·기한·예산을 넣어야 권고가 된다 — 그 값은 제가 알 수 없다.

- **부정 병렬은 1개 남겼다.** `Retention is everyone's responsibility, not only the customer success team's remit` — 이 문장은 실제로 책임 배분을 주장하므로 장식이 아니다. (스캐너는 `not only ... but` 형태만 매칭해서 0으로 읽히지만, 실제로는 1개 살아 있다. 전량 제거는 그 자체로 실패라서 의도적으로 남겼다.)

- **손대지 않은 것**: `activation threshold`, `time-to-first-value`, `mid-tier`, `product-market fit`, `behavioral analytics`, `machine learning`, `churn`, `customer success`, `30 days`. 원문 요인 5개는 전부 보존하고 3개 그룹(time to value / support load / pricing perception)으로 묶기만 했다.
