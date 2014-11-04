Using the parser
================

To parse a query, use the ``parse`` function in the splparser module. For example::

    python -c "import splparser; splparser.parse('search sourcetype=access_* method=GET').print_tree()"

The ``parse`` function returns a tree-based representation of the query that can be used to pull out its constituent parts.

The script ``splparser.sh`` is included as a convenience so that you can parse queries from the command line, mostly for testing purposes.
To use this, run ``source splparser.sh`` (and consider putting that in your login script).
You can then run, for example::

    splparse 'search sourcetype=access_* method=GET'

Note that when parsing queries from the command line, there are occasionally issues with how some characters are interpreted by the shell.

