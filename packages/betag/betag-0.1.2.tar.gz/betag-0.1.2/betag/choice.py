import random
from typing import List
import streamlit as st
import streamlit.components.v1 as components
import sys
import pandas as pd

ITEM_INDEX_KEY = "item_index"

argv = sys.argv
# print(argv)
input_path = argv[1]
text_column = argv[2]
label_column = argv[3]
options = argv[4].split(",")

st.set_page_config("Choice")


@st.cache(allow_output_mutation=True)
def load(path: str):
    df = pd.read_csv(path)
    if label_column not in df.columns:
        df[label_column] = None
    return df


def save(df: pd.DataFrame, path: str):
    df.to_csv(path, index=False)


def get_random_index(df) -> int:
    indices = list(df[df[label_column].isna()].index.values)
    if len(indices) > 0:
        return random.choice(indices)


def label_example(index: int, option: str):
    print(index, option)
    df.loc[index, label_column] = option
    st.session_state[ITEM_INDEX_KEY] = get_random_index(df)
    save(df, input_path)
    print(df)


df = load(input_path)

if ITEM_INDEX_KEY not in st.session_state:
    st.session_state[ITEM_INDEX_KEY] = get_random_index(df)

index = st.session_state[ITEM_INDEX_KEY]


def make_cb(option: str):
    def f():
        label_example(index, option)

    return f


if index is None:
    st.header("Nothing left to label!")
else:
    st.header(df[text_column].iloc[index])
    cols = st.columns([1] * len(options))

    for i, option in enumerate(options):
        with cols[i]:
            st.button(f"{option} ({i+1})", on_click=make_cb(option))


def gen_html_key_map(options: List[str]):
    buttons = []
    for i, option in enumerate(options):
        option_text = f"{option} ({i+1})"
        buttons.append(f"'{i+1}': buttons.find(el => el.innerText === '{option_text}')")
    return "{" + ",".join(buttons) + "};"


components.html(
    """
<script>
const doc = window.parent.document;
buttons = Array.from(doc.querySelectorAll('button[kind=primary]'));
key_map = %s
doc.addEventListener('keydown', function(e) {
    console.log(event.key)
    if (key_map[event.key]) {
        key_map[event.key].click();
    }
});
</script>
"""
    % gen_html_key_map(options),
    height=0,
    width=0,
)


def progress(df: pd.DataFrame) -> float:
    return df[label_column].notna().sum() / len(df)


st.sidebar.title("betag")
st.sidebar.title("Progress")
columns = st.sidebar.columns([1, 4])
with columns[0]:
    st.text(f"{progress(df)*100:.0f}%")
with columns[1]:
    st.progress(progress(df))


def draw_label_counts(counts, options, context):
    context.title("Options")
    total = df[label_column].count()
    values = [counts[option] / total if option in counts else 0 for option in options]
    for option, value in zip(options, values):
        columns = context.columns([1, 4])
        with columns[0]:
            st.text(option)
        with columns[1]:
            st.progress(value)


draw_label_counts(dict(df[label_column].value_counts()), options, st.sidebar)
