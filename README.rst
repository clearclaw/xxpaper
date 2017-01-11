xxpaper
=======

Installation dependency:

	     PsFile: http://www.seehuhn.de/pages/psfile

Unfortunately PsFile is not available via setuptools and the cheese
factory.

Otherwise:

	     pip install xppaper

Should do the job.

XXPaper generates Postscript files representing charters, privates,
shares, station markers, trains and (linear) stock markets (2D stock
markets coming later) as defined by a configuration passed on the
command line.  All art is made using a format which is friendly to
die-cutting.  Default component sizes for shares, privates and
trains fit the ~$20 test die provided with Ellison Prestige Pro die
cutters.  Cut-lines are provided in the "outline" files for hand
cutting.  Alignment lines are provided for all files that allow
accurate die placement when using a die cutter.

The resulting Postscript files can be converted to PDFs using the
`ps2pdf` utility that comes with Ghostscript.

Sample configuration files can be found in the "samples" directory
of the source tree.  The README there lists the various sample files,
their complexity and purpose (some are much more involved than 
others).  The files produced by those sample files can be seen at:

	     http://kanga.nu/~claw/xxpaper/example
       
-- JCL

P.S. PsFile appears to have fallen off the 'net.  A copy may be
found here:

     https://github.com/clearclaw/psfile
