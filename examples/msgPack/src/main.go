package main
import "C"
import (
  	"github.com/vmihailenco/msgpack/v5"
    "github.com/alireza-hariri/go4py/go_pkg/go4py"
)

// [go4py] decode-msgpack
//export Example_fn1
func Example_fn1() ([]byte, *C.char) {
	some_map := map[string]string{"hello": "world", "example-key": "example-val"}
	b, err := msgpack.Marshal(some_map)
	if err != nil{
		return nil, C.CString(err.Error())
	}
  	return go4py.CopySlice(b), nil
}

// [go4py] decode-msgpack
//export Example_fn2
func Example_fn2() ([]byte, *C.char) {
	type Item struct {
        Foo string
    }
    b, err := msgpack.Marshal(&Item{Foo: "bar"})
	if err != nil{
		return nil, C.CString(err.Error())
	}
  	return go4py.CopySlice(b), nil}

func main() {}
