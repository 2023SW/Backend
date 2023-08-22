import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# 원본 파일 읽기 (인코딩을 명시적으로 지정)
original_df = pd.read_csv('info.csv', encoding='cp949')

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

# 나이와 성별 차이에 대한 가중치 정의
age_weight = 0.8
gender_weight = 0.8

# 나이와 성별 차이를 고려한 가중 유사도 계산
weighted_similarity_matrix = np.zeros((len(user_data), len(user_data)))

for i in range(len(user_data)):
    for j in range(len(user_data)):
        user1 = user_data.iloc[i]
        user2 = user_data.iloc[j]

        age_similarity = 1 - abs(user1['나이'] - user2['나이']) * age_weight
        gender_similarity = 1 if user1['성별'] == user2['성별'] else gender_weight
        region_similarity = similarity_matrix[i][j]

        weighted_similarity = age_similarity * gender_similarity * region_similarity
        weighted_similarity_matrix[i][j] = weighted_similarity

# 가중치를 적용한 유사도 행렬을 DataFrame으로 변환
weighted_similarity_df = pd.DataFrame(weighted_similarity_matrix, columns=original_df['유저번호'],
                                      index=original_df['유저번호'])

# 가중치를 적용한 유사도 DataFrame을 CSV 파일로 저장
weighted_similarity_df.to_csv('user_user_similarity_weighted.csv')

print("가중치 적용된 유저-유저 유사도 계산 및 파일 생성이 완료되었습니다.")