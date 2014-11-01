Overview
========

splparser is a Python parser for `Splunk Processing Language <http://docs.splunk.com/Documentation/Splunk/6.2.0/SearchReference/ListOfSearchCommands>`_ queries.

It does not parse all commands in the language but it can parse the sixty or so most commonly used commands.

The parser is not tied to a particular version of the language and may break for some versions.

Please `submit an issue <https://github.com/salspaugh/splparser/issues>`_ if you run into any problems.

Use `this link <mailto:saraalspaugh@gmail.com>`_ to send feedback.

Supported commands
==================

The SPL commands currently capable of being parsed are:

* abstract
* addinfo
* addtotals
* append
* appendcols
* audit
* bucket
* chart
* collect
* convert
* dedup
* delete
* delta
* eval
* eventstats
* export
* extractkv
* fieldformat
* fields
* filldown
* fillnull
* gauge
* head
* history
* inputcsv
* inputlookup
* join
* loadjob
* localop
* lookup
* makemv
* metadata
* multikv
* mvcombine
* mvexpand
* nomv
* outlier
* outputcsv
* outputlookup
* overlap
* rare
* regex
* relevancy
* rename
* replace
* reverse
* rex
* search
* sort
* spath
* stats
* strcat
* streamstats
* table
* tags
* tail
* timechart
* top
* transaction
* transpose
* tstats
* typeahead
* uniq
* where
* xmlkv
* xpath
