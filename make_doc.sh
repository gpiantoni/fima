rm docs -fr
pdoc3 fima -o doc --html
mv doc/fima docs
rmdir doc
git add docs

