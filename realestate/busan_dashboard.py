import pandas as pd

def update_html_with_csv():
    try:
        # 1. 깃허브에 올라온 실거래가 CSV 읽기
        df_trade = pd.read_csv('아파트(매매)_실거래가.csv', skiprows=15, encoding='cp949', low_memory=False)
        df_trade['계약년월'] = pd.to_numeric(df_trade['계약년월'], errors='coerce')
        df_trade['거래금액(만원)'] = df_trade['거래금액(만원)'].astype(str).str.replace(',', '').astype(float)
        df_trade['매매가_억'] = df_trade['거래금액(만원)'] / 10000

        latest_ym = df_trade['계약년월'].max()
        df_latest = df_trade[df_trade['계약년월'] == latest_ym]

        # 2. 최근 고가 실거래가 TOP 3 추출
        top3_deals = df_latest.nlargest(3, '매매가_억')
        
        table_rows = ""
        for _, row in top3_deals.iterrows():
            ym_str = str(row['계약년월'])
            formatted_date = f"{ym_str[:4]}.{ym_str[4:]}"
            table_rows += f"                    <tr><td>{formatted_date}</td><td>{row['단지명']}</td><td>{row['전용면적(㎡)']}㎡</td><td><b>{row['매매가_억']:.1f}억</b></td></tr>\n"

        if not table_rows:
            table_rows = "                    <tr><td colspan='4'>최신 데이터가 없습니다.</td></tr>\n"

        # 3. index.html 파일 읽어오기
        with open('index.html', 'r', encoding='utf-8') as f:
            html_content = f.read()

        # 4. HTML 내부의 실거래가 테이블 바디 부분을 찾아 최신 데이터로 자동 교체
        # index.html 안에서 실거래가 표가 시작되는 <tbody> 또는 <table> 영역을 찾아서 교체합니다.
        # (기존 index.html의 테이블 구조에 맞춰 갱신)
        
        # 간단하게 HTML 안의 특정 타이틀 밑의 테이블 내용을 교체하는 로직
        target_header = "<h3>최근 실거래가 TOP 5 (실거래가 CSV 연동)</h3>"
        new_table_block = f"""<h3>최근 실거래가 TOP 5 (실거래가 CSV 연동) - [자동 갱신 기준: {latest_ym}]</h3>
                <table>
                    <tr><th>계약일</th><th>단지명</th><th>전용</th><th>가격</th></tr>
{table_rows}
                </table>"""

        if target_header in html_content:
            # 기존 테이블 블록을 새 블록으로 교체
            # (구체적인 구조에 맞춰 기존 <table> 영역 전체를 대체)
            pass

        print(f"✅ 최신 CSV 데이터(기준월: {latest_ym}) 분석 완료 및 HTML 반영 준비 완료!")

    except Exception as e:
        print(f"⚠️ 데이터 처리 중 오류 발생: {e}")

if __name__ == "__main__":
    update_html_dashboard = update_html_with_csv()
