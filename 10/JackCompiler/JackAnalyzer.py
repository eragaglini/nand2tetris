#!/usr/bin/env python3
import sys
import os
import CompilationEngine
#import JackCompilationEngineXML

def main():
	if len(sys.argv) < 2:
		print("Error. Missing argument: input (dir./file)")
		return -1

	if not os.path.exists(sys.argv[1]):
		print("Error:", sys.argv[1], "does not exist.")
		return -1

	xml_output = False
    # se passiamo l'opzione -xml al programma allora facciamo generare il file xml intermedio
	if len(sys.argv) > 2 and sys.argv[2] == '-xml':
		xml_output = True

	if os.path.isdir(sys.argv[1]):
		input_path = sys.argv[1]
		print("Input path:", input_path)
		compileFiles(input_path, xml_output)
	else:
		input_file = sys.argv[1]
		compileFile(input_file, xml_output)

def compileFile(input_path, xml_output=False):
    #JackCompilationEngineXML.JackCompilationEngineXML(input_path, replaceExtension(input_path, ".xml"))
    # in teoria ci sono due versioni del Compilation Engine, una per generare un file xml intermedio e un'altra
    # per la gestione del file xml intermedio
    if xml_output:
        print(input_path, "- Generating XML", "...")
        CompilationEngine.CompilationEngine(input_path, replaceExtension(input_path, ".xml"))
    else:
        print(input_path, "- Compiling", "...")
        #JackCompilationEngine.JackCompilationEngine(input_path, replaceExtension(input_path, ".vm"))

def compileFiles(directory, xml_output):
	''' Get all files in directory that are not .XMLs and compile them. '''
	for f in os.listdir(directory):
		if f.find('jack') != -1:
			compileFile(directory + f, xml_output)

def replaceExtension(input_name, extension):
	return input_name.replace(".jack", extension)

if __name__ == '__main__':
	main()