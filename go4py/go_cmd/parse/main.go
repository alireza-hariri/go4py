package main

import (
	"encoding/json"
	"fmt"
	"go/ast"
	"go/doc"
	"go/parser"
	"go/token"
	"os"
)

type VarType struct {
	GoType string `json:"go_type"`
}

type Variable struct {
	Name string  `json:"name"`
	Type VarType `json:"type"`
}

type GoFunction struct {
	Package    string     `json:"package"`
	Name       string     `json:"name"`
	Docs       string     `json:"docs"`
	Arguments  []Variable `json:"arguments"`
	ReturnType []VarType  `json:"return_type"`
}


var DEBUG = false

func Errorf(format string, args ...interface{}) {
	fmt.Fprintf(os.Stderr, "ERROR: "+format+"\n", args...)
}

func Debugf(format string, args ...interface{}) {
	if DEBUG {
		fmt.Printf("DEBUG: "+format+"\n", args...)
	}
}

func readNodeText(content string, fset *token.FileSet, n ast.Node) (string, error) {
	s := fset.Position((n).Pos()).Offset
	e := fset.Position((n).End()).Offset
	if s < 0 || e < 0 || s > e || e > int(len(content)) {
		return "", fmt.Errorf("invalid offset")
	}
	return content[s:e], nil
}

// getFileContent returns the content of a given file.
func getFileContent(n string) (string, error) {
	data, err := os.ReadFile(n)
	if err != nil {
		Errorf("Error reading file: %v", err)
		return "", err
	}
	return string(data), nil
}

func main() {
	// Create a slice to store GoFunction objects
	var functions []GoFunction

	fset := token.NewFileSet() // positions are relative to fset
	dirPath := "./lib"
	if len(os.Args) > 1 {
		dirPath = os.Args[1]
	}
	if len(os.Args) > 2 && os.Args[2] == "--debug" {
		DEBUG = true
	}
	d, err := parser.ParseDir(fset, dirPath, nil, parser.ParseComments)
	if err != nil {
		Errorf("%v", err)
		return
	}
	for k, pkg := range d {
		Debugf("package %s", k)
		for n, file := range pkg.Files {
			Debugf("File name: %q", n)
			// Get the file's content
			fileContent, err := getFileContent(n)
			if err != nil {
				Errorf("%v", err)
				continue
			}

			for _, decl := range file.Decls {
				fn, ok := decl.(*ast.FuncDecl)
				if ok {
					Debugf("Function name: %s", fn.Name.Name)

					// if its exported function
					if fn.Name.IsExported() {
						// Create a new GoFunction object
						goFunc := GoFunction{
							Package:    k,
							Name:       fn.Name.Name,
							Arguments:  []Variable{}, // Initialize empty
							ReturnType: []VarType{},  // Initialize empty
						}

						// inputs
						for _, param := range fn.Type.Params.List {
							t, err := readNodeText(fileContent, fset, param.Type)
							if err != nil {
								Errorf("%v", err)
								continue
							}
							Debugf("params %v %s", param.Names, t) //, param.Type)

							// Add arguments to the GoFunction
							for _, name := range param.Names {
								goFunc.Arguments = append(goFunc.Arguments, Variable{
									Name: name.Name,
									Type: VarType{
										GoType: t,
									},
								})
							}
						}
						// outputs
						if fn.Type.Results != nil {
							for _, param := range fn.Type.Results.List {
								// read file from pos to end of param.Type
								t, err := readNodeText(fileContent, fset, param.Type)
								if err != nil {
									Errorf("%v", err)
									continue
								}

								Debugf("result %s", t) //, param.Type)
								// Append to return types
								goFunc.ReturnType = append(goFunc.ReturnType, VarType{GoType: t})

								// // if its sclice
								// if slice, ok := param.Type.(*ast.ArrayType); ok {
								// 	t2, _ := readNodeText(fileContent, fset, slice.Elt)
								// 	Debugf("slice-type: %s", t2)
								// 	goFunc.ReturnType = &VarType{GoType: t2}
								// }
								// // if its map
								// if mapType, ok := param.Type.(*ast.MapType); ok {
								// 	t2, _ := readNodeText(fileContent, fset, mapType.Key)
								// 	t3, _ := readNodeText(fileContent, fset, mapType.Value)
								// 	fmt.Println("map-type", t2, t3)
								// }
							}
						}

						// Add the function to our list
						functions = append(functions, goFunc)
					}
				}
				decl, ok := decl.(*ast.GenDecl)
				if ok {
					for _, spec := range decl.Specs {
						typeSpec, ok := spec.(*ast.TypeSpec)
						if ok {
							structType, ok := typeSpec.Type.(*ast.StructType)

							if ok {
								Debugf("struct: %s", typeSpec.Name.Name)
								for _, field := range structType.Fields.List {
									Debugf("field: %s", field.Names[0].Name)
								}
								// Newline for readability in logs
							}
						}
					}
				}
			}
		}
		p := doc.New(pkg, "./", doc.AllDecls)
		for _, f := range p.Funcs {
			if f.Doc != "" {
				Debugf("%s docs: %s", f.Name, f.Doc)

				// Update the documentation for the corresponding function in our list
				for i := range functions {
					if functions[i].Name == f.Name && functions[i].Package == k {
						functions[i].Docs = f.Doc
						break
					}
				}
			}
		}
	}

	// Marshal the functions slice to JSON
	jsonData, err := json.MarshalIndent(functions, "", "  ")
	if err != nil {
		Errorf("Error marshaling to JSON: %v", err)
		return
	}

	// Save the JSON to a file
	err = os.WriteFile("artifacts/functions.json", jsonData, 0644)
	if err != nil {
		Errorf("Error writing JSON to file: %v", err)
		return
	}

	Debugf("Successfully saved %d functions to functions.json", len(functions))
}
