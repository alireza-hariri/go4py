package main

import "C"

import (
	"crypto/md5"
	"encoding/hex"
	"io"

	"os"

	"github.com/alireza-hariri/go4py/examples/benchmarks/internal/buffer_util"
	"github.com/alireza-hariri/go4py/go_pkg/go4py"
)

const (
	chunkSize = 2 * 1024 * 1024 // 2MB
)

// pre allocate a pool of buffers for lower memory allocation overhead (and also lower GC time)
var bufferPool = buffer_util.NewBufferPool(16, chunkSize)

//export File_md5
func File_md5(filePath string) *C.char {

	file, err := os.Open(filePath)
	if err != nil {
		return nil
	}
	defer file.Close()

	buffer, id := bufferPool.GetBuffer()
	defer bufferPool.ReleaseBuffer(id)

	// we simply assume that the file size is less than chunkSize
	bytesRead, err := file.Read(buffer)
	if err != nil {
		return nil
	}

	hasher := md5.New()
	hasher.Write(buffer[:bytesRead])
	return C.CString(hex.EncodeToString(hasher.Sum(nil)))
}

// parallelized with go-routines
//
//export File_list_md5
func File_list_md5(filePaths []string) []*C.char {
	// make a go-routine for each file
	type ResultItem = struct {
		idx int
		md5 *C.char
	}
	ch := make(chan ResultItem, len(filePaths))
	for idx, filePath := range filePaths {
		go func(filePath string, idx int) {
			ch <- ResultItem{idx, File_md5(filePath)}
		}(filePath, idx)
	}
	// collect results
	md5s := go4py.MakeSlice[*C.char](len(filePaths))
	for range len(filePaths) {
		res := <-ch
		md5s[res.idx] = res.md5
	}
	return md5s
}

//export File_md5_method2
func File_md5_method2(filePath string) *C.char {
	file, err := os.Open(filePath)
	if err != nil {
		return nil
	}
	defer file.Close()
	hasher := md5.New()
	_, err = io.Copy(hasher, file)
	if err != nil {
		return nil
	}
	return C.CString(hex.EncodeToString(hasher.Sum(nil)))
}

//export File_md5_method3
func File_md5_method3(filePath string) *C.char {
	buffer, err := os.ReadFile(filePath)
	if err != nil {
		return nil
	}
	hasher := md5.New()
	hasher.Write(buffer)
	return C.CString(hex.EncodeToString(hasher.Sum(nil)))
}

// same as method2 but with no-gil annotation
// [go4py] no-gil
//
//export File_md5_method4
func File_md5_method4(filePath string) *C.char {
	return File_md5_method2(filePath)
}
