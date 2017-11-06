import splparser
import json

query = "search *"
parsetree = splparser.parse(query)
parsetree_as_json = parsetree.jsonify()
print json.dumps(parsetree_as_json, sort_keys=True, indent=2, separators=(',', ': '))
