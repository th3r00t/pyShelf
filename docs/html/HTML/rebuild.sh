#!/bin/sh
#
# rebuild.sh: rebuild hypertext with the previous context.
#
# Usage:
#	% sh rebuild.sh
#
cd /home/raelon/Projects/pyShelf/src/backend && GTAGSCONF=':langmap=c\:.c.h,yacc\:.y,asm\:.s.S,java\:.java,cpp\:.c++.cc.hh.cpp.cxx.hxx.hpp.C.H,php\:.php.php3.phtml:skip=HTML/,HTML.pub/,tags,TAGS,ID,y.tab.c,y.tab.h,gtags.files,cscope.files,cscope.out,cscope.po.out,cscope.in.out,SCCS/,RCS/,CVS/,CVSROOT/,{arch}/,autom4te.cache/,*.orig,*.rej,*.bak,*~,#*#,*.swp,*.tmp,*_flymake.*,*_flymake,*.o,*.a,*.so,*.lo,*.zip,*.gz,*.bz2,*.xz,*.lzh,*.Z,*.tgz,*.min.js,*min.css:' htags -g -s -a -n -v -w -t 'pyShelf Open Source Ebook Server-0.3.0' /home/raelon/Projects/pyShelf/docs/html
