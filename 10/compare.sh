for i in *.xml; do
    [ -f "$i" ] || break
    TextComparer.sh $1/$i $i
done
