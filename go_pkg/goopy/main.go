package goopy

/*
#include "goopy.h"

*/
import "C"

func CError(err error) C.Error {
	if err == nil {
		return nil
	}
	return C.CString(err.Error())
}
