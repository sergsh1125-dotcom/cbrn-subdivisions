import io
import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

# Налаштування сторінки
st.set_page_config(
    page_title="Розрахунок сил та засобів РХБ захисту",
    page_icon="🛡️",
    layout="wide",
)

# Повне приховування службових іконок Streamlit Cloud та стилізація
st.markdown(
    """
    <style>
    /* Приховуємо службову шапку та меню */
    header, [data-testid="stHeader"], #MainMenu, footer {
        display: none !important;
        height: 0px !important;
        visibility: hidden !important;
    }

    /* Фіксуємо темну тему та білий колір тексту */
    .stApp {
        background-color: #0E1117 !important;
        color: #FFFFFF !important;
    }

    h1, h2, h3, h4, h5, h6,
    label, p, span, div, .stMarkdown {
        color: #FFFFFF !important;
    }
    
    /* Відступ зверху */
    .block-container {
        padding-top: 1.5rem !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)

st.title("Розрахунок сил та засобів РХБЗ")
st.markdown("""
Цей застосунок призначений для оперативної оцінки необхідної кількості підрозділів радіаційної та хімічної розвідки (РХР), 
санітарної обробки людей, а також спеціальної обробки (дегазації/дезактивації) техніки.
""")

# ==========================================
# БЛОК НАЛАШТУВАННЯ НОРМАТИВІВ (В ОСНОВНІЙ ПАНЕЛІ)
# ==========================================
with st.expander("⚙️ МОЖЛИВОСТІ ПІДРОЗДІЛІВ РХБ ЗАХИСТУ (НАЛАШТУВАННЯ НОРМАТИВІВ)", expanded=False):
    cap_col1, cap_col2, cap_col3 = st.columns(3)
    
    with cap_col1:
        st.markdown("#### 1. Відділення РХ розвідки (1 СМРХР)")
        rhr_speed_route = st.number_input(
            "РХ розвідка маршруту (км/год)",
            min_value=1.0,
            max_value=50.0,
            value=15.0,
            step=1.0,
        )
        rhr_speed_area = st.number_input(
            "РХ розвідка району (км²/год)",
            min_value=0.5,
            max_value=20.0,
            value=3.0,
            step=0.5,
        )

    with cap_col2:
        st.markdown("#### 2. Відділення санітарної обробки")
        san_capacity_per_unit = st.number_input(
            "Санітарна обробка людей (люд/год)",
            min_value=5,
            max_value=200,
            value=40,
            step=5,
        )

    with cap_col3:
        st.markdown("#### 3. Відділення спец. обробки (1 СМРХЗ)")
        decontam_degas_rate = st.number_input(
            "Дегазація / Дезінфекція (легкових авт./год)",
            min_value=1,
            max_value=60,
            value=20,
            step=1,
            help="Норма для легкового авто (нанесення розчину розпилювачем)",
        )
        decontam_deact_rate = st.number_input(
            "Дезактивація (легкових авт./год)",
            min_value=1,
            max_value=60,
            value=10,
            step=1,
            help="Норма для легкового авто (змивання під тиском зі щітками)",
        )

    st.info("💡 **Примітка щодо розрахунку техніки:** Прийнято оперативно-тактичне допущення, що 1 вантажний автомобіль або 1 автобус за обсягом робіт дорівнює 2 легковим автомобілям.")

st.markdown("---")

# ==========================================
# ОСНОВНА ПАНЕЛЬ: ВХІДНІ ДАНІ ДЛЯ ЗАВДАННЯ
# ==========================================
st.subheader("Вихідні дані для розрахунку")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### Радіаційна та хімічна розвідка")
    rhr_type = st.radio(
        "Об'єкти розвідки:", ["Маршрут (км)", "Район / Площа (км²)"]
    )
    if rhr_type == "Маршрут (км)":
        rhr_val = st.number_input(
            "Протяжність маршруту (км)",
            min_value=0.0,
            value=45.0,
            step=5.0,
        )
    else:
        rhr_val = st.number_input(
            "Площа району (км²)", min_value=0.0, value=12.0, step=1.0
        )

with col2:
    st.markdown("### Санітарна обробка людей")
    personnel_count = st.number_input(
        "Кількість людей",
        min_value=0,
        value=250,
        step=10,
    )

with col3:
    st.markdown("### Спеціальна обробка техніки")
    decontam_type = st.radio(
        "Вид спеціальної обробки:",
        ["Дегазація (дезінфекція)", "Дезактивація"],
    )
    light_vehicles = st.number_input(
        "Легкові автомобілі (од)",
        min_value=0,
        value=15,
        step=1,
    )
    heavy_and_buses = st.number_input(
        "Вантажні автомобілі та автобуси (од)",
        min_value=0,
        value=8,
        step=1,
    )

st.markdown("---")
time_limit = st.slider(
    "Термін для проведення заходів РХБ захисту (годин)",
    min_value=0.5,
    max_value=24.0,
    value=2.0,
    step=0.5,
)


# ==========================================
# ЛОГІКА РОЗРАХУНКУ
# ==========================================
# 1. РХР
if rhr_type == "Маршрут (км)":
    capacity_rhr = rhr_speed_route * time_limit
    rhr_units_required = (
        math.ceil(rhr_val / capacity_rhr) if capacity_rhr > 0 else 0
    )
else:
    capacity_rhr = rhr_speed_area * time_limit
    rhr_units_required = (
        math.ceil(rhr_val / capacity_rhr) if capacity_rhr > 0 else 0
    )

# 2. Санітарна обробка
capacity_san = san_capacity_per_unit * time_limit
san_units_required = (
    math.ceil(personnel_count / capacity_san) if capacity_san > 0 else 0
)

# 3. Спеціальна обробка техніки (Зведення до умовних легкових авто: 1 вантажне/автобус = 2 легкових)
equiv_light_vehicles = light_vehicles + (heavy_and_buses * 2)

if decontam_type == "Дегазація (дезінфекція)":
    current_decontam_rate = decontam_degas_rate
else:
    current_decontam_rate = decontam_deact_rate

capacity_decontam_per_unit = current_decontam_rate * time_limit
decontam_units_required = (
    math.ceil(equiv_light_vehicles / capacity_decontam_per_unit)
    if capacity_decontam_per_unit > 0
    else 0
)


# ==========================================
# ВІДОБРАЖЕННЯ РЕЗУЛЬТАТІВ
# ==========================================
st.subheader("Результати розрахунку необхідних сил і засобів РХБ захисту")

m_col1, m_col2, m_col3 = st.columns(3)

with m_col1:
    st.metric(
        label="Відділень РХР",
        value=f"{rhr_units_required}",
        delta=f"Обсяг: {rhr_val} "
        + ("км" if rhr_type == "Маршрут (км)" else "км²"),
    )

with m_col2:
    st.metric(
        label="Відділень сан. обробки",
        value=f"{san_units_required}",
        delta=f"людей: {personnel_count}",
    )

with m_col3:
    st.metric(
        label=f"Відділень спец. обробки ({decontam_type})",
        value=f"{decontam_units_required}",
        delta=f"Всього техніки: {light_vehicles + heavy_and_buses} од. ({equiv_light_vehicles} умов. од.)",
    )

st.markdown("---")

# Візуалізація результатів
col_chart, col_summary = st.columns([1, 1.2])

with col_chart:
    st.subheader("Необхідна кількість підрозділів")

    categories = [
        "Відділення РХР",
        "Відділення сан. обробки",
        "Відділення спец. обробки",
    ]
    values = [rhr_units_required, san_units_required, decontam_units_required]

    fig, ax = plt.subplots(figsize=(3.5, 2.0))
    bars = ax.barh(categories, values, color=["#1f77b4", "#ff7f0e", "#2ca02c"])
    ax.set_xlabel("Кількість (відділень)", fontsize=8)
    ax.set_xlim(0, max(values + [5]) + 2)
    ax.tick_params(axis="both", labelsize=7)

    # Додавання значень на бари
    for bar in bars:
        width = bar.get_width()
        ax.text(
            width + 0.1,
            bar.get_y() + bar.get_height() / 2,
            f"{int(width)}",
            ha="left",
            va="center",
            fontweight="bold",
            fontsize=8,
        )

    plt.tight_layout()
    st.pyplot(fig)

with col_summary:
    st.subheader("Деталізація та звіт")

    report_data = {
        "Категорія": [
            "Розвідка (РХР)",
            "Санітарна обробка",
            f"Спец. обробка ({decontam_type})",
        ],
        "Обсяг завдань": [
            f"{rhr_val} " + ("км" if rhr_type == "Маршрут (км)" else "км²"),
            f"{personnel_count} осіб",
            f"{light_vehicles} легкових, {heavy_and_buses} вантажних/автобусів ({equiv_light_vehicles} умов. од.)",
        ],
        "Термін виконання": [
            f"{time_limit} год",
            f"{time_limit} год",
            f"{time_limit} год",
        ],
        "Можливості 1 відділення": [
            (
                f"{rhr_speed_route} км/год"
                if rhr_type == "Маршрут (км)"
                else f"{rhr_speed_area} км²/год"
            ),
            f"{san_capacity_per_unit} осіб/год",
            f"{current_decontam_rate} умов. од./год",
        ],
        "Необхідна кількість відділень": [
            f"{rhr_units_required}",
            f"{san_units_required}",
            f"{decontam_units_required}",
        ],
    }

    df_report = pd.DataFrame(report_data)
    st.dataframe(df_report, hide_index=True, use_container_width=True)

    st.caption("Примітка: 1 вантажний автомобіль або 1 автобус прирівнюється до 2 умовних легкових автомобілів.")

    # Експорт у CSV
    csv_buffer = io.StringIO()
    df_report.to_csv(csv_buffer, index=False, encoding="utf-8-sig")

    st.download_button(
        label="📥 Завантажити звіт у CSV",
        data=csv_buffer.getvalue(),
        file_name="cbrn_calculation_report.csv",
        mime="text/csv",
    )
