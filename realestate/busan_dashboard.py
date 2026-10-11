import pandas as pd

def process_real_estate_data():
    try:
        # 실거래가 데이터 로드 및 분석
        df_trade = pd.read_csv('아파트(매매)_실거래가.csv', skiprows=15, encoding='cp949', low_memory=False)
        df_trade['계약년월'] = pd.to_numeric(df_trade['계약년월'], errors='coerce')
        df_trade['거래금액(만원)'] = df_trade['거래금액(만원)'].astype(str).str.replace(',', '').astype(float)
        df_trade['매매가_억'] = df_trade['거래금액(만원)'] / 10000
        df_trade['구'] = df_trade['시군구'].apply(lambda x: str(x).split()[1] if len(str(x).split()) > 1 else '')

        latest_ym = df_trade['계약년월'].max()
        df_latest = df_trade[df_trade['계약년월'] == latest_ym]

        print(f"✅ 데이터 처리 완료 (기준 계약년월: {latest_ym}, 총 거래 건수: {len(df_latest)}건)")
        
        # 구별 매매평균가 TOP 5 출력 확인
        top5_gu = df_latest.groupby('구')['매매가_억'].mean().nlargest(5)
        print("\n[구별 매매평균가 TOP 5]")
        for gu, price in top5_gu.items():
            print(f" - {gu}: 약 {price:.2f}억 원")

    except Exception as e:
        print(f"⚠️ 데이터 처리 중 오류 발생: {e}")

if __name__ == "__main__":
    process_real_estate_data()