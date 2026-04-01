import streamlit as st
import pandas as pd

# Налаштування сторінки
st.set_page_config(page_title='Аналітика трафіку', page_icon='🌐', layout='wide')
st.title('🌐 Аналітика трафіку вебсайту')

# --- 1. Завантаження даних ---
@st.cache_data
def load_data():
    df = pd.read_csv('website_traffic.csv')
    df['Дата'] = pd.to_datetime(df['Дата'])
    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error("Файл 'website_traffic.csv' не знайдено. Створіть його за наданим шаблоном.")
    st.stop()

# --- 2. Загальна статистика та графік відвідуваності ---
st.subheader('📈 Динаміка відвідуваності (Сеанси та Користувачі)')

# Групуємо дані за датою для загального графіка
daily_traffic = df.groupby('Дата')[['Користувачі', 'Сеанси']].sum()
st.line_chart(daily_traffic)

st.divider()

# --- 3. Джерела трафіку та Сегментація за пристроями ---
col1, col2 = st.columns(2)

with col1:
    st.subheader('🔗 Джерела трафіку')
    # Групуємо за джерелом
    source_traffic = df.groupby('Джерело')['Сеанси'].sum().reset_index()
    # Сортуємо для красивого відображення
    source_traffic = source_traffic.sort_values(by='Сеанси', ascending=False)
    st.bar_chart(source_traffic.set_index('Джерело'))

with col2:
    st.subheader('📱 Сегментація за пристроями')
    # Групуємо за пристроєм
    device_traffic = df.groupby('Пристрій')['Сеанси'].sum().reset_index()
    st.bar_chart(device_traffic.set_index('Пристрій'), color="#ff4b4b")

st.divider()

# --- 4. Кореляційний аналіз показників ---
st.subheader('🔗 Кореляційний аналіз показників')
st.write("Аналіз взаємозв'язку між різними числовими метриками сайту.")

# Вибираємо лише числові колонки для кореляції
numeric_cols = ['Користувачі', 'Сеанси', 'Показник_відмов_%', 'Тривалість_сеансу_сек']
corr_matrix = df[numeric_cols].corr()

# Виводимо матрицю з градієнтом кольору
st.dataframe(
    corr_matrix.style.background_gradient(cmap='coolwarm', axis=None).format("{:.2f}"),
    use_container_width=True
)

st.info("""
💡 **Як інтерпретувати кореляційну матрицю:**
* **Близько до 1 (червоний):** Сильний прямий зв'язок. Наприклад, 'Користувачі' та 'Сеанси' логічно мають кореляцію майже 1.0.
* **Близько до -1 (синій):** Сильний зворотний зв'язок. Наприклад, ми бачимо сильну негативну кореляцію між **'Показником відмов'** та **'Тривалістю сеансу'** (що вищий показник відмов, то менше часу люди проводять на сайті).
* **Близько до 0:** Зв'язку майже немає.
""")
