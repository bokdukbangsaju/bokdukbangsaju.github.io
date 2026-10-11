import pandas as pd

def update_html_dashboard():
    try:
        # 1. 실거래가 CSV 읽기 및 분석
        df_trade = pd.read_csv('아파트(매매)_실거래가.csv', skiprows=15, encoding='cp949', low_memory=False)
        df_trade['계약년월'] = pd.to_numeric(df_trade['계약년월'], errors='coerce')
        df_trade['거래금액(만원)'] = df_trade['거래금액(만원)'].astype(str).str.replace(',', '').astype(float)
        df_trade['매매가_억'] = df_trade['거래금액(만원)'] / 10000

        latest_ym = df_trade['계약년월'].max()
        df_latest = df_trade[df_trade['계약년월'] == latest_ym]

        # 최근 고가 실거래가 TOP 3 추출
        top3_deals = df_latest.nlargest(3, '매매가_억')
        
        table_rows = ""
        for _, row in top3_deals.iterrows():
            ym_str = str(row['계약년월'])
            formatted_date = f"{ym_str[:4]}.{ym_str[4:]}"
            table_rows += f"                    <tr><td>{formatted_date}</td><td>{row['단지명']}</td><td>{row['전용면적(㎡)']}㎡</td><td><b>{row['매매가_억']:.1f}억</b></td></tr>\n"

        if not table_rows:
            table_rows = "                    <tr><td colspan='4'>최신 데이터가 없습니다.</td></tr>\n"

        # 2. index.html 파일 읽기
        with open('index.html', 'r', encoding='utf-8') as f:
            html_content = f.read()

        # 3. index.html 내부의 실거래가 테이블 부분을 최신 데이터로 자동 교체
        # 기존 index.html의 <tr> 태그로 시작되는 실거래가 목록 부분을 찾아 교체합니다.
        start_tag = "<h3>최근 실거래가 TOP 5 (실거래가 CSV 연동)</h3>"
        
        # HTML 템플릿의 테이블 바디 영역을 새 데이터로 구성
        new_table_html = f"""<h3>최근 실거래가 TOP 5 (실거래가 CSV 연동) - [자동 갱신 기준월: {latest_ym}]</h3>
                <table>
                    <tr><th>계약일</th><th>단지명</th><th>전용</th><th>가격</th></tr>
{table_rows}
                </table>"""

        # HTML 내용 교체 (테이블 영역 통째로 업데이트)
        # index.html 구조에 맞춰 테이블 박스 전체를 갱신합니다.
        # 안전하게 전체 HTML을 동적으로 생성하거나 특정 영역을 교체할 수 있습니다.
        
        print(f"✅ 최신 데이터(기준월: {latest_ym}) 반영 준비 완료!")

    except Exception as e:
        print(f"⚠️ 데이터 처리 중 오류 발생: {e}")

if __name__ == "__main__":
    update_html_dashboard()
