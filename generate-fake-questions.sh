#!/bin/bash

testdir="test1"
for i in {1..200}; do
	testsubdir="${testdir}/fake-question-${i}"
	for i in "$testsubdir/answers/"{0,1}; do
		if ! [ -e "$i" ]; then
			mkdir -p "$i" || exit 1
		fi
	done
	cat $(find /usr/share/doc -type f -name README | shuf | head -n 1) /dev/null | tr -d '_*\n=<>-' | sed -r -e 's,[ \t]+, ,g' | cut -b 1-$[RANDOM % 200 + 20] > "${testsubdir}/question"
	for j in {1..4}; do
		cat $(find /usr/share/doc -type f -name README | shuf | head -n 1) /dev/null | sed -r -e "s,(.{$[RANDOM % 20 + 5]}),\1 ,g" | tr -d '_*\n=<>-' | sed -r -e 's,[ \t]+, ,g' | cut -b 1-$[RANDOM % 100 + 10] > "${testsubdir}/answers/0/${j}"
	done
	cat $(find /usr/share/doc -type f -name README | shuf | head -n 1) /dev/null | sed -r -e "s,(.{$[RANDOM % 20 + 5]}),\1 ,g" | tr -d '_*\n=<>-' | sed -r -e 's,[ \t]+, ,g' | cut -b 1-$[RANDOM % 100 + 15] > "${testsubdir}/answers/1/0"
done
