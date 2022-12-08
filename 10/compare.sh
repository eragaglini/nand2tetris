python3 JackCompiler/JackAnalyzer.py $1 -xml

for i in *.xml; do
    [ -f "$i" ] || break
    TextComparer.sh $1/$i $i
done

rm *.xml