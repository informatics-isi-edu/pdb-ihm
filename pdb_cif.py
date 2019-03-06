import json
import deriva.core.ermrest_model as em

filename = 'json-schema-full-ihm_dev_v1_0_1.json'
#Read JSON data into the datastore variable
with open(filename, 'r') as f:
    pdb = json.load(f)


class Table():
    def __init__(self, name, dict):

        def maptype(t):
            m = {'string', 'text'}

        print(name)
        self.name = name
        assert(dict['type'] == 'array' or dict['type'] == 'object')

        if dict['type'] == 'array':
            assert (dict['items']['type'] == 'object')
            columns = dict['items']['properties']
        else:
            columns = dict['properties']

        self.columns = [
            {
            'nullok': k not in v['required'],
            'comment': v['description'],
            'type': maptype(v['type']),
            'name': k
        }
            for k,v in columns.items()]
        self.keys = ['id'] if 'id' in v else []
        self.fkeys = [ k.replace('_id','') for k in columns.keys() if '_id' in k]
        # Need to check for enum....


tables = { k:Table(k,v) for k,v in pdb['properties'].items() if k != '_entry_id'}