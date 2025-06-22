from go4py.get_go_functions import extract_functions_from_dot_h
import io

dot_h_file = """
extern struct Map_test2_return Map_test2();
extern void Slice_inp_test(GoSlice nums);
extern void* Http_test(GoString url);
extern void SomeFunc(GoSlice nums);
extern void SomeFunc2(GoSlice nums);"""


def test_fn_names():
    fn_names = extract_functions_from_dot_h(io.StringIO(dot_h_file))

    assert fn_names == {'Map_test2','Slice_inp_test','SomeFunc','SomeFunc2','Http_test'}
