# 제3자 저작물 고지

이 저장소는 아래 외부 저작물의 내용을 참조·인용한다. 원저작자의 라이선스 조건을
따르며, 재배포하는 쪽도 이 고지를 유지해야 한다.

## Humanize KR (im-not-ai)

- 원본: https://github.com/epoko77-ai/im-not-ai
- 저작권: Copyright (c) 2026 epoko77-ai
- 라이선스: MIT

`skills/humanizer/references/ai-tells-korean.md` 의 한국어 AI 티 **패턴 분류와 실측
수치**는 이 프로젝트의 `ai-tell-taxonomy.md` v2.3 에서 가져왔다. 구체적으로는

- 패턴 분류 체계(번역투 · 구조적 패턴 · 관용구 · 리듬 · 시각 장식 등)와 개별 패턴 정의
- 실측 분리도 — 연결어미 뒤 쉼표 4.84배, 부정 대구 9.2배(사람 글 532편 중 31편 출현) 등
- 과윤문 가드(변경률 30%/50%), 역주입 금지, 전멸 금지 원칙

코드는 가져오지 않았다(`scripts/scan.py` 는 새로 작성). 위 수치들의 **원출처**는 다시
KatFish(Park et al., 인간 470편 대 LLM 1,624편), Toral(2019) post-editese, 한국
번역학계 번역투 연구(이영옥 2001 · 김정우 2007 · 김도훈 2009 · 김혜영 2019 등)다.

원본 라이선스 전문:

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

## 참고 문헌 (직접 인용 아님)

`skills/humanizer/references/mckinsey-voice.md` 의 피라미드 구조·SCQA·MECE 는
Barbara Minto, *The Minto Pyramid Principle* (1987 / 1996 / 2009) 의 공개된 개념을
정리한 것이다. 원문을 인용하지 않았다.

영어 AI 티 어휘 목록은 공개 연구·편집자 합의 목록을 참조했다. em dash 밀도 수치는
E. M. Freeburg (2026) preprint — 12개 instruction-tuned 모델 약 240,000단어 대
인간 기준선 57,232단어 비교 — 에서 인용했다.
