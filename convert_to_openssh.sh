for file in *.pem; do
    ssh-keygen -i -f "$file" > "open_$file"
done

for file in open_*;do
    name="${file%%.pem}"
    name="${name##open_}"
    sed -i -- "s/==/== $name/g" $file
done
cat open_* > opensshkeys
rm open_*
