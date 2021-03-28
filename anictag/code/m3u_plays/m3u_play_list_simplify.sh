#!/bin/bash
#	(c)2021 Henrique Moreira

# simplify m3u playlists


usage ()
{
 echo "$0 command [command-args ...]

simplify-m3u file [file ...]
"
 exit 0
}


simplify_EXTINF ()
{
 local FILE
 local EXT
 for FILE in $* ; do
	[ "$FILE" = "" ] && continue
	echo "Checking whether playlist is to be simplified: $FILE"
	# e.g. #EXTINF:0,03. Cool.mp3
	#	is converted into:
	#	#EXTINF:0,03. Cool
	EXT=."${FILE##*.}"	# filename="${filename%.*}"
	[ "$EXT" = "." ] && continue
	grep -h ^"#EXTINF" $FILE | grep \.mp3$ > /dev/null
	if [ $? != 0 ]; then
	    echo "Nothing to simplify: $FILE"
	    continue
	fi
	echo "Simplifying EXTINF: $FILE"
	sed -i 's/^#EXTINF:0,\(.*\).mp3$/#EXTINF:0,\1/' $FILE
 done
 return 0
}


simplify_m3u ()
{
 simplify_EXTINF $*
 return $?
}


# Main script

case $1 in
	simplify-m3u) shift; simplify_m3u $* ; exit $?
	;;
	*) usage
	;;
esac

# Exit status
exit $RES
