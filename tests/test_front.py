import pathlib
import pytest

pytest.importorskip("playwright")


def test_index_title(page):
    index = pathlib.Path(__file__).resolve().parents[1] / "static" / "index.html"
    page.goto(index.as_uri())
    assert page.title() == "Planificateur Sportif Intégré"
