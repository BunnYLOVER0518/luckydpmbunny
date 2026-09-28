# 불멸 영웅 DPM 연구실

`index.html`은 외부 리소스 없이 동작하는 배포 페이지입니다. DPM 기본 행의 유일한 원본은 `data/dpm-raw.json`이며, 페이지의 `RAW` 배열은 생성 결과입니다. 다른 계산 데이터와 화면 코드는 현재 `index.html`에 포함되어 있습니다.

```sh
python3 scripts/build-dpm.py          # 원본을 수정한 뒤 index.html 재생성
python3 scripts/build-dpm.py --check  # 원본/산출물 및 기준 영웅·케이스·DPM 검사
```

영웅이나 케이스를 의도적으로 추가하고 기준 DPM이 바뀐다면 `scripts/build-dpm.py`의 기준 목록과 샘플 값을 검토해 함께 갱신하세요. CI는 원본과 페이지가 어긋나거나 기존 기준이 예기치 않게 바뀌면 실패합니다. 과거의 별도 `dpm-data.js`, `rune-data.js` 등은 현재 페이지에서 참조하지 않아 제거했습니다.
