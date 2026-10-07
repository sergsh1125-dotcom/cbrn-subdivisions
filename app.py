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

# Custom CSS для темного фону, білих заголовків та ЖОВТОЇ КНОПКИ бічної панелі
st.markdown(
    """
    <style>
    /* Приховуємо лише верхнє меню Streamlit та футер */
    #MainMenu {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    
    /* Фіксуємо темну тему для додатка */
    .stApp, [data-testid="stSidebar"], [data-testid="stSidebarContent"] {
        background-color: #0E1117 !important;
        color: #FAFAFA !important;
    }

    /* Заголовки залишаємо білими */
    h1, h2, h3, h4, h5, h6, 
    .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6,
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: #FAFAFA !important;
        font-weight: bold !important;
    }

    /* ЖОВТИЙ КВАДРАТ ДЛЯ КНОПКИ РОЗГОРТАННЯ / ЗГОРТАННЯ ПАНЕЛІ */
    [data-testid="stSidebarCollapseButton"] button,
    [data-testid="stSidebarCollapsedControl"] button,
    button[aria-label="Open sidebar"],
    button[aria-label="Close sidebar"],
    button[data-testid="baseButton-header"] {
        background-color: #FFD700 !important;
        border: 2px solid #FFD700 !important;
        border-radius: 8px !important;
        opacity: 1 !important;
        visibility: visible !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        box-shadow: 0px 2px 6px rgba(0,0,0,0.6) !important;
    }

    /* Чорна іконка всередині жовтого квадрата */
    [data-testid="stSidebarCollapseButton"] svg,
    [data-testid="stSidebarCollapsedControl"] svg,
    button[aria-label="Open sidebar"] svg,
    button[aria-label="Close sidebar"] svg,
    button[data-testid="baseButton-header"] svg {
        color: #000000 !important;
        fill: #000000 !important;
        stroke: #000000 !important;
        width: 22px !important;
        height: 22px !important;
    }

    /* Текст для всіх елементів */
    label, p, span, div, .stMarkdown {
        color: #FAFAFA !important;
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
# БІЧНА ПАНЕЛЬ: НАЛАШТУВАННЯ НОРМАТИВІВ
# ==========================================
st.sidebar.header("МОЖЛИВОСТІ ПІДРОЗДІЛІВ РХБ ЗАХИ
