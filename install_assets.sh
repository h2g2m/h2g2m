TDIR=/tmp/h2g2tmp
mkdir $TDIR

# Bootstrap 3.3.4
wget -P $TDIR https://github.com/twbs/bootstrap/releases/download/v3.3.4/bootstrap-3.3.4-dist.zip
unzip $TDIR/bootstrap-3.3.4-dist.zip -d $TDIR
cp $TDIR/bootstrap-3.3.4-dist/css/bootstrap.css ./h2g2m/static/css/bootstrap.css
cp $TDIR/bootstrap-3.3.4-dist/js/bootstrap.js ./h2g2m/static/js/bootstrap.js

# Glyphicons
if [ ! -d ./h2g2m/static/fonts ]; then 
 mkdir ./h2g2m/static/fonts
fi
file_extensions=(eot svg ttf woff woff2)
for file_extension in ${file_extensions[@]}; do
  cp $TDIR/bootstrap-3.3.4-dist/fonts/glyphicons-halflings-regular.$file_extension ./h2g2m/static/fonts/glyphicons-halflings-regular.$file_extension
done

# jQuery 1.11.2
wget -P ./h2g2m/static/js/ https://code.jquery.com/jquery-1.11.2.js

# jQuery storage api 1.7.3
wget -P ./h2g2m/static/js/ https://raw.githubusercontent.com/julien-maurel/jQuery-Storage-API/abef0586cf92e29297a283ee6299bac741ae125e/jquery.storageapi.js

# jQuery tpye ahead 0.11.1
wget -P ./h2g2m/static/js/ https://raw.githubusercontent.com/twitter/typeahead.js/588440f66559714280628a4f9799f0c4eb880a4a/dist/bloodhound.js
wget -P ./h2g2m/static/js/ https://raw.githubusercontent.com/twitter/typeahead.js/588440f66559714280628a4f9799f0c4eb880a4a/dist/typeahead.jquery.js

# MathJax 2.1
wget -P $TDIR https://github.com/mathjax/MathJax/archive/v2.1-latest.zip
unzip $TDIR/v2.1-latest.zip -d $TDIR
mv $TDIR/MathJax-2.1-latest ./h2g2m/static/mathjax

echo cleaning up temporary files in $TDIR
rm -r $TDIR 


