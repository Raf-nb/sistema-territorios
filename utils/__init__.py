# utils/__init__.py
"""
Pacote com utilitários diversos para o Sistema de Controle de Territórios.
"""

from utils.date_utils import (
    format_date, get_current_date, get_date_diff_days, add_days,
    get_date_weekday, get_month_start_end, get_current_month_start_end,
    get_month_name, get_last_months, is_valid_date, get_age_from_date,
    get_date_period_description
)

from utils.string_utils import (
    normalize_string, text_to_slug, truncate_string, format_phone_number,
    format_currency, extract_initials, is_valid_email, highlight_search_term,
    split_name, clean_html, pluralize
)

from utils.config_reader import (
    get_config, get_default_config, save_config, get_config_path, ensure_dirs
)

from utils.validation import (
    validate_required, validate_min_length, validate_max_length, validate_email,
    validate_numeric, validate_date, validate_phone, validate_select,
    validate_min_value, validate_max_value, validate_regex, validate_password_strength,
    validate_passwords_match, validate_form, validate_unique, validate_integer,
    validate_float
)

from utils.file_utils import (
    ensure_directory, get_file_extension, get_file_size, format_file_size,
    read_text_file, write_text_file, read_json_file, write_json_file,
    read_csv_file, write_csv_file, list_files, backup_file,
    is_file_older_than, get_file_info, open_file_with_default_app,
    remove_old_files
)

__all__ = [
    # Date utils
    'format_date', 'get_current_date', 'get_date_diff_days', 'add_days',
    'get_date_weekday', 'get_month_start_end', 'get_current_month_start_end',
    'get_month_name', 'get_last_months', 'is_valid_date', 'get_age_from_date',
    'get_date_period_description',
    
    # String utils
    'normalize_string', 'text_to_slug', 'truncate_string', 'format_phone_number',
    'format_currency', 'extract_initials', 'is_valid_email', 'highlight_search_term',
    'split_name', 'clean_html', 'pluralize',
    
    # Config utils
    'get_config', 'get_default_config', 'save_config', 'get_config_path', 'ensure_dirs',
    
    # Validation utils
    'validate_required', 'validate_min_length', 'validate_max_length', 'validate_email',
    'validate_numeric', 'validate_date', 'validate_phone', 'validate_select',
    'validate_min_value', 'validate_max_value', 'validate_regex', 'validate_password_strength',
    'validate_passwords_match', 'validate_form', 'validate_unique', 'validate_integer',
    'validate_float',
    
    # File utils
    'ensure_directory', 'get_file_extension', 'get_file_size', 'format_file_size',
    'read_text_file', 'write_text_file', 'read_json_file', 'write_json_file',
    'read_csv_file', 'write_csv_file', 'list_files', 'backup_file',
    'is_file_older_than', 'get_file_info', 'open_file_with_default_app',
    'remove_old_files'
]