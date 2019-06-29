def announcements_schema():
    return {
        'title': {
            'type': 'string',
            'required': True,
            'empty': False
        },
        'description': {
            'type': 'string',
            'required': True,
            'empty': False
        },
        'receivers': {
            'type': 'list',
            'required': True,
            'empty': False
        },
        # 'date': {
        #     'type': 'string',
        # },
        # 'temp_has_date': {
        #     'type': 'string',
        #     'dependencies': 'date'
        # },
    }


def update_announcements_schema():
    return {
        'title': {
            'type': 'string',
            'required': True,
            'empty': False
        },
        'description': {
            'type': 'string',
            'required': True,
            'empty': False
        }
    }
