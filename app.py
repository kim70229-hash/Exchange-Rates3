
import streamlit as st
import requests

st.set_page_config(
    page_title="실시간 환율 조회",
    page_icon="💱",
    layout="centered"
)

st.title("💱 실시간 환율 조회")
st.write("Frankfurter API를 활용한 환율 조회 서비스입니다.")

st.divider()

# 통화 목록
currencies = {
    "미국 달러 (USD)": "USD",
    "한국 원화 (KRW)": "KRW",
    "일본 엔화 (JPY)": "JPY",
    "유럽 유로 (EUR)": "EUR",
    "중국 위안 (CNY)": "CNY",
    "영국 파운드 (GBP)": "GBP",
}

st.subheader("환율 조회")

# 통화 선택
col1, col2 = st.columns(2)

with col1:
    base_name = st.selectbox(
        "기준 통화",
        list(currencies.keys()),
        index=0
    )

with col2:
    target_name = st.selectbox(
        "변환 통화",
        list(currencies.keys()),
        index=1
    )

base_currency = currencies[base_name]
target_currency = currencies[target_name]

# 환율 조회 함수
def get_exchange_rate(base, target):
    url = "https://api.frankfurter.dev/v2/rates"

    params = {
        "base": base,
        "quotes": target
    }

    response = requests.get(
        url,
        params=params,
        timeout=10
    )

    response.raise_for_status()

    data = response.json()
    return data


# 환산할 금액 입력
amount = st.number_input(
    "환산할 금액을 입력하세요",
    min_value=0.01,
    value=100.0,
    step=10.0
)

# 조회 버튼
if st.button("환율 조회하기"):

    if base_currency == target_currency:
        st.warning("서로 다른 통화를 선택해 주세요.")

    else:
        try:
            data = get_exchange_rate(
                base_currency,
                target_currency
            )

            if data:
                rate = data[0]["rate"]
                date = data[0]["date"]

                converted_amount = amount * rate

                st.success("환율 조회 성공!")

                st.metric(
                    label=f"1 {base_currency} 기준 환율",
                    value=f"{rate:,.4f} {target_currency}"
                )

                st.subheader("환산 결과")

                st.metric(
                    label=f"{amount:,.2f} {base_currency}",
                    value=f"{converted_amount:,.2f} {target_currency}"
                )

                st.caption(f"환율 기준일: {date}")

            else:
                st.warning("환율 데이터가 없습니다.")

        except requests.exceptions.RequestException as e:
            st.error(f"API 연결 오류: {e}")

        except (KeyError, IndexError, TypeError):
            st.error("환율 데이터 형식이 올바르지 않습니다.")
