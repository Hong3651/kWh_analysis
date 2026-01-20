# kWh_analysis

# 🏭 Steel Industry Energy Consumption Prediction & Optimization

머신러닝 기반 철강 공장 전력 사용량 패턴 분석 및 에너지 절감 솔루션 제안

---

## 1. 프로젝트 개요

### 📌 프로젝트 목적

철강 공장의 운영 데이터를 기반으로 **전력 소비 패턴을 예측**하고,
물리적 설비 제어 없이 **운영 스케줄 최적화만으로 에너지 낭비를 얼마나 줄일 수 있는지**를 분석합니다.

> **Key Question**
> *"물리적 제어 없이 운영 스케줄 조정만으로 전력량을 얼마나 줄일 수 있는가?"*

### 📊 데이터셋

* 철강 산업 단지 전력 소비 데이터
* 15분 단위 측정
* 약 **35,000 rows**

---

## 2. 분석 프로세스

### 🛠 데이터 전처리 & Feature Engineering

* **데이터 누수(Data Leakage) 방지**

  * 전력 사용량의 파생/상관 변수인 `CO2`, `Reactive Power (rp)`, `Power Factor (pf)` 제거
  * 모델이 *실제 운영 변수만*으로 예측하도록 설계

* **범주형 변수 처리**

  * `WeekStatus`, `Day_of_week`, `Load_Type` → Label Encoding

* **시간 파생 변수 생성**

  * `NSM (Number of Seconds from Midnight)`
  * `Hour`, `Month`
  * 조업 패턴의 **일/월 주기성** 반영

---

### 🤖 머신러닝 모델링

#### 📐 비교 모델

* Linear Regression
* Random Forest
* XGBoost
* LightGBM
* Support Vector Regression (SVR)

#### 🏆 최종 선택 모델

* **LightGBM**
* **R² Score: 0.779**

> 운영 변수만으로 전력 사용량의 **약 78% 설명 가능**함을 입증
### --- 🏭 최종 분석 리포트 ---
* ✅ 분석 모델: LightGBM (정확도: 77.9%)
* ✅ 현재 총 사용량: 193950.68 kWh
* ✅ AI 운영 최적화 시 절감 가능량: 31046.46 kWh
###  ❗❗예상 에너지 절감률❗❗: ***16.01%***

---

## 3. 핵심 분석 결과 (Insights)

### 🔑 주요 전력 소비 영향 요인 (Feature Importance)

1. **NSM (자정 이후 경과 시간)**

   * 조업 시간대에 따른 전력 소모 변동이 가장 큼

2. **Month (월)**

   * 계절성 및 월별 생산 계획 차이 반영

3. **Load_Type (부하 종류)**

   * 가동 설비 상태에 따른 전력 소비 변화

---

### 📉 에너지 절감 잠재력 시뮬레이션


  * **운영 최적화만으로 약 10~15% 전력 절감 가능성 확인**

---

## 4. 최종 전략 제안 (Action Plan)

### ⚡ 피크 시프트 (Peak Shift)

* NSM 기반 피크 시간대 식별
* 주요 공정 가동 시간을 분산 배치하여 부하 완화

### 📅 월별 목표 관리

* Month 중요도를 반영
* 여름/겨울 등 고부하 시즌 집중 모니터링

### ⏱ 대기 전력 관리

* 주말(`WeekStatus`) 및 비가동 시간대
* 표준 사용량 초과 시 **자동 알림 시스템** 도입 제안

---

## 5. 향후 과제 (Next Steps)

* **모델 성능 고도화**

  * GridSearchCV / Optuna 기반 하이퍼파라미터 튜닝
  * 목표: **R² ≥ 0.80**

* **데이터 확장을 통한 점진적 최적화**
  * 데이터 규모 확대: 현재의 데이터셋을 넘어 1년치 이상의 장기 데이터를 확보하여, 요일별/월별을 넘어선 연간 조업 사이클을 반영한 모델로 고도화.
  * 점진적 성능 개선: 새로운 데이터가 유입될 때마다 모델이 자동으로 학습하고 예측 오차를 수정하는 재학습(Retraining) 시스템을 설계하여, 시간이 지날수록 예측 정확도를 높이는 점진적 최적화를 달성.
  * 추가 변수(Feature) 도입: 기온, 습도와 같은 기상 데이터나 생산 라인별 가동 상태 데이터를 결합하여, 외부 환경 변화에도 흔들리지 않는 견고한 예측 시스템을 구축

---

## 🛠 기술 스택

* **Language**: Python 3.x
* **Libraries**: 

  * Pandas, Scikit-learn
  * XGBoost, LightGBM
  * Matplotlib, Seaborn
* **Environment**:

  * Jupyter Notebook / Google Colab

---

## 📌 기대 효과

* 설비 변경 없이 **운영 전략만으로 에너지 절감 가능성 입증**
* 제조·스마트팩토리 환경에서 **AI 기반 에너지 관리 모델의 실질적 활용 사례** 제시

