import streamlit as st
import numpy as np
import pandas as pd
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
import time
import metapy as meta
from analyser import analyser
from cssactivate import local_css
from PIL import Image
import re
from directories import get_directory, get_main_show_image
from languagemodels import get_translation

#Initialise state -- for when user clicks 'Generate phrases'
if 'button_clicked' not in st.session_state:
    st.session_state['button_clicked'] = False

def callback():
    st.session_state['button_clicked'] = True

def callback_revert():
    st.session_state['button_clicked'] = False

st.set_page_config(
    page_title="Netflix & Learn",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

col1, colmid, col2 = st.columns([6, 0.15, 4])
with col2:
    st.image("images/netflixandlearn.jpg", width=250)
    st.markdown(meta.SIDEBAR_INFO, unsafe_allow_html=True)

    with st.expander("What is this all about?", expanded=False):
        st.markdown(meta.STORY, unsafe_allow_html=True)

with col1:
    st.markdown(meta.HEADER_INFO, unsafe_allow_html=True)

    st.markdown(meta.APP_INFO, unsafe_allow_html=True)
    lang_selec = st.selectbox("Choose the language you are learning (only German supported currently)", index=0, options=["German"], on_change = callback_revert)
    show_selec = st.selectbox("Choose the show you want to watch", index=0, options=["Babylon Berlin", "Biohackers", "Dark"], on_change = callback_revert)
    phrase_selec = st.slider('Choose the maximum amount of phrases per episode you wish to focus on', 1, 10, 5, on_change = callback_revert)  # min: 1, max: 10, default: 5
    ngram_selec = st.slider('Choose the amount of words per phrase you wish to focus on', 2, 6, 4, on_change = callback_revert)  # min: 2, max: 5, default: 4

    generate_button = st.button('Start Netflix & Learning!', on_click = callback)

st.markdown(
    "<hr />",
    unsafe_allow_html=True )


if generate_button or st.session_state['button_clicked'] == True:
    with st.spinner(f"Generating phrases for {show_selec}"):
        @st.cache(show_spinner=False)  # 👈 This function will be cached
        def generate_main_df(language, show, words_per_ngram, ngrams_per_episode):
            ''' Generates a dataframe based on the users selections in the app '''
            main_df = analyser(language, show, words_per_ngram, ngrams_per_episode)
            return main_df
        
        main_df = generate_main_df(lang_selec, show_selec, ngram_selec, phrase_selec)
        main_df = main_df.sort_values(by=['Episode'])
    
    output_format_selec = st.radio("Output format", ('List', 'Spreadsheet'), on_change = callback)

    if output_format_selec == 'List':

        colep1, colep2 = st.columns([6, 4])
        
        with colep1:
            episode_selection = st.selectbox(
                'Which episode are you about to watch?',
                main_df['Episode'].unique(),
                on_change = callback)
        
        if st.session_state['button_clicked'] == True:
            episode_df = main_df.loc[main_df['Episode'] == episode_selection]
            episode_df = episode_df.sort_values(by=['Subtitle start time'])

            col1a, coldmida, col2a, col3a = st.columns([1.5, 0.15, 5.35, 1])
            
            with col1a:
                episode_image_dir = get_directory(lang_selec, show_selec, "images")
                episode_image = get_main_show_image(episode_image_dir, show_selec)
                st.image(episode_image, width=225)

            with col2a:
                phrases_list = list(episode_df['Phrase'])

                local_css("asset/css/style.css")
                st.markdown(
                    " ".join([
                        "<div>",
                        # f"<h3>{episode_selection}</h3>",
                        "</div>",
                        '<div><div></div></div>',
                        "<h2>Phrases</h2>",
                        "<ul class='phrases-list font-body'>",
                        " ".join([f'<li>{phrase}</li>' for phrase in phrases_list]),
                        "</ul>"
                    ]),
                    unsafe_allow_html=True
                )

            col1b, col2b = st.columns([6, 4])
            with col1b:
                phrase_counter = 1
                for index, row in episode_df.iterrows():
                    phrase_in_row_text = row['Phrase']
                    phrase_in_row_count = row['# of occurences']
                    phrase_in_row_ep_count = row['# of episodes']
                    phrase_in_row_ep_start_time = row['Subtitle start time']
                    phrase_in_row_dialogue_short = row['Subtitle shortened']
                    phrase_in_row_dialogue = row['Featured dialogue'] 

                    phrase_in_row_dialogue_2 = phrase_in_row_dialogue.replace(phrase_in_row_dialogue_short, f"**{phrase_in_row_dialogue_short}**")

                    phrase_description = f'''> ## Phrase #{phrase_counter}:
                            > ### {phrase_in_row_text}
                            >
                            > - *\# of occurences throughout show:* **{phrase_in_row_count}**
                            > - *\# of episodes featured in:* **{phrase_in_row_ep_count}**
                            > - *Timestamp in episode:* **{phrase_in_row_ep_start_time}**
                            >
                            >  "{phrase_in_row_dialogue_2}"'''
                    
                    phrase_counter += 1
                    st.markdown(phrase_description)

                    dialogue_translated = get_translation(lang_selec, phrase_in_row_dialogue_2)
                    with st.expander("Dialogue translation", expanded=False):
                        st.markdown(dialogue_translated, unsafe_allow_html=True)

    elif output_format_selec == 'Spreadsheet':
        main_df_short = main_df.drop(['Phrase rank', 'Subtitle shortened'], axis=1)
        gb = GridOptionsBuilder.from_dataframe(main_df_short, enableValue=True)
        gb.configure_pagination()
        gridOptions = gb.build()
        
        AgGrid(main_df_short, gridOptions=gridOptions, enable_enterprise_modules=True, fit_columns_on_grid_load = True, height = 350)

