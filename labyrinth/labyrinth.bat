mkdir labyrinth
cd labyrinth
mkdir ParentFolder
cd ParentFolder
mkdir ChildFolder
mklink /J Junction1 %~dp0labyrinth\ParentFolder
cd ChildFolder
mklink /J Junction2 %~dp0labyrinth\ParentFolder
echo "" > Minotaur.txt