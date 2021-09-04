from chessmanager.models.schemas.error import SchemaNotFoundKeyError
from chessmanager.models.schemas.error import SchemaEmptyFoundError

from tinydb import TinyDB, where
from datetime import datetime
from datetime import date
from os import path


class Schema:
    def __init__(self, config=None, table="_default", query_model=None):
        
        if config is not None:
            if len(config.keys()) == 0:
                raise SchemaEmptyFoundError(config)
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

                try:
                    config_field['default']

                except KeyError:
                    config_field['default'] = None

                try:
                    config_field['type']

                except KeyError:
                    config_field['type'] = str

                if config_field['required']:
                    self.required_keys.append(config_key)

        self.config = config
        self.is_already_loaded = False
        self.load()
        # timestamp = str(datetime.now().timestamp()).split('.')[0]
        timestamp = "1630676601"
        db_folder = './data/database/'
        db_file_name = f"chess_db_{timestamp}.json"
        self.DB = TinyDB(path.join(db_folder, db_file_name))
        self.table = self.DB.table(table)
        self.query_model = query_model

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

    @staticmethod
    def is_valide_field_type(field):
        if field['type'] is date:
            try:
                date.fromisoformat(field['value'])
                return True

            except ValueError:
                return False

        else:
            try:
                field['type'](field['value'])
                return True

            except ValueError:
                return False

    def is_valide_field(self, key):
        field = self.get_field(key)
        if field['value'] is not None and field['value'] != "":
            if self.is_valide_field_type(field):
                return True

        else:
            if not field['required']:
                return True

        return False

    def set_field_value(self, field_name, value):
        if self.is_exist_field(field_name):
            old_field_value = self.config[field_name]['value']
            if self.config[field_name]['type'] is not date:
                self.config[field_name]['value'] = self.config[field_name]['type'](value)
            else:
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
            if self.is_already_loaded:
                if not self.is_valide_field(field):
                    return None
            ready_to_load[field] = config[field]
        self.__dict__.update(ready_to_load)
        self.is_already_loaded = True
        return True

    def to_dict(self):
        _dict = {}
        excluded_attr = [
            'required_keys',
            'config',
            'is_already_loaded',
            'query_model',
            'table',
            'DB'
            ]
        for attr in self.__dict__:
            if attr not in excluded_attr:
                attribute = self.__dict__[attr]
                if attr in self.config.keys():
                    attribute = self.__dict__[attr]['value']
                _dict[attr] = attribute
        return _dict

    def get_db_model_id(self):
        model = self.to_dict
        tiny_model = self.table.get(self.query_model())
        if tiny_model is not None:
            return tiny_model.doc_id
        else:
            return False
        

    def serialize(self):
        is_model_in_db = self.get_db_model_id()
        model = self.to_dict()
        if is_model_in_db is False:
            # insertables_players.append(player)
            # insert model in table
            self.table.insert(model)
        else:
            # model_query = lambda x=None: ((where('last_name') == player['last_name']) &
            # (where('first_name') == player['first_name']) &
            # (where('birth_date') == player['birth_date']))
            self.table.update(model, self.query_model())

if __name__ == '__main__':

    schema = Schema({
            'name': {
                'required': True,
                'value': None
            }
        })

    print(schema.is_valide_field('name'))
    print(schema.set_field_value('name', "chessmanager"))
    print(schema.is_valide_field('name'))
    print(schema.set_field_value('name', ""))
    print(schema.is_valide_field('name'))
