def extract_data_items(data, selected_fields, fields_dict, is_to_dict=False, is_to_string=False):
    items = data.get('items', [])
    extracted_items = []

    for item in items:
        if is_to_dict:
            row = {}
        else:
            row = []
        for field in selected_fields:
            field_path = fields_dict.get(field)
            if field_path:
                value = item
                keys = field_path.split('.')
                if keys[0] == 'items':
                    keys = keys[1:]
                for key in keys:
                    value = value.get(key, "")
                if is_to_string:
                    value = str(value)
                if is_to_dict:
                    row[field] = value
                else:
                    row.append(value)
        extracted_items.append(row)
    return extracted_items
