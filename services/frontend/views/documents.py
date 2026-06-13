import streamlit as st
from datetime import datetime

from ui.css_styling import load_documents_styles
from ui.render_functions import render_section_header, render_list_item
from services.frontend_actions import upload_documents
from services.backend_client import BackendClient

PAGE_KEY = "documents"
PAGE_NAME = "Dokumente"
PAGE_PATH = "/views/documents.py"
PAGE_ICON = "📄"

# Hauptfunktion, die die Seite rendert
def render_documents():

    init_session_state()

    load_documents_styles()

    with st.container(key="documents_page_container"):
        render_documents_header()

        with st.container(key="documents_content_container"):
            render_documents_upload()
            render_documents_list()


def init_session_state():

    if "open_document_name" not in st.session_state:
        st.session_state.open_document_name = None

    if "documents_uploader_version" not in st.session_state:
        st.session_state.documents_uploader_version = 0

    if "documents_upload_success" not in st.session_state:
        st.session_state.documents_upload_success = None

    if "documents_sort_by" not in st.session_state:
        st.session_state.documents_sort_by = "modified_at"

    if "documents_sort_ascending" not in st.session_state:
        st.session_state.documents_sort_ascending = False


# Rendert den Dokumenten-Header mit den Sortierbuttons
def render_documents_header():

    header = st.container(key="documents_header_container")

    with header:

        title_col, name_col, date_col = st.columns([6, 1.5, 1.5])

        with title_col:
            st.subheader("Dokumentenverwaltung")

        with name_col:
            sort_name_clicked = st.button(
                "Name ↕",
                key="documents_sort_name",
                use_container_width=True
            )

            if sort_name_clicked:
                update_document_sort(sort_by="name", default_ascending=True)

        with date_col:
            sort_date_clicked = st.button(
                "Datum ↕",
                key="documents_sort_date",
                use_container_width=True
            )

            if sort_date_clicked:
                update_document_sort(sort_by="modified_at", default_ascending=False)


# Rendert den Dokumentenupload Bereich im Ganzen
def render_documents_upload():

    render_section_header("Dokumentenupload")

    with st.container(key="documents_upload_container"):

        if st.session_state.documents_upload_success:
            st.toast(st.session_state.documents_upload_success)
            st.session_state.documents_upload_success = None

        uploaded_files = st.file_uploader(
            "Dokumente auswählen",
            type=["pdf", "txt", "docx"],
            accept_multiple_files=True,
            label_visibility="collapsed",
            key=f"documents_file_uploader_{st.session_state.documents_uploader_version}"
        )

        # Falls eine Datei im Upload-Bereich liegt, wird die if Anweisung ausgeführt
        if uploaded_files:
            st.caption(f"{len(uploaded_files)} Dokument(e) ausgewählt")
        else:
            st.caption("Dokumente auswählen oder hierher ziehen")

        # Button zum Upload der Dokumente. Dieser ist nur klickbar, wenn mindestens eine Datei im Uploader liegt.
        upload_clicked = st.button(
            "Dokumente hochladen",
            type="primary",
            use_container_width=True,
            key="documents_upload_button",
            disabled=not uploaded_files
        )

        # Logik für die Ausführung des Uploads von Dokumenten.
        if upload_clicked:
            result = upload_documents(uploaded_files)

            if result is not None:
                st.session_state.documents_upload_success = (
                    f"{len(uploaded_files)} Dokumente wurden erfolgreich hochgeladen.")
                st.session_state.documents_uploader_version += 1
                st.rerun()


# Rendert die Dokumentenliste in ihrer übergeordneten Struktur
def render_documents_list():

    render_section_header("Gespeicherte Dokumente")

    backend_client = BackendClient()

    try:
        documents = backend_client.get_documents()

    except Exception as error:
        st.error(f"Dokumente konnten nicht geladen werden: {error}")
        return

    if not documents:
        st.info("Keine Dokumente vorhanden.")
        return

    documents = sort_documents(documents)

    for document in documents:
        render_document_item(document, backend_client)


# Rendert einen einzelnen Listeneintrag für ein Dokument
def render_document_item(document, backend_client):

    file_name = document["name"]
    modified_at = format_modified_at(document["modified_at"])

    is_open = (st.session_state.open_document_name == file_name)

    item_label = f"{modified_at}  |  {file_name}"

    is_pdf = file_name.lower().endswith(".pdf")

    document_url = (
        backend_client.get_document_url(file_name)
        if is_pdf
        else None
    )

    toggle_clicked, _ = render_list_item(
        item_label=item_label,
        item_key=f"document_{file_name}",
        action_label="Öffnen",
        action_url=document_url,
        action_disabled=not is_pdf
    )

    if toggle_clicked:
        toggle_document(file_name)

    if is_open:
        render_document_preview(document)


# Rendert die Vorschau der Metadaten eines Dokuments, falls der Button geklickt wird
def render_document_preview(document):

    file_name = document["name"]
    file_size = format_file_size(document["size"])
    modified_at = format_modified_at(document["modified_at"])

    file_extension = file_name.rsplit(".", 1)[-1].upper()

    with st.container(key=f"document_preview_container_{file_name}"):

        st.markdown("**Dokumentinformationen**")
        st.write(f"Dateiname: {file_name}")
        st.write(f"Dateityp: {file_extension}")
        st.write(f"Dateigröße: {file_size}")
        st.write(f"Zuletzt geändert: {modified_at}")


# -----HILFSFUNKTIONEN-----

# Dokumentensortierung aufsteigend/absteigend nach Name/Datum (sort_by)
def update_document_sort(sort_by, default_ascending):

    if st.session_state.documents_sort_by == sort_by:
        st.session_state.documents_sort_ascending = (
            not st.session_state.documents_sort_ascending
        )
    else:
        st.session_state.documents_sort_by = sort_by
        st.session_state.documents_sort_ascending = default_ascending


def sort_documents(documents):

    sort_by = st.session_state.documents_sort_by
    ascending = st.session_state.documents_sort_ascending

    if sort_by == "name":
        return sorted(
            documents,
            key=lambda document: document["name"].casefold(),
            reverse=not ascending
        )

    if sort_by == "modified_at":
        return sorted(
            documents,
            key=lambda document: document["modified_at"],
            reverse=not ascending
        )

    return documents


# Steuert das Öffnen (else) bzw. Schließen (if) der Metadaten eines Items
def toggle_document(file_name):

    if st.session_state.open_document_name == file_name:
        st.session_state.open_document_name = None
    else:
        st.session_state.open_document_name = file_name

    st.rerun()


def format_file_size(size_in_bytes):

    if size_in_bytes >= 1024 * 1024:
        return f"{size_in_bytes / (1024 * 1024):.1f} MB"

    return f"{size_in_bytes / 1024:.1f} KB"


def format_modified_at(timestamp):

    return datetime.fromtimestamp(timestamp).strftime("%d.%m.%Y")
