
import json

class Schema(object):
    
    def __init__(self):
        self.fields = []

    def __repr__(self):
        fields_transposed = self.transpose_fields()
        max_lens = [f.max_value_length() for f in self.fields] 
        s = ""
        for row in fields_transposed:
            values_and_lengths = zip(row, max_lens)
            s = s + '|'.join('{0:{width}}'.format(x, width=y) for x, y in values_and_lengths) + "\n"
        return s

    def merge_schema(self, other):
        nameless_field_values = set()
        for other_field in other.fields:
            if other_field == "":
                for x in other_field.values:
                    nameless_field_values.add(x)
        for self_field in self.fields:
            if self_field == "":
                for x in self_field.values:
                    nameless_field_values.add(x)
            for other_field in other.fields:
                if self_field.name != "" and self_field.name == other_field.name:
                    self_field.values = list(set(self_field.values + other_field.values))

    def transpose_fields(self):
        if len(self.fields) == 0:
            return []
        rows = {}
        max_num_values = max([len(f.values) for f in self.fields])
        for f in self.fields:
            while len(f.values) < max_num_values:
                f.values.append("")
            i = 0
            for v in [f.name] + f.values:
                if not i in rows:
                    rows[i] = []
                rows[i].append(v)
                i += 1
        rows = sorted(rows.iteritems(), key=lambda x: x[0])
        return [x[1] for x in rows]

    class SchemaEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, Schema):
                return obj.jsonify()
            return json.JSONEncoder.default(self, obj)

    def dumps(self, **kwargs):
        return json.dumps(self, cls=self.SchemaEncoder, **kwargs)
        
    def jsonify(self):
        encoding = {}
        encoding["fields"] = [f.jsonify() for f in fields]
        return encoding

    @staticmethod
    def from_dict(d):
        s = Schema()
        s.fields = [Field.from_dict(f) for f in d["fields"]]
        return s

class Field(object):
    
    def __init__(self, name):
        self.name = name
        self.values = []

    def max_value_length(self):
        return max([len(str(v)) for v in [self.name] + self.values])

    def jsonify(self):
        encoding = {}
        encoding["name"] = name
        encoding["values"] = values
        return encoding

    @staticmethod
    def from_dict(d):
        f = Field(d["name"])
        f.values = d["values"]
        return f
