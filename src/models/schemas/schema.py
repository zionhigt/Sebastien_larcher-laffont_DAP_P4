from .error import *

class Schema:
    def __init__(self, config=None):
        if config is None:
            raise SchemaEmptyFoundError(config)
        if len(config.keys()) == 0:
            raise SchemaEmptyFoundError(config)
        else:
            self.required_keys = []
            for config_key in config.keys():
                config_field = config[config_key]

                try:
                    config_field['required']

                except KeyError:
                    config_field['required'] = False

                try:
                    config_field['value']

                except KeyError:
                    config_field['value'] = None

                if config_field['required']:
                    self.required_keys.append(config_key)
                    
        self.config = config
        self.loaded = False

    def get_field(self, field_name):

        if self.is_exist_field(field_name):
            return self.config[field_name]
        else:
            raise SchemaNotFoundKeyError(field_name)

    def is_exist_field(self, field_name):
        try:
            if self.config[field_name]:
                return True
        except KeyError:
            return False

    def is_valide_field(self, key):
        field = self.get_field(key)
        if field['required']:
            if field['value'] is not None and field['value'] != "":
                return True
        else:
            return True
        return False
    
    def set_field_value(self, field_name, value):
        if self.is_exist_field(field_name):
            old_field_value = self.config[field_name]['value']
            self.config[field_name]['value'] = value

            if not self.is_valide_field(field_name):
                self.config[field_name]['value'] = old_field_value
        return self.config[field_name]['value']

    def get_schema_input(self):
        return self.config

    def load(self):
        ready_to_load = {}
        config = self.get_schema_input()
        for field in config.keys():
            if self.is_valide_field(field):
                ready_to_load[field] = config[field]['value']
            else:
                return None
        self.__dict__.update(ready_to_load)
        self.loaded = True
        return True



if __name__ == '__main__':

    schema = Schema({
            'name': {
                'required': True,
                'value': None
            }
        })

    print(schema.is_valide_field('name'))
    print(schema.set_field_value('name', "Chester"))
    print(schema.is_valide_field('name'))
    print(schema.set_field_value('name', ""))
    print(schema.is_valide_field('name'))
