# Vercel 배포 가이드 (수정됨 - NOT_FOUND 오류 해결)

## 📋 준비사항

1. **Vercel 계정** - https://vercel.com 에서 가입
2. **GitHub 계정** - 코드를 GitHub에 업로드할 계정
3. **Gemini API Key** - 이미 있음: `AIzaSyA9_-Nn8LFkh4PJXvwSpy1xrEuVOG8zrUU`

## ⚠️ 중요 변경사항

NOT_FOUND 오류 해결을 위해 다음 파일들이 추가/수정되었습니다:
- ✅ `api/index.py` - Vercel 진입점
- ✅ `public/index.html` - 정적 파일
- ✅ `vercel.json` - 라우팅 설정 업데이트

## 🚀 배포 단계

### 1단계: 코드 업데이트 (중요!)

1. GitHub에 로그인
2. 새 저장소 생성
   - 이름: `b2b-ai-agent` (또는 원하는 이름)
   - 공개/비공개 선택
3. 저장소 URL 복사

### 2단계: 코드를 GitHub에 업데이트

이미 GitHub에 올렸다면, 새로운 파일들을 추가하세요:

```bash
cd "C:\Users\user\B2B_AI AGENT"

# 새 파일 추가
git add api/ public/ vercel.json app.py

# 커밋
git commit -m "Fix: Vercel NOT_FOUND error - Add api/index.py"

# 푸시
git push
```

처음 올리는 경우:

```bash
cd "C:\Users\user\B2B_AI AGENT"

# Git 초기화
git init

# 파일 추가 (.gitignore 자동 적용)
git add .

# 커밋
git commit -m "Initial commit: B2B AI Agent with Vercel support"

# GitHub 저장소 연결 (본인의 저장소 URL로 변경)
git remote add origin https://github.com/본인계정/저장소이름.git

# 푸시
git branch -M main
git push -u origin main
```

### 3단계: Vercel에서 프로젝트 생성

1. **Vercel 로그인**
   - https://vercel.com 접속
   - GitHub 계정으로 로그인

2. **새 프로젝트 생성**
   - "Add New..." → "Project" 클릭
   - GitHub 저장소 연결 허용
   - `b2b-ai-agent` 저장소 선택
   - "Import" 클릭

3. **프로젝트 설정**
   - Framework Preset: `Other` 선택
   - Build Command: 비워두기
   - Output Directory: 비워두기
   - Install Command: `pip install -r requirements.txt`

4. **환경 변수 설정** ⭐ 매우 중요!
   - "Environment Variables" 섹션에서:
   ```
   Name: GEMINI_API_KEY
   Value: AIzaSyA9_-Nn8LFkh4PJXvwSpy1xrEuVOG8zrUU
   ```
   - "Add" 클릭

5. **Deploy 버튼 클릭**

### 4단계: 배포 완료 및 확인

1. 배포가 완료되면 (약 2-3분 소요):
   ```
   ✅ Deployed successfully!
   ```

2. 제공된 URL로 접속:
   ```
   https://your-project-name.vercel.app
   ```

3. 테스트:
   - 웹 인터페이스 접속
   - 채팅 기능 테스트
   - 그래프 생성 확인

## 🔧 배포 후 설정

### 도메인 설정 (선택사항)

1. Vercel Dashboard → Settings → Domains
2. 커스텀 도메인 추가 가능

### 환경 변수 추가/수정

1. Vercel Dashboard → Settings → Environment Variables
2. 변수 추가/수정 후 자동 재배포

## 🔄 업데이트 배포

코드를 수정한 후:

```bash
git add .
git commit -m "업데이트 내용"
git push
```

→ Vercel이 자동으로 재배포합니다!

## ⚠️ 주의사항

### 1. API Key 보안
- ✅ 환경 변수에 저장됨 (안전)
- ❌ 코드에 직접 입력하지 말 것
- GitHub에 API Key가 노출되지 않도록 주의

### 2. 데이터 파일
현재 설정:
- `SALES DATA.csv` - GitHub에 포함
- `Details of the company.xlsx` - GitHub에 포함

⚠️ **대용량 파일인 경우 Git LFS 사용 권장**

### 3. 서버리스 제한사항
- 요청 타임아웃: 10초 (Hobby), 60초 (Pro)
- 메모리: 1GB (Hobby), 3GB (Pro)
- 대용량 데이터 처리 시 최적화 필요

## 📊 모니터링

### Vercel Dashboard에서:
- 배포 로그 확인
- 실시간 트래픽 모니터링
- 오류 로그 확인

### 로그 확인:
```
Dashboard → Deployments → 특정 배포 클릭 → Function Logs
```

## 🛠️ 문제 해결

### 배포 실패 시:
1. Vercel 로그 확인
2. `requirements.txt` 의존성 확인
3. 환경 변수 설정 확인

### API 오류 시:
1. Gemini API Key 확인
2. 환경 변수 이름 확인 (`GEMINI_API_KEY`)
3. Vercel 함수 로그 확인

## 📱 접속 URL

배포 완료 후:
```
https://your-project-name.vercel.app
```

이 URL을 팀원들과 공유하여 어디서든 사용 가능!

## 💡 팁

1. **무료 플랜**: 월 100GB 대역폭, 무제한 배포
2. **자동 HTTPS**: Vercel이 자동으로 SSL 인증서 제공
3. **글로벌 CDN**: 전 세계 어디서나 빠른 접속
4. **Git 기반**: 코드 푸시하면 자동 배포

## 🎉 완료!

이제 전 세계 어디서든 B2B AI Agent를 사용할 수 있습니다!
