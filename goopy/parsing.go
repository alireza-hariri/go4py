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

type TypeAlias = string

type Variable struct {
	Name string
	Type TypeAlias
}

type GoFunction struct {
	Package    string
	Name       string
	Arguments  []Variable
	ReturnType TypeAlias
	Docs       string
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
		return "", err
	}
	return string(data), nil
}

func main() {
	// Create a slice to store GoFunction objects
	var functions []GoFunction

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
			// Get the file's content
			fileContent, err := getFileContent(n)
			if err != nil {
				fmt.Println(err)
				continue
			}

			for _, decl := range file.Decls {
				fn, ok := decl.(*ast.FuncDecl)
				if ok {
					fmt.Printf("Function name: %s\n", fn.Name.Name)

					// if its exported function
					if fn.Name.IsExported() {
						// Create a new GoFunction object
						goFunc := GoFunction{
							Package: k,
							Name:    fn.Name.Name,
						}

						// inputs
						for _, param := range fn.Type.Params.List {
							t, err := readNodeText(fileContent, fset, param.Type)
							if err != nil {
								fmt.Println(err)
								continue
							}
							fmt.Println("params", param.Names, t) //, param.Type)

							// Add arguments to the GoFunction
							for _, name := range param.Names {
								goFunc.Arguments = append(goFunc.Arguments, Variable{
									Name: name.Name,
									Type: t,
								})
							}
						}
						// outputs
						if fn.Type.Results != nil {
							for _, param := range fn.Type.Results.List {
								// read file from pos to end of param.Type
								t, err := readNodeText(fileContent, fset, param.Type)
								if err != nil {
									fmt.Println(err)
									continue
								}

								fmt.Println("result", t) //, param.Type)
								// Set return type
								goFunc.ReturnType = t

								// // if its sclice
								if slice, ok := param.Type.(*ast.ArrayType); ok {
									t2, _ := readNodeText(fileContent, fset, slice.Elt)
									fmt.Println("slice-type:", t2)
									goFunc.ReturnType = "[]" + t2
								}
								// // if its map
								// if mapType, ok := param.Type.(*ast.MapType); ok {
								// 	t2, _ := readNodeText(fileContent, fset, mapType.Key)
								// 	t3, _ := readNodeText(fileContent, fset, mapType.Value)
								// 	fmt.Println("map-type", t2, t3)
								// }
							}
						}
						print("\n")

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
								fmt.Println("struct:", typeSpec.Name.Name)
								for _, field := range structType.Fields.List {
									fmt.Println("field:", field.Names[0].Name)
								}
								fmt.Print("\n")
							}
						}
					}
				}
			}
		}
		p := doc.New(pkg, "./", doc.AllDecls)
		for _, f := range p.Funcs {
			if f.Doc != "" {
				fmt.Print(f.Name, " docs:", f.Doc)

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
		fmt.Println("Error marshaling to JSON:", err)
		return
	}

	// Save the JSON to a file
	err = os.WriteFile("functions.json", jsonData, 0644)
	if err != nil {
		fmt.Println("Error writing JSON to file:", err)
		return
	}

	fmt.Println("Successfully saved", len(functions), "functions to functions.json")
}
