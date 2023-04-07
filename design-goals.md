# `censusdis` design goals

There are other existing Python packages to call the U.S.
Census API. And it is also possible to manually construct
URLs to the API and parse the JSON that comes back. But we
felt we could do better. We wanted to create an API that
did all the heavy lifting transparently and let users 
concentrate on the research questions they were trying to
answer. Finding and downloading the data you want and 
plotting your results on a map should be quick and easy,
using just a few lines of easy to read code.

More specifically, our goals were:

1. The API should be pythonic. In particular, it should not
   embed logic in strings like "state:34" or similar. It is
   much preferred to have a keyword argument like
   `state="34"`,  or, where possible `state=STATE_NJ`.
2. There should be little or no hardcoded metadata. This 
   should be true of census data sets, groups, variable, and
   geographies. These tend to change in small ways that
   are difficult to keep track of and up to date. For example,
   different groups and variables are available in different
   data sets, and their IDs can change from year to year.
   Different data sets support different geographic level
   data aggregations. If a python package hard-codes these
   then it is a never ending battle to keep them up to date.
   Instead, metadata should be queried at run time whenever
   possible.
3. Mapping should be a first class concern. Often the most
   compelling presentations of census data or data derived
   from it are in the form of maps. It should be easy and
   obvious how to add geographic geometry to data. For
   example, adding a `with_geometry=True` argument to a query
   should get you not just the census data you want but
   also the geometry of the geographic regions in a format
   that is easy to plot. On a related note, the package
   should provide a nice utility to plot the United States
   with Alaska and Hawaii moved to the lower left corner
   of the continental United States so as to produce more
   compact maps.
4. The implementation should be fast enough to be used
   interactively. It should be possible
   to download nationwide data at the block group level
   (approximately 240,000 rows) in under a minute with
   typical high-speed internet. Most manipulation and
   mapping operations on data at that scale should be 
   doable in seconds.

Although we are always looking to make further improvements,
we hope that as you explore the API and the sample code
and begin to use `censisdis` yourself, you will agree that 
we have achieved these goals.
