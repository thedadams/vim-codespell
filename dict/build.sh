#!/bin/bash
rm all.list
cat *.list >> all.temp
mv all.temp all.list

aspell --lang=$1 create master ./cs-$1.dict < all.list
