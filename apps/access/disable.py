

disable_acl_map = {
    'activity': [
        "activity_index",
    ],
    'activity_show': [
        'single_activity',
    ],
    'activity_create': [
        'activity_create',
        'activity_submit',
    ],
    'activity_add': [
        'activity_create',
        'activity_submit',
    ],
    'activity_star': [
        "activity_rate",
        # 'activity_star'
    ],
    'activity_comment': [
        'activity_comment',
    ],
    'activity_search': [
        "search_activity",
    ],
    'activity_rate_users': [
        "activity_rate_users",
    ],
    'activity_check': [
        "activity_check",
        "workspace_index",
    ],
    'activity_update': [
        "activity_update",
    ],

    'question': [
        'hamraz_faq_index',
        'hamraz_qa_index',
    ],
    'question_create': [
        'hamraz_submit',
    ],
    'question_answer': [
        'answer_question',
    ],
    'question_search': [
        'question_search'
    ],
    'question_score': [
        'question_score',
    ],

    'shop': [
        'products',
    ],
    'shop_buy': [
        'shopping_basket',
    ],
    'shop_search': [
        'search_product',
    ],


    'schedule': [
        'calendar_index',
    ],
    'schedule_add': [
        'occurrence',
        'update_occurrence',
    ],
    'schedule_del': [
        'remove_event',
        'remove_occurrence',
    ],

    'league': [
        'league_index',
    ],

    'league_single': [
        'league_single_school',
    ],

    'report': [
        'index_report',
        'date_register_activity_reports',
        'activity_reports',
        'date_done_activity_reports',
        'date_accept_activity_reports',
        'get_activity_from_province',
        'average_date_activity_reports',
        'activity_cat_dep',
        'user_reports',
        'school_reports',
    ],

    'announcement': [
        'announcements_index',
        'announcement',
    ],
    'announcement_read': [
        'single_announcement',
    ],

    'notification': [
        'notification_index',
        'notification',
    ],
}