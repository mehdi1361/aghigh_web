def activity_create_schema():
    return {
        'title': {
            'type': 'string',
            'required': True,
            'empty': False
        },
        'location': {
            'type': 'string',
            'required': True,
            'empty': False
        },
        # 'start_date': {
        #     'type': 'datetime_str',
        #     'required': True,
        #     'empty': False
        # },
        # 'end_date': {
        #     'type': 'datetime_str',
        #     'required': True,
        #     'empty': False
        # },
        'description': {
            'type': 'string',
            'required': True,
            'empty': False
        },
        'category': {
            'type': 'string',
            'required': True,
            'empty': False
        }
    }


def activity_report_schema():
    return {
        'content': {
            'type': 'string'
        },
        'activity': {
            'type': 'string',
            'required': True,
            'empty': False
        },
        'category': {
            'type': 'string',
            'required': True,
            'empty': False
        }
    }
