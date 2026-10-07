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
    initial_sidebar_state="expanded",
)

st.title("Розрахунок сил та засобів РХБЗ")
st.markdown("""
Цей застосунок призначений для оперативної оцінки необхідної кількості підрозділів радіаційної та хімічної розвідки (РХР), 
санітарної обробки людей, а також спеціальної обробки (дегазації/дезактивації) техніки.
""")

# ==========================================
# БІЧНА ПАНЕЛЬ: НАЛАШТУВАННЯ НОРМАТИВІВ
# ==========================================
st.sidebar.header("МОЖЛИВОСТІ ПІДРОЗДІЛІВ РХБ ЗАХИСТУ")

with st.sidebar.expander("Можливості відділення РХ розвідки (1 СМРХР):", expanded=False):
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

with st.sidebar.expander("Можливості відділення санітарної обробки (1 комплект для сан. обробки)", expanded=False):
    san_capacity_per_unit = st.number_input(
        "Санітарна обробка людей (люд/год)",
        min_value=5,
        max_value=200,
        value=40,
        step=5,
   )

with st.sidebar.expander(
    "Можливості відділення спец. обробки техніки (1 СМРХЗ)", expanded=False
):
    decontam_light_time = st.number_input(
        "Обробка легкових автомобілів (од/год)",
        min_value=5,
        max_value=120,
        value=20,
        step=5,
    )
    decontam_heavy_time = st.number_input(
        "Обробка вантажших та спец. автомобілів (од/год)",
        min_value=10,
        max_value=180,
        value=40,
        step=5,
    )


# ==========================================
# ОСНОВНА ПАНЕЛЬ: ВХІДНІ ДАНІ ДЛЯ ЗАВДАННЯ
# ==========================================
st.subheader("Вихідні дані для розрахунку")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("Радіаційна та хімічна розвідка")
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
    st.markdown("Санітарна обробка людей")
    personnel_count = st.number_input(
        "Кількість людей",
        min_value=0,
        value=250,
        step=10,
    )

with col3:
    st.markdown("Спеціальна обробка техніки")
    light_vehicles = st.number_input(
        " Легкові автомобілі (од)",
        min_value=0,
        value=15,
        step=1,
    )
    heavy_vehicles = st.number_input(
        "Вантажні та спец. автомобілі (од)",
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

# 3. Спеціальна обробка техніки
total_decontam_hours = (light_vehicles * (decontam_light_time / 60.0)) + (
    heavy_vehicles * (decontam_heavy_time / 60.0)
)
decontam_units_required = math.ceil(total_decontam_hours / time_limit)


# ==========================================
# ВІДОБРАЖЕННЯ РЕЗУЛЬТАТІВ
# ==========================================
st.markdown("Результати розрахунку необхідних сил і засобів РХБ захисту")

m_col1, m_col2, m_col3 = st.columns(3)

with m_col1:
    st.metric(
        label="Відділень РХР",
        value=f"{rhr_units_required} од.",
        delta=f"Обсяг: {rhr_val} "
        + ("км" if rhr_type == "Маршрут (км)" else "км²"),
    )

with m_col2:
    st.metric(
        label="Відділень сан. обробки",
        value=f"{san_units_required} од.",
        delta=f"людей: {personnel_count}",
    )

with m_col3:
    st.metric(
        label="Відділень спец. обробки",
        value=f"{decontam_units_required} од.",
        delta=f"Всього техніки: {light_vehicles + heavy_vehicles} од.",
    )

st.markdown("---")

# Візуалізація результатів
col_chart, col_summary = st.columns([1.2, 1])

with col_chart:
    st.markdown("Необхідна кількість підрозділів")

    categories = [
        "Відділення РХР",
        "Відділення сан. обробки",
        "Відділення спец. обробки техніки",
    ]
    values = [rhr_units_required, san_units_required, decontam_units_required]

    fig, ax = plt.subplots(figsize=(6, 3.5))
    bars = ax.barh(categories, values, color=["#1f77b4", "#ff7f0e", "#2ca02c"])
    ax.set_xlabel("Кількість підрозділів / відділень (од)")
    ax.set_xlim(0, max(values + [5]) + 2)

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
        )

    plt.tight_layout()
    st.pyplot(fig)

with col_summary:
    st.markdown("Деталізація та звіт")

    report_data = {
        "Категорія": [
            "Розвідка (РХР)",
            "Санітарна обробка",
            "Дегазація/Дезактивація техніки",
        ],
        "Обсяг завдань": [
            f"{rhr_val} " + ("км" if rhr_type == "Маршрут (км)" else "км²"),
            f"{personnel_count} осіб",
            f"{light_vehicles} легкових, {heavy_vehicles} вантажних",
        ],
        "Нормативна спроможність на 1 од.": [
            (
                f"{rhr_speed_route} км/год"
                if rhr_type == "Маршрут (км)"
                else f"{rhr_speed_area} км²/год"
            ),
            f"{san_capacity_per_unit} осіб/год",
            f"{decontam_light_time} год/ {decontam_heavy_time} год",
        ],
        "Загальна трудомісткість": [
            f"{rhr_val / (rhr_speed_route if rhr_type == 'Маршрут (км)' else rhr_speed_area):.1f} маш.-год",
            f"{personnel_count / san_capacity_per_unit:.1f} маш.-год",
            f"{total_decontam_hours:.1f} маш.-год",
        ],
        "Необхідна кількість": [
            f"{rhr_units_required} од.",
            f"{san_units_required} од.",
            f"{decontam_units_required} од.",
        ],
    }

    df_report = pd.DataFrame(report_data)
    st.dataframe(df_report, hide_index=True, use_container_width=True)

    # Експорт у CSV
    csv_buffer = io.StringIO()
    df_report.to_csv(csv_buffer, index=False, encoding="utf-8-sig")

    st.download_button(
        label="📥 Завантажити звіт у CSV",
        data=csv_buffer.getvalue(),
        file_name="cbrn_calculation_report.csv",
        mime="text/csv",
    )
