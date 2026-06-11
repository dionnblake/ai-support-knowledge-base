import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock, mock_open
from app.services.document_loader import load_pdf, load_docx, load_txt, load_document

@patch("app.services.document_loader.PdfReader")
def test_load_pdf(mock_pdf_reader):
    # Mocking the PdfReader
    fake_reader = MagicMock()
    fake_page = MagicMock()
    fake_page.extract_text.return_value = "Page text content"
    fake_reader.pages = [fake_page]
    mock_pdf_reader.return_value = fake_reader

    file_path = Path("mock_doc.pdf")
    docs = load_pdf(file_path)

    assert len(docs) == 1
    assert docs[0].page_content == "Page text content"
    assert docs[0].metadata["source"] == "mock_doc.pdf"
    assert docs[0].metadata["page"] == 0

@patch("app.services.document_loader.docx.Document")
def test_load_docx(mock_docx_document):
    # Mocking docx Document
    fake_doc = MagicMock()
    fake_para = MagicMock()
    fake_para.text = "Word paragraph text"
    fake_doc.paragraphs = [fake_para]
    mock_docx_document.return_value = fake_doc

    file_path = Path("mock_doc.docx")
    docs = load_docx(file_path)

    assert len(docs) == 1
    assert docs[0].page_content == "Word paragraph text"
    assert docs[0].metadata["source"] == "mock_doc.docx"
    assert docs[0].metadata["page"] == 0

def test_load_txt():
    # Mock standard open
    mock_file_content = "Plain text file content"
    with patch("builtins.open", mock_open(read_data=mock_file_content)):
        file_path = Path("mock_doc.txt")
        docs = load_txt(file_path)

        assert len(docs) == 1
        assert docs[0].page_content == "Plain text file content"
        assert docs[0].metadata["source"] == "mock_doc.txt"
        assert docs[0].metadata["page"] == 0

@patch("app.services.document_loader.load_pdf")
@patch("app.services.document_loader.load_docx")
@patch("app.services.document_loader.load_txt")
def test_load_document_dispatcher(mock_txt, mock_docx, mock_pdf):
    # Test dispatching
    load_document(Path("doc.pdf"))
    mock_pdf.assert_called_once_with(Path("doc.pdf"))

    load_document(Path("doc.docx"))
    mock_docx.assert_called_once_with(Path("doc.docx"))

    load_document(Path("doc.txt"))
    mock_txt.assert_called_once_with(Path("doc.txt"))
