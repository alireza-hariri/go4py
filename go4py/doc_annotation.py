from pydantic import BaseModel


class DocAnnots(BaseModel):
    msgpack_decode: bool = False
    no_gil: bool = False
    skip_binding: bool = False


def make_doc_annots(doc: str) -> DocAnnots:
    doc_annots = DocAnnots()
    for line in doc.splitlines():
        if "[go4py]" in line:
            args = line.replace("[go4py]", "").strip().split()
            for arg in args:
                if arg in "decode-msgpack":
                    doc_annots.msgpack_decode = True
                elif arg == "no-gil":
                    doc_annots.no_gil = True
                elif arg == "skip-binding":
                    doc_annots.skip_binding = True
                else:
                    raise ValueError(f"Unknown go4py annotation: {arg}")
    return doc_annots


def test_make_doc_annots():
    doc = "[go4py]   decode-msgpack\n"
    doc_annots = make_doc_annots(doc)
    assert doc_annots.msgpack_decode


if __name__ == "__main__":
    test_make_doc_annots()
    print("All tests passed.")

"""
uv run -m go4py.doc_annotation
"""
