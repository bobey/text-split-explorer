import streamlit as st
from langchain.text_splitter import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter, CharacterTextSplitter, Language


# Streamlit UI
st.title("Text Splitter Playground")
st.info("""Split a text into chunks using a **Text Splitter**. Parameters include:

- `chunk_size`: Max size of the resulting chunks (in either characters or tokens, as selected)
- `chunk_overlap`: Overlap between the resulting chunks (in either characters or tokens, as selected)
- `length_function`: How to measure lengths of chunks, examples are included for either characters or tokens
- The type of the text splitter, this largely controls the separators used to split on
""")
col1, col2, col3, col4 = st.columns([1, 1, 1, 2])

with col1:
    chunk_size = st.number_input(min_value=1, label="Chunk Size", value=1000)

with col2:
    # Setting the max value of chunk_overlap based on chunk_size
    chunk_overlap = st.number_input(
        min_value=1,
        max_value=chunk_size - 1,
        label="Chunk Overlap",
        value=int(chunk_size * 0.2),
    )

    # Display a warning if chunk_overlap is not less than chunk_size
    if chunk_overlap >= chunk_size:
        st.warning("Chunk Overlap should be less than Chunk Length!")

with col3:
    length_function = st.selectbox(
        "Length Function", ["Characters", "Tokens"]
    )

splitter_choices = ["RecursiveCharacter", "Character", "RecursiveCharacter > Markdown"]

with col4:
    splitter_choice = st.selectbox(
        "Select a Text Splitter", splitter_choices
    )

# Box for pasting Markdown
markdown_document = st.text_area("Paste your Markdown document here:")

# Split text button
if st.button("Split Text"):
    headers_to_split_on = [
        ("#", "Header 1"),
        ("##", "Header 2"),
        ("###", "Header 3"),
    ]

    # MD splits
    markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
    md_header_splits = markdown_splitter.split_text(markdown_document)

    if splitter_choice == "Character":
        text_splitter = CharacterTextSplitter(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap
        )

    if splitter_choice == "RecursiveCharacter":
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap
        )

    if splitter_choice == "RecursiveCharacter > Markdown":
        text_splitter = RecursiveCharacterTextSplitter.from_language(
            language=Language.MARKDOWN, chunk_size=chunk_size, chunk_overlap=chunk_overlap
        )

    # Split
    splits = text_splitter.split_documents(md_header_splits)

    # Display the splits
    for idx, split in enumerate(splits, start=1):
        st.text_area(
            f"Split {idx}", split, height=300
        )
