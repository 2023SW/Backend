import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity
from mlxtend.frequent_patterns import fpgrowth
from mlxtend.frequent_patterns import association_rules
from matplotlib import font_manager, rc

# 한글 폰트 경로 설정 (시스템에 설치된 한글 폰트 경로로 수정해주세요)
font_path = "C:\Windows\Fonts\gulim.ttc"

# 폰트 설정
font_name = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font_name)


# 원본 파일 읽기 (인코딩을 명시적으로 지정)
original_df = pd.read_csv('info.csv', encoding="cp949")

# 지역 목록 및 NaN 값 처리
regions = [
    '홍대', '합정', '상수', '연남', '강남', '역삼', '삼성', '신촌', '연희', '이대',
    '신사', '논현', '청담', '압구정', '망원', '상암', '서초', '교대', '방배', '명동',
    '을지로', '동대문', '성수', '왕십리', '서울숲', '영등포', '여의도', '문래', '종로',
    '광화문', '대학로', '송파', '잠실', '방이', '용산', '이태원', '한남', '관악',
    '신림', '서울대입구', '건대', '성신여대', '안암', '마포', '고척', '불광', '연신내',
    '은평', '강북', '쌍문', '목동'
]

original_df['지역'] = original_df['지역'].fillna('')

# 지역 열의 각 행에 대해 지역 목록에 해당하는 열에 1을 표시하고, 나머지는 0으로 처리
for region in regions:
    original_df[region] = original_df['지역'].apply(lambda x: 1 if region in x else 0)

# '지역' 열 제거
original_df.drop(columns=['지역'], inplace=True)

# 나이 데이터를 숫자로 변환하는 함수
def convert_age(age_str):
    if age_str == '10대':
        return 1
    elif age_str == '20대':
        return 2
    elif age_str == '30대':
        return 3
    elif age_str == '40대':
        return 4
    elif age_str == '50대':
        return 5

# 성별 데이터를 숫자로 변환하는 함수
def convert_gender(gender_str):
    if gender_str == '남성':
        return 0
    elif gender_str == '여성':
        return 1

# '나이' 열 데이터 변환
original_df['나이'] = original_df['나이'].apply(convert_age)

# '성별' 열 데이터 변환
original_df['성별'] = original_df['성별'].apply(convert_gender)

# 유저 번호 열 추가
original_df.insert(0, '유저번호', ['user' + str(i) for i in range(1, len(original_df) + 1)])

# NaN 값을 0으로 대체
original_df.fillna(0, inplace=True)

# '나이'와 '성별'이 같은 사용자들 간에 유사도 계산
user_data = original_df[['유저번호', '나이', '성별'] + regions].copy()

# 유사도 계산을 위해 '유저번호' 열 제거
user_data.drop(columns=['유저번호'], inplace=True)

original_df.to_csv('original.csv')

# 유사도 계산
similarity_matrix = cosine_similarity(user_data)

# 유사도 행렬을 DataFrame으로 변환
similarity_df = pd.DataFrame(similarity_matrix, columns=original_df['유저번호'], index=original_df['유저번호'])

# 결과 파일로 저장
similarity_df.to_csv('user_user_similarity.csv')

## 'original.csv' 파일을 읽어옵니다.
original_df = pd.read_csv('original.csv')

# 지역별 선택 카운트를 계산합니다.
region_counts = original_df[regions].sum()

# 혼잡도를 계산하여 'congestion' 열을 추가합니다.
congestion_thresholds = [1, 4, 7, 10]  # 혼잡도 기준
congestion_labels = ['매우 한산', '한산', '혼잡', '매우 혼잡']

def calculate_congestion(count):
    for i, threshold in enumerate(congestion_thresholds):
        if count >= threshold:
            return congestion_labels[i]
    return '매우 한산'

region_counts['혼잡도'] = region_counts.apply(calculate_congestion)

# 결과를 CSV 파일로 저장합니다.
region_counts.to_csv('congestion.csv', index=True)

print("지역별 혼잡도 계산 및 파일 생성이 완료되었습니다.")

# 지역 간의 연관성을 분석하기 위한 데이터 준비
association_data = original_df[regions].copy()

# association_data 데이터프레임 내의 데이터를 불리언 형태로 변환
association_data = association_data.astype(bool)

# FP-Growth 알고리즘을 사용하여 빈발 지역 간의 연관 규칙을 찾음
frequent_itemsets = fpgrowth(association_data, min_support=0.1, use_colnames=True)

# 연관 규칙을 생성하고 지역 간의 연관성을 나타내는 지표인 'lift' 값을 추가
association_rules_df = association_rules(frequent_itemsets, metric="lift", min_threshold=1)

# 연관성이 높은 지역 간의 연관 규칙을 CSV 파일로 내보내기
association_rules_df.to_csv('association_rules.csv', index=False)

print("연관 규칙을 찾아내어 CSV 파일로 저장하는 작업이 완료되었습니다.")

# association_rules_df 데이터프레임에서 필요한 열을 가져오기
antecedents_str = association_rules_df['antecedents'].apply(lambda x: ', '.join(list(x)))
confidence = association_rules_df['confidence']

# antecedents를 문자열 형태로 변환하여 새로운 컬럼 생성
association_rules_df['antecedents_str'] = antecedents_str

# antecedents와 consequents를 문자열 형태로 변환하여 새로운 컬럼 생성
association_rules_df['consequents_str'] = association_rules_df['consequents'].apply(lambda x: ', '.join(list(x)))

# 각 antecedents의 frozenset에 대해 consequence 지역 이름과 confidence를 기준으로 내림차순 정렬하여 상위 10개 선택하고 시각화
for frozenset_item in association_rules_df['antecedents_str'].unique():
    filtered_rules = association_rules_df[association_rules_df['antecedents_str'] == frozenset_item]
    sorted_rules = filtered_rules.sort_values(by='confidence', ascending=False).head(10)

    plt.figure(figsize=(8, 6))
    plt.bar(sorted_rules['consequents_str'], sorted_rules['confidence'])
    plt.xlabel('Consequents')
    plt.ylabel('Confidence')
    plt.title(f'Top 10 Association Rules for {frozenset_item}')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()