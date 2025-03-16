from pydantic import BaseModel


class DocAnnots(BaseModel):
    msgpack_bytes: bool = False
    no_gil: bool = False


def make_doc_annots(doc: str) -> DocAnnots:
    doc_annots = DocAnnots()
    for line in doc.splitlines():
        if "[go4py]" in line:
            args = line.replace("[go4py]", "").strip().split()
            for arg in args:
                if arg == "msgpack-bytes":
                    doc_annots.msgpack_bytes = True
                elif arg == "no-gil":
                    doc_annots.no_gil = True
    return doc_annots


def test_make_doc_annots():
    doc = "[go4py]   msgpack-bytes\n"
    doc_annots = make_doc_annots(doc)
    assert doc_annots.msgpack_bytes


if __name__ == "__main__":
    test_make_doc_annots()
    print("All tests passed.")

"""
uv run -m go4py.doc_annotation
"""
