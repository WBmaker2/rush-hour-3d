# 업데이트 내역

## 2026-11-08
- 참고 사이트(jvibeschool.org/3D/RushHour) 확인: 6×6 보드, 노란 경찰차를 오른쪽 출구로 이동, LEVEL 01 최소 이동 12회
- Blender MCP로 3D 구현을 시작했으나, 초기화 함수(factory reset)가 MCP 연결을 끊음
- Blender에서는 factory reset을 쓰지 않고 수동으로 지우는 `build_rush_hour.py` 스크립트 저장 — Blender Scripting에서 Run Script 하면 보드·차량·해법 재생 애니메이션 생성됨
- 다음 단계: Blender 재시작 후 MCP 재연결 → build_rush_hour.py 실행 → rush-hour-3d.blend 저장
- (재연결 후 완료) 6×6 보드·벽·출구·차량 10대(노란 경찰차 포함)를 Blender MCP로 생성하고 해법 재생 애니메이션(최소 이동 6회) 적용 — `rush-hour-3d.blend` 저장 완료
- 웹앱(Three.js) 출시: 12개 퍼즐, 드래그·방향키 이동, BFS 최소 이동/힌트, 해법 재생, 되돌리기·다시 시작, 기록 저장, 입체/위에서 보기, 다크 모드, 업데이트 내역 모달 — GitHub Pages 배포 완료: https://wbmaker2.github.io/rush-hour-3d/
- 개선: 차량을 잡고 드래그하면 화면이 회전하지 않고 자동차만 움직임(빈 공간 드래그만 회전). 차량을 귀여운 장난감 스타일로 재디자인 — 둥근 본체·유리 캐빈·헤드라이트/테일라이트·범퍼·사이드미러·허브캡, 길이 3 트럭은 화물 상자, 경찰차는 경광등· 흰 줄무늬(https://wbmaker2.github.io/rush-hour-3d/)
