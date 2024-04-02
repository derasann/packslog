import streamlit as st
import pandas as pd
import openpyxl
import random

# pip install streamlit pandas openpyxl

st.set_page_config(page_title='練習記録app')
st.title("練習記録app")

df = pd.read_excel('pack.xlsx', sheet_name='Sheet1', index_col=0)

with st.expander('df', expanded=False):
    st.table(df)

st.markdown('##### 積み重ねが大切')
len_df = len(df)
num = random.randint(0, len_df - 1)
s_selected = df.loc[num]
val = s_selected.loc['内容']
st.write(val)

# 入力回数を記録する変数を定義
count = 0
# アイコンを格納する変数
icons = ''
# 日付を格納する変数
date_str = ''

def add_row():
    global count, icons, date_str
    new_text = st.text_input('追加する内容を入力', key='new_text')
    date_input = st.date_input('日付を入力', key='date_input')
    date_str = str(date_input)  # 日付を文字列に変換

    if new_text != '':
        new_row = {'内容': new_text, '日付': date_str}
        global df
        df.loc[len_df] = new_row
        df.to_excel('pack.xlsx')
        st.table(df)
        
        count += 1  # 入力回数をカウントアップ
        icons += '■'  # iconsに'■'を追加
        st.markdown(f'##### 入力回数: {icons}')  # アイコンを表示
        
        if count == 5:  # 5回入力した場合
            st.success('練習をすこし継続しました!')  # メッセージを表示
        if count == 10:  # 10回入力した場合
            st.success('練習をだいぶ継続しました!')  # メッセージを表示
        if count == 20:  # 20回入力した場合
            st.success('練習をかなり継続しました!')  # メッセージを表示

# 画像を表示する
st.image('gate.png', caption='がんばれ', use_column_width=True)


# 行の削除
def drop_row():
    with st.form('form'):
        num_delete = st.number_input('削除する行番号を入力', step=1, key='num_delete')
        submitted = st.form_submit_button('submitted')
        if submitted:
            global df
            df = df.drop(num_delete)
            df = df.reset_index(drop=True)
            df.to_excel('pack.xlsx')
            st.table(df)

def main():
    apps = {
        '-': None,
        '行の追加': add_row,
        '行の削除': drop_row
    }
    selected_app_name = st.sidebar.selectbox(label='項目の選択', options=list(apps.keys()))
    if selected_app_name == '-':
        st.info('行の追加・削除はサイドバーから')
        st.stop()
    render_func = apps[selected_app_name]
    render_func()

if __name__ == '__main__':
    main()

