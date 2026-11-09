# 업데이트 내역

## 2026-11-09
- Blender 씬 세밀화(장난감 스타일 유지): PolyHaven HDRI(small_rural_road) 적용, 선형 보정으로 선명한 차량 색상, 베벨 모디파이어·둥근 본체·유리 캐빈·헤드/테일 라이트·트럭 화물 리브·경찰 경광등 추가, 타이어+허브캡·미러·범퍼·출구 셰브론·교통콘 소품, Sun+Fill 3점조명, AgX High Contrast + 노출 -0.4
- 해법 재생 애니메이션 유지(최소 이동 6회, 1~73프레임). rush-hour-3d.blend 저장 완료. 웹(Three.js)은 그대로

## 2026-11-08
- Blender MCP로 3D 구현을 시작했으나, 초기화 함수(factory reset)가 MCP 연결을 끊음
- Blender에서는 factory reset을 쓰지 않고 수동으로 지우는 `build_rush_hour.py` 스크립트 저장 — Blender Scripting에서 Run Script 하면 보드·차량·해법 재생 애니메이션 생성됨
- 다음 단계: Blender 재시작 후 MCP 재연결 → build_rush_hour.py 실행 → rush-hour-3d.blend 저장
- (재연결 후 완료) 6×6 보드·벽·출구·차량 10대(노란 경찰차 포함)를 Blender MCP로 생성하고 해법 재생 애니메이션(최소 이동 6회) 적용 — `rush-hour-3d.blend` 저장 완료
- 웹앱(Three.js) 출시: 12개 퍼즐, 드래그·방향키 이동, BFS 최소 이동/힌트, 해법 재생, 되돌리기·다시 시작, 기록 저장, 입체/위에서 보기, 다크 모드, 업데이트 내역 모달 — GitHub Pages 배포 완료: https://wbmaker2.github.io/rush-hour-3d/
- 개선: 차량을 잡고 드래그하면 화면이 회전하지 않고 자동차만 움직임(빈 공간 드래그만 회전). 차량을 귀여운 장난감 스타일로 재디자인 — 둥근 본체·유리 캐빈·헤드라이트/테일라이트·범퍼·사이드미러·허브캡, 길이 3 트럭은 화물 상자, 경찰차는 경광등· 흰 줄무늬(https://wbmaker2.github.io/rush-hour-3d/)
- 개선: 화면 회전 토글 버튼 추가(“화면 회전: 켜기/꺼기”) — 꺼기면 회전 없이 차량 이동만 가능. 목표 경찰차는 ★ 목표 차량 ★ 라벨·금빛 화살표·금빛 링·점멸 경광등으로 한눈에 구분되도록 재디자인(https://wbmaker2.github.io/rush-hour-3d/)
- 수정: '이동' 카운터는 실제로 자동차가 한 칸 움직인 경우에만 셉니다(마우스 미세 움직임·해법 재생 제외). 목표차가 보드 밖(출구 밖)으로 완전히 나간 뒤에야 미션 해결 판정. 미션 해결 시 팝업 모달에 금빛 펄스 '다음 단계 도전' 버튼 표시(https://wbmaker2.github.io/rush-hour-3d/)
- 수정: 전체 12개 레벨의 차량 겹침 제거(L1/L5/L7/L8/L10/L12) — 흰색 트럭 E와 보라색 차가 겹치지 않음. 바닥을 회색 파랑으로 어둡게, 타일을 흰/파랑 체크, 트럭 화물상을 주황색+검정 줄무늬로 바꿔 바닥과 확실히 구분(https://wbmaker2.github.io/rush-hour-3d/)
- 기본값 변경: 화면 회전 ‘꺼기’ + ‘위에서’ 시점으로 시작(https://wbmaker2.github.io/rush-hour-3d/)
- 단계 확장: 12 → 26개 퍼즐(최소 이동 5회→21회 오름차순, 초급/중급/고급). 마지막 단계에서는 ‘모든 퍼즐 완료!’ 모달로 끝나며 처음 단계로 돌아감(무한 반복 제거)(https://wbmaker2.github.io/rush-hour-3d/)
