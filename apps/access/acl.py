acl_view_segment_divided = {
    "activity_student": [
        "activity_submit",
        "activity_comment",
        "activity_like",
        "activity_update",
        "activity_rate",
        "student_point"
    ],

    "activity_teacher": [
        "workspace_index",
        "activity_check",
        "activity_confirm"
    ],

    "my_school_student": [
        "my_school_index",
        "league_single_school",
        "activity_report_abuses",
    ],

    "my_school_teacher": [
        "teacher_schools",
        "league_single_school",
    ],

    "league_general": [
        "league_index",
    ],

    "activity_general": [
        "search_activity",
        "specific_activity",
        "specific_student",
        "single_activity",
        "activity_additional_fields",
        "activity_index",
        "activity_rate_users",
        "test_activity",
        "get_sub_form",
    ],

    "announcement_general": [
        "announcements_index",
        "single_announcement"
    ],

    "announcement_teacher": [
        "create_announcement",
        "posted_announcement",
        "update_announcement",
        "delete_announcement"
    ],

    "main_general": [
        "main_index",
        "main_camps",
        "main_cities",
        "main_schools",
    ],

    "notification_general": [
        "notification_index",
    ],

    "calendar": [
        "calendar_index",
        "get_annual_events",
        "remove_occurrence",
        "remove_event",
        "update_occurrence",
        "occurrence",
    ],

    "reports": [
        "date_register_activity_reports",
        "index_report",
        "activity_reports",
        "user_reports",
        "school_reports",
        "get_activity_from_province",
        "average_date_activity_reports",
        "activity_cat_dep",
        "date_done_activity_reports",
        "date_accept_activity_reports"
    ],

    "shop_manager": [
        'product_list_manager',
        'product_index_manager',
        'product_insert_manager',
        'load_sample_form_field',
        'product_delete_manager',
        'banner_manager',
        'sub_category'
    ],

    "shop": [
        'products',
        'shopping_basket',
        'shopping_payment',
        'shopping_final',
        'single_product',
        'test_shop',
        'search_product',
        'shopping_invoice',
        'delete_basket',
        'single_invoice',
    ],

    "advisor": [
        'confirm_question',
    ],

    "expert": [
        'workspace_question',
        'pick_question',
        'answer_question',
        'reject_question',
        'records_question',
        'one_question',
        'comment_manager_question',
        'faq_manager_question',
    ],

    "top_expert": [
        'workspace_question',
        'workspace_faq',
        'workspace_statistics',
        'pick_question',
        'answer_question',
        'reject_question',
        'records_question',
        'one_question',
        'comment_manager_question',
        'faq_manager_question',
        'accept_faq_question',
        'remove_faq_question',
    ],

    "question_manager_general": [
        'question_manager_index',
        'get_question',
        'hamraz_qa_categories',
    ],

    "hamraz_student": [
        "hamraz_faq_index",
        "hamraz_qa_index",
        "hamraz_faq_single",
        "hamraz_qa_single",
        "question_status",
        "hamraz_qa_categories",
        "hamraz_submit",
        "hamraz_conversation_single",
        "question_score",
    ],

    "profile": [
        "user_profile",
        "update_profile_image",
    ],

    "change_role": [
        "change_role_and_gender",
    ],

    "report_abuses": [
        "all_report_abuses",
        "get_report_abuses",
        "change_state_activity"
    ],
    "hamraz_country": [
        "hamraz_faq_index",
        "hamraz_faq_single",
    ]
}

acl_view_segment = dict(
    student=list(
        acl_view_segment_divided["activity_student"] +
        acl_view_segment_divided["hamraz_student"] +
        acl_view_segment_divided["my_school_student"] +
        acl_view_segment_divided["league_general"] +
        acl_view_segment_divided["activity_general"] +
        acl_view_segment_divided["announcement_general"] +
        acl_view_segment_divided["main_general"] +
        acl_view_segment_divided["calendar"] +
        acl_view_segment_divided["shop"] +
        acl_view_segment_divided["profile"] +
        acl_view_segment_divided["notification_general"]
    ),
    coach=list(
        acl_view_segment_divided["activity_general"] +
        acl_view_segment_divided["announcement_general"] +
        acl_view_segment_divided["main_general"] +
        acl_view_segment_divided["notification_general"] +
        acl_view_segment_divided["my_school_teacher"] +
        acl_view_segment_divided["activity_teacher"] +
        acl_view_segment_divided["change_role"] +
        acl_view_segment_divided["profile"] +
        acl_view_segment_divided["league_general"] +
        acl_view_segment_divided["shop"]
    ),
    camp=list(
        acl_view_segment_divided["activity_general"] +
        acl_view_segment_divided["announcement_general"] +
        acl_view_segment_divided["main_general"] +
        acl_view_segment_divided["notification_general"] +
        acl_view_segment_divided["my_school_teacher"] +
        acl_view_segment_divided["activity_teacher"] +
        acl_view_segment_divided["change_role"] +
        acl_view_segment_divided["profile"] +
        acl_view_segment_divided["league_general"] +
        acl_view_segment_divided["shop"]
    ),
    county=list(
        acl_view_segment_divided["activity_general"] +
        acl_view_segment_divided["announcement_general"] +
        acl_view_segment_divided["announcement_teacher"] +
        acl_view_segment_divided["main_general"] +
        acl_view_segment_divided["notification_general"] +
        acl_view_segment_divided["my_school_teacher"] +
        acl_view_segment_divided["activity_teacher"] +
        acl_view_segment_divided["change_role"] +
        acl_view_segment_divided["profile"] +
        acl_view_segment_divided["league_general"] +
        acl_view_segment_divided["shop"]
    ),
    province=list(
        acl_view_segment_divided["activity_general"] +
        acl_view_segment_divided["announcement_general"] +
        acl_view_segment_divided["announcement_teacher"] +
        acl_view_segment_divided["main_general"] +
        acl_view_segment_divided["notification_general"] +
        acl_view_segment_divided["my_school_teacher"] +
        acl_view_segment_divided["activity_teacher"] +
        acl_view_segment_divided["change_role"] +
        acl_view_segment_divided["reports"] +
        acl_view_segment_divided["profile"] +
        acl_view_segment_divided["league_general"] +
        acl_view_segment_divided["shop"]
    ),
    province_m=list(
        acl_view_segment_divided["activity_general"] +
        acl_view_segment_divided["announcement_general"] +
        acl_view_segment_divided["announcement_teacher"] +
        acl_view_segment_divided["main_general"] +
        acl_view_segment_divided["notification_general"] +
        acl_view_segment_divided["my_school_teacher"] +
        acl_view_segment_divided["activity_teacher"] +
        acl_view_segment_divided["change_role"] +
        acl_view_segment_divided["profile"] +
        acl_view_segment_divided["league_general"] +
        acl_view_segment_divided["shop"]
    ),
    province_f=list(
        acl_view_segment_divided["activity_general"] +
        acl_view_segment_divided["announcement_general"] +
        acl_view_segment_divided["announcement_teacher"] +
        acl_view_segment_divided["main_general"] +
        acl_view_segment_divided["notification_general"] +
        acl_view_segment_divided["my_school_teacher"] +
        acl_view_segment_divided["activity_teacher"] +
        acl_view_segment_divided["change_role"] +
        acl_view_segment_divided["profile"] +
        acl_view_segment_divided["league_general"] +
        acl_view_segment_divided["shop"]
    ),

    country=list(
        acl_view_segment_divided["activity_general"] +
        acl_view_segment_divided["announcement_general"] +
        acl_view_segment_divided["announcement_teacher"] +
        acl_view_segment_divided["main_general"] +
        acl_view_segment_divided["notification_general"] +
        acl_view_segment_divided["my_school_teacher"] +
        acl_view_segment_divided["reports"] +
        acl_view_segment_divided["activity_teacher"] +
        acl_view_segment_divided["shop_manager"] +
        acl_view_segment_divided["profile"] +
        acl_view_segment_divided["change_role"] +
        acl_view_segment_divided["report_abuses"] +
        acl_view_segment_divided['hamraz_country'] +
        acl_view_segment_divided["shop"]
    ),

    advisor=list(
        acl_view_segment_divided["advisor"] +
        acl_view_segment_divided["question_manager_general"] +
        acl_view_segment_divided["announcement_general"] +
        acl_view_segment_divided["change_role"] +
        acl_view_segment_divided["notification_general"]

    ),
    expert=list(
        acl_view_segment_divided["expert"] +
        acl_view_segment_divided["question_manager_general"] +
        acl_view_segment_divided["announcement_general"] +
        acl_view_segment_divided["change_role"] +
        acl_view_segment_divided["notification_general"]

    ),
    top_expert=list(
        acl_view_segment_divided["top_expert"] +
        acl_view_segment_divided["question_manager_general"] +
        acl_view_segment_divided["announcement_general"] +
        acl_view_segment_divided["change_role"] +
        acl_view_segment_divided["notification_general"]
    ),
)
