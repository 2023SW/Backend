input_data = """
홍대
합정
상수
연남
강남
역삼
삼성
신촌
연희
이대
신사
논현
청담
압구정
망원
상암
서초
교대
방배
명동
을지로
동대문
성수
왕십리
서울숲
영등포
여의도
문래
종로
광화문
대학로
송파
잠실
방이
용산
이태원
한남
관악
신림
서울대입구
건대
성신여대
안암
마포
고척
불광
연신내
은평
강북
쌍문
목동
"""

lines = input_data.strip().split('\n')
result = ','.join(lines)

with open('place_name.csv', 'w') as f:
    f.write(result)
