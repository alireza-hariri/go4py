package main

import (
	"fmt"
	"go/ast"
	"go/doc"
	"go/parser"
	"go/token"
)

// GetFoo comments I can find easely
// line2
func GetFoo() {
    // Comment I would like to access
    test := 1
    fmt.Println(test)
}

func main() {
    fset := token.NewFileSet() // positions are relative to fset
    d, err := parser.ParseDir(fset, "./lib", nil, parser.ParseComments)
    if err != nil {
        fmt.Println(err)
        return
    }
    for k, pkg := range d {
        fmt.Println("package", k)
        for n, file := range pkg.Files {
            fmt.Printf("File name: %q\n", n)
            for _, decl := range file.Decls {
                fn, ok := decl.(*ast.FuncDecl)
                if !ok {
                    continue // Not a function declaration
                }
                fmt.Printf("Function name: %s\n", fn.Name.Name)
                if fn.Name.Name == "main" {
                    continue
                }
                // inputs
                for _, param := range fn.Type.Params.List {
                    fmt.Println("params",param.Names,param.Type)
                }
                // outputs
                for _, param := range fn.Type.Results.List {
                    fmt.Println("results",param.Names,param.Type)
                }
            }

        }

        p := doc.New(pkg, "./", doc.AllDecls)
        for _, f := range p.Funcs {
            fmt.Println("type", f.Name)
            fmt.Println("docs:", f.Doc)
        }
    }
}