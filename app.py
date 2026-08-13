import streamlit as st
import requests
from pathlib import Path


# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Currency Converter",
    page_icon="💱",
    layout="centered"
)


# ==========================================================
# LOAD CSS
# ==========================================================

css_path = Path("assets/style.css")

if css_path.exists():
    css = css_path.read_text(encoding="utf-8")
    st.markdown(
        f"<style>{css}</style>",
        unsafe_allow_html=True
    )


# ==========================================================
# LOAD HTML HEADER
# ==========================================================

html_path = Path("templates/index.html")

if html_path.exists():
    html = html_path.read_text(encoding="utf-8")
    st.markdown(html, unsafe_allow_html=True)


# ==========================================================
# BANNER
# ==========================================================

st.image(
    "https://images.unsplash.com/photo-1580519542036-c47de6196ba5"
    "?auto=format&fit=crop&w=1200&q=80",
    use_container_width=True
)


# ==========================================================
# TITLE
# ==========================================================

st.markdown("### 🌍 Choose Your Currencies")

st.write(
    "Select a source currency, a target currency, "
    "and enter the amount you want to convert."
)


# ==========================================================
# CURRENCY OPTIONS
# ==========================================================

currency_options = {
    "🇮🇳 INR - Indian Rupee": "INR",
    "🇺🇸 USD - US Dollar": "USD",
    "🇪🇺 EUR - Euro": "EUR",
    "🇬🇧 GBP - British Pound": "GBP",
    "🇯🇵 JPY - Japanese Yen": "JPY",
    "🇦🇺 AUD - Australian Dollar": "AUD",
    "🇨🇦 CAD - Canadian Dollar": "CAD",
    "🇨🇭 CHF - Swiss Franc": "CHF",
    "🇨🇳 CNY - Chinese Yuan": "CNY",
    "🇸🇬 SGD - Singapore Dollar": "SGD",
    "🇳🇿 NZD - New Zealand Dollar": "NZD",
    "🇦🇪 AED - UAE Dirham": "AED",
    "🇸🇦 SAR - Saudi Riyal": "SAR",
    "🇶🇦 QAR - Qatari Riyal": "QAR",
    "🇰🇼 KWD - Kuwaiti Dinar": "KWD",
    "🇧🇭 BHD - Bahraini Dinar": "BHD",
    "🇴🇲 OMR - Omani Rial": "OMR",
    "🇲🇾 MYR - Malaysian Ringgit": "MYR",
    "🇹🇭 THB - Thai Baht": "THB",
    "🇭🇰 HKD - Hong Kong Dollar": "HKD",
    "🇿🇦 ZAR - South African Rand": "ZAR",
    "🇸🇪 SEK - Swedish Krona": "SEK",
    "🇳🇴 NOK - Norwegian Krone": "NOK",
    "🇩🇰 DKK - Danish Krone": "DKK",
    "🇵🇱 PLN - Polish Zloty": "PLN",
    "🇹🇷 TRY - Turkish Lira": "TRY",
    "🇷🇺 RUB - Russian Ruble": "RUB",
    "🇧🇷 BRL - Brazilian Real": "BRL",
    "🇲🇽 MXN - Mexican Peso": "MXN",
    "🇮🇩 IDR - Indonesian Rupiah": "IDR"
}

currency_labels = list(currency_options.keys())


# ==========================================================
# SESSION STATE
# ==========================================================

if "from_label" not in st.session_state:
    st.session_state.from_label = currency_labels[0]

if "to_label" not in st.session_state:
    st.session_state.to_label = currency_labels[1]

if "converted_amount" not in st.session_state:
    st.session_state.converted_amount = None

if "exchange_rate" not in st.session_state:
    st.session_state.exchange_rate = None

if "rate_date" not in st.session_state:
    st.session_state.rate_date = None


# ==========================================================
# SWAP FUNCTION
# ==========================================================

def swap_currencies():

    old_from = st.session_state.from_label
    old_to = st.session_state.to_label

    st.session_state.from_label = old_to
    st.session_state.to_label = old_from

    # Clear old result
    st.session_state.converted_amount = None
    st.session_state.exchange_rate = None
    st.session_state.rate_date = None


# ==========================================================
# SIDEBAR
# ==========================================================

st.sidebar.markdown("## 🌈 Conversion Settings")

st.sidebar.caption(
    "✨ Choose currencies and amount to convert ✨"
)

st.sidebar.markdown("---")


# ==========================================================
# AMOUNT
# ==========================================================

amount = st.sidebar.number_input(
    "💵 Amount",
    min_value=0.0,
    value=100.0,
    step=1.0
)


# ==========================================================
# CURRENCY SELECTION
# ==========================================================

st.sidebar.markdown("### 💱 Currency Selection")


st.sidebar.selectbox(
    "🌍 From Currency",
    currency_labels,
    key="from_label"
)


st.sidebar.selectbox(
    "🌎 To Currency",
    currency_labels,
    key="to_label"
)


from_label = st.session_state.from_label
to_label = st.session_state.to_label

from_currency = currency_options[from_label]
to_currency = currency_options[to_label]


# ==========================================================
# SWAP BUTTON
# ==========================================================

st.sidebar.button(
    "🔄 Swap Currencies",
    on_click=swap_currencies,
    use_container_width=True
)

st.sidebar.markdown("---")


# ==========================================================
# API FUNCTION
# ==========================================================

def get_exchange_rate(from_currency, to_currency):

    if from_currency == to_currency:
        return 1.0, "Same Currency"

    url = (
        f"https://open.er-api.com/v6/latest/"
        f"{from_currency}"
    )

    try:

        response = requests.get(
            url,
            timeout=20
        )

        response.raise_for_status()

        data = response.json()

        if data.get("result") != "success":

            return None, "API did not return success."

        rates = data.get("rates", {})

        if to_currency not in rates:

            return None, (
                f"Rate for {to_currency} "
                "was not found."
            )

        rate = float(rates[to_currency])

        update_time = data.get(
            "time_last_update_utc",
            "Not available"
        )

        return rate, update_time

    except requests.exceptions.Timeout:

        return None, "Request timed out."

    except requests.exceptions.ConnectionError:

        return None, (
            "Could not connect to the exchange "
            "rate server."
        )

    except requests.exceptions.HTTPError as e:

        return None, f"HTTP error: {e}"

    except Exception as e:

        return None, str(e)


# ==========================================================
# CONVERT BUTTON
# ==========================================================

if st.button(
    "💸 Convert Now",
    type="primary",
    use_container_width=True
):

    if amount <= 0:

        st.error(
            "❌ Please enter an amount greater than 0."
        )

    else:

        rate, rate_date = get_exchange_rate(
            from_currency,
            to_currency
        )

        if rate is not None:

            # Calculate amount
            converted = amount * rate

            # Save result
            st.session_state.converted_amount = converted
            st.session_state.exchange_rate = rate
            st.session_state.rate_date = rate_date

        else:

            st.session_state.converted_amount = None
            st.session_state.exchange_rate = None

            st.error(
                f"❌ Unable to convert currency.\n\n"
                f"Reason: {rate_date}"
            )


# ==========================================================
# DISPLAY CONVERSION RESULT
# ==========================================================

if st.session_state.converted_amount is not None:

    converted = st.session_state.converted_amount
    rate = st.session_state.exchange_rate
    rate_date = st.session_state.rate_date

    st.markdown("---")

    st.markdown("## 💰 Conversion Result")


    # ======================================================
    # AMOUNT DISPLAY
    # ======================================================

    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            label=f"💵 {from_currency}",
            value=f"{amount:,.2f}"
        )


    with col2:

        st.markdown(
            "<h1 style='text-align:center;'>➡️</h1>",
            unsafe_allow_html=True
        )


    with col3:

        st.metric(
            label=f"💰 {to_currency}",
            value=f"{converted:,.2f}"
        )


    # ======================================================
    # LARGE RESULT
    # ======================================================

    st.success(
        f"💰 {amount:,.2f} {from_currency} "
        f"= {converted:,.2f} {to_currency}"
    )


    # ======================================================
    # EXCHANGE RATE
    # ======================================================

    st.markdown("### 💹 Live Exchange Rate")


    rate_col1, rate_col2 = st.columns(2)


    with rate_col1:

        st.metric(
            "Exchange Rate",
            f"{rate:.8f}"
        )


    with rate_col2:

        st.metric(
            "Currency Pair",
            f"{from_currency} → {to_currency}"
        )


    st.info(
        f"**1 {from_currency} = "
        f"{rate:.8f} {to_currency}**\n\n"
        f"🕒 Rate updated: {rate_date}"
    )


    st.balloons()

    st.toast(
        "Conversion Successful! 🎉",
        icon="💸"
    )


# ==========================================================
# POPULAR CURRENCY PAIRS
# ==========================================================

st.markdown("---")

st.markdown("### 🌟 Popular Currency Pairs")


col1, col2, col3 = st.columns(3)

with col1:
    st.info("🇮🇳 INR → 🇺🇸 USD")

with col2:
    st.info("🇺🇸 USD → 🇪🇺 EUR")

with col3:
    st.info("🇯🇵 JPY → 🇬🇧 GBP")


col4, col5, col6 = st.columns(3)

with col4:
    st.info("🇬🇧 GBP → 🇮🇳 INR")

with col5:
    st.info("🇪🇺 EUR → 🇺🇸 USD")

with col6:
    st.info("🇦🇺 AUD → 🇨🇦 CAD")


# ==========================================================
# FOOTER
# ==========================================================

st.markdown(
    """
    <div class="footer">
        Thank you for using our Currency Converter! 💱✨
    </div>

    <style>
        .footer {
            margin-top: 40px;
            margin-bottom: 20px;
            padding: 18px;
            text-align: center;

            background: transparent;

            border: 1px solid rgba(255, 255, 255, 0.35);
            border-radius: 15px;

            backdrop-filter: blur(8px);
            -webkit-backdrop-filter: blur(8px);

            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);

            font-size: 16px;
            font-weight: 500;
        }
    </style>
    """,
    unsafe_allow_html=True
)