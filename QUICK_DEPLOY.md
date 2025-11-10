# 🚀 간단 배포 가이드

## 방법 1: GitHub Desktop 사용 (가장 쉬움)

### 1단계: GitHub Desktop 설치
- https://desktop.github.com/ 에서 다운로드

### 2단계: 저장소 만들기
1. GitHub Desktop 열기
2. "File" → "New repository"
3. 이름: `b2b-ai-agent`
4. Local path: `C:\Users\user\B2B_AI AGENT` 선택
5. "Create repository" 클릭

### 3단계: GitHub에 업로드
1. "Publish repository" 클릭
2. Private/Public 선택
3. "Publish repository" 클릭
4. ✅ 완료!

---

## 방법 2: 명령어 사용

```bash
# 폴더로 이동
cd "C:\Users\user\B2B_AI AGENT"

# Git 초기화 (처음만)
git init

# 모든 파일 추가
git add .

# 커밋
git commit -m "B2B AI Agent"

# GitHub에 연결 (본인 저장소 URL)
git remote add origin https://github.com/본인계정/저장소이름.git

# 업로드
git branch -M main
git push -u origin main
```

---

## Vercel 배포

### 1단계: Vercel 접속
- https://vercel.com
- GitHub 계정으로 로그인

### 2단계: 프로젝트 추가
1. "Add New..." → "Project"
2. GitHub 저장소 선택 (`b2b-ai-agent`)
3. "Import" 클릭

### 3단계: 환경 변수 설정 ⭐
```
Name: GEMINI_API_KEY
Value: AIzaSyA9_-Nn8LFkh4PJXvwSpy1xrEuVOG8zrUU
```

### 4단계: Deploy!
- "Deploy" 버튼 클릭
- 2-3분 대기
- ✅ 완료!

---

## ✨ 그게 다예요!

폴더 전체를 그대로 GitHub에 올리면:
- ✅ 모든 Python 파일
- ✅ 데이터 파일 (CSV, Excel)
- ✅ HTML, CSS, JS
- ✅ 설정 파일 (vercel.json, requirements.txt)

모두 자동으로 업로드됩니다!

`.gitignore` 파일이 자동으로 불필요한 파일들(`__pycache__`, `.pyc` 등)은 제외합니다.

---

## 🔄 코드 수정 후 업데이트

GitHub Desktop 사용:
1. 변경사항 확인
2. 커밋 메시지 입력
3. "Commit to main" 클릭
4. "Push origin" 클릭

명령어 사용:
```bash
git add .
git commit -m "수정 내용"
git push
```

→ Vercel이 자동으로 재배포!

---

## ❓ 자주 묻는 질문

**Q: 폴더 이름에 공백이 있어도 되나요?**
A: 네! `B2B_AI AGENT` 그대로 사용 가능합니다.

**Q: 모든 파일을 올려도 되나요?**
A: 네! `.gitignore`가 불필요한 파일은 자동으로 제외합니다.

**Q: 데이터 파일(CSV, Excel)도 올라가나요?**
A: 네! 자동으로 포함됩니다.

**Q: 비밀번호/API 키가 노출되지 않나요?**
A: Vercel에서 환경 변수로 설정하면 안전합니다.

---

## 🎉 완료 후

배포된 URL:
```
https://your-project-name.vercel.app
```

이제 전 세계 어디서든 접속 가능!
