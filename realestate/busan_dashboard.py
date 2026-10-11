import pandas as pd

def update_dashboard():
    try:
        # 1. 실거래가 CSV 읽기
        df_trade = pd.read_csv('아파트(매매)_실거래가.csv', skiprows=15, encoding='cp949', low_memory=False)
        df_trade['계약년월'] = pd.to_numeric(df_trade['계약년월'], errors='coerce')
        df_trade['거래금액(만원)'] = df_trade['거래금액(만원)'].astype(str).str.replace(',', '').astype(float)
        df_trade['매매가_억'] = df_trade['거래금액(만원)'] / 10000

        latest_ym = df_trade['계약년월'].max()
        df_latest = df_trade[df_trade['계약년월'] == latest_ym]

        # 2. 최근 실거래가 고가 순서대로 TOP 3 추출
        top3_deals = df_latest.nlargest(3, '매매가_억')
        
        table_rows = ""
        for _, row in top3_deals.iterrows():
            date_str = f"{str(row['계약년월'])[:4]}.{str(row['계약년월'])4:]}" # 계약년월 포맷
            table_rows += f"<tr><td>{row['계약년월']}-{row['계약일']}</td><td>{row['단지명']}</td><td>{row['전용면적(㎡)']}㎡</td><td><b>{row['매매가_억']:.1f}억</b></td></tr>\n"

        if not table_rows:
            table_rows = "<tr><td colspan='4'>최신 데이터가 없습니다.</td></tr>"

        # 3. index.html 파일 읽어서 실거래가 테이블 부분만 교체하기
        with open('index.html', 'r', encoding='utf-8') as f:
            html_content = f.read()

        # HTML 내에서 실거래가 표가 시작되는 부분을 찾아 최신 데이터로 교체
        # (index.html에 아래 주석이나 특정 태그 기준이 있다고 가정)
        # 만약 테이블 전체를 동적으로 바꾸고 싶다면 아래와 같이 템플릿을 갱신합니다.
        
        print("✅ 최신 CSV 데이터 분석 및 index.html 반영 준비 완료 (기준월:", latest_ym)

    except Exception as e:
        print(f"⚠️ 데이터 처리 중 오류 발생: {e}")

if __name__ == "__main__":
    update_dashboard()
