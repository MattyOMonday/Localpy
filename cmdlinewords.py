# -*- coding: utf-8 -*-
"""
Created on Wed Apr 01 23:41:32 2015

@author: Matty
"""

#prints when a non existent file is run, %(file name)
file_not_found = "No podia encontrar el archivo: %s"
#prints when a command isn't found, %(command name)
cmd_not_found = "No podia encontrar el mandato: %s"
#prints when you try to cd into an empty directory, %(dir name)
empty_dir = "el directorio %s esta vacio"
#prints when the command line is exited
bye_msg = "Gracias para usar Piton. Adios."
#prints when a syntax error occurs, %(line number)
syntax_error = "un error de syntax habia occurido en linea %i"
#prints when any other type of error occurs %(error type, line number)
error_msg = "un error de %s habia occurido en linea %i"

#prints with every input
in_phrase = "En"
#prints with every output
out_phrase ="Sal"

#the command used for help
help_cmd = "ayuda"

#the command used to run a file
run_cmd = "corre"

#the command used to exit the command line
bye = "sal"

#the command to list all files in the directory
ls = "ls"
#the sub command to only list [special type] files
ls_sub1 = "-p"
#special type file:
special_extension = ".pi"

#the command to change directory
cd = "cd"
#the sub command to go up one directory level
cd_sub1 = "-s"

#the command to print current directory
cwd = "dta"

#the command to print a list of commands
cmds = "mandatos"

#the command to list all translated packages
trans = "traducidos"

#prints upon start of command line
start_msg = \
"""
Piton 0.0.1 -- Python en espanol
Desarrollado por Matthew Westphall
Escrito en Python 2.7, un producto de Guido van Rossum

Mandatos utiles:
corre <<nombre>> -> correr un archivo
ayuda <<otro mandato>>-> una descripcion detallada de <<otro mandato>>
mandatos -> una lista de los mandatos
sal -> salir de la programa
"""

#list of translated packages (add to this):
translatedPackages = ["time"]


#help definitions. Print when "help <<command name>> is called"
#the text displayed for "help help"
help_help = \
"""
formato: ayuda <<otro mandato>>
se usa para recibir mas informacion sobre <<otro mandato>>
esta en la forma de: mandato (sub-mandato) <<otra informacion>>
"""

#the text displayed for "help run"
run_help = \
"""
formato: corre <<nombre de archivo>>
se usa para correr un archivo
ej: si tienes un archivo que se llama <<ejemplo.pi>>,
<<corre ejemplo.pi>> va a correr el archivo <<ejemplo.pi>>
"""

#the text displayed for "help bye"
bye_help = \
"""
formato: sal
Sale de Piton
"""

#the text displayed for "help ls"
ls_help = \
"""
formato: ls (-p)
imprima los archivos en el directorio actual
sub-mandatos:\n" +
-p: imprima solo los archivos del tipo .pi
ej: si el directorio actual tiene los archivos <<ejemplo.pi>> y <<texto.txt>>
<<ls>> va a imprimir <<ejemplo.pi , texto.txt>>
y <<ls -p>> va a imprimir <<ejemplo.pi>>
"""

cd_help = \
"""
formato: cd (-s) <<nombre de directorio>>
se usa para cambiar directorio
sub-mandatos:
-s: Sube al directorio un nivel mas alto del directorio actual
ej: si el directorio actual es C:\\Usuarios\\Piton\\Proyectos,
<<cd Escuela>> lo cambiara a C:\\Usuarios\\Piton\\Proyectos\\Escuela
<<cd -s>> lo cambiara a C:\\Usuarios\\Piton
y <<cd \\Usuarios>> lo cambiara a C:\\Usuarios
"""

cwd_help = \
"""
formato: dta
imprima el directorio en que trabaja actualmente
ej: si su directorio actual es C:\\Usuarios\\Piton\\Proyectos,
<<dta>> va a imprimir <<C:\\Usuarios\\Piton\\Proyectos>
"""

cmds_help = \
"""
formato: mandatos
imprima una lista de todos los mandatos
"""

trans_help = \
"""
formato: traducidos
imprima una lista de todos los paquetes de Python que son traducidos actualmente
el lista va a crecer con tiempo
"""


#IMPORTANT: Only change lines below here if you're adding new commands

all_cmds =[help_cmd,run_cmd,bye,ls,cd,cwd,cmds,trans]
all_cmds.sort()

help_dict = \
{
help_cmd:help_help,
run_cmd:run_help,
bye:bye_help,
ls:ls_help,
cd:cd_help,
cwd:cwd_help,
cmds:cmds_help,
trans:trans_help
}
