# imports

HTTP_PROTOCOL = 'http://'

SITE_NAMES_MINIMUM_LENGTH = 3

SITE_NAMES_FORBIDDEN = [
    'testsite', 'admin', 'messages', 'rss', 'xml', 'html', 'python', 'perl', 'cgi', 'w3c', 'www',
    'images', 'styles', 'wysiwygpro', 'java', 'exe', 'bin', 'usr', 'cmd', 'command',
    'rss2', 'rss3', 'css', 'supportfiles',
    'andrews', 'chrisandrews', 'cjandrews', 'chris_andrews', 'chris-andrews', 'christopherandrews',
    'fight-the-right', 'fighttheright', 'fight-the-right-org', 'fight-the-right-com', 'jeromes', 'TheJeromes',
    'faerycats', 'therio']
SITE_NAMES_FORBIDDEN_PREFIXES = ['scripts', 'upload', 'yakjive', 'cgi-bin', 'restrict']
SITE_NAMES_RESERVED = []
SITE_NAMES_RESERVED_PREFIXES = ['milo', 'jeanette', 'jezebel']

GLOBAL_DEBUG = True

MULTIPLE_SITES_ALLOWED = [
    'chris.j.andrews@gmail.com',
    'cjandrews@usa.net',
    'jherbert94965@yahoo.com',
    'jeanettecandrews@gmail.com',
    'benjamincandrews@gmail.com',
    'dherbert60@gmail.com',
    'ebelaski@comcast.net',
    'noah@thebenedicts.net',
    'noah.benedict@idea.com'
    ]

GLOBAL_DEBUG = True
INTERNAL_REFERER = 'yj-referer'

FILENAME_SITE_PROPERTIES = 'data/site_properties.xml'
FILENAME_PAGE_TEMPLATE = 'data/page_templates/template-page.html'
FILENAME_EMAIL_PROBLEM = 'data/email_templates/email_error.txt'

DEFAULT_REDIRECT = HTTP_PROTOCOL + 'www.yakjive.com/index.html'

ROOT_SITE_URL = HTTP_PROTOCOL + 'www.yakjive.com/'
ROOT_SITE_MESSAGES_URL = ROOT_SITE_URL + 'messages/'

ROOT_SITE_ADMIN_URL = HTTP_PROTOCOL + 'www.yakjive.net/cgi-bin/'

# Use this for sites created under the yj account
CUSTOM_SITE_ADMIN_URL = HTTP_PROTOCOL + 'www.yakjive.com/cgi-bin/yj/'

STATUS_GOOD = 'good'
STATUS_INACTIVE = 'inactive'
STATUS_TERMINATED = 'terminated'

INVITE_CODES = ['YJBETA']

ALPHANUM_CHARS = ' abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ01234567890-_'

EMAIL_INCLUDE_DIR = 'data/email_templates/'
FILENAME_EMAIL_WELCOME = 'email_welcome.txt'
FILENAME_EMAIL_ERROR = 'email_error.txt'
FILENAME_EMAIL_INVITE = 'email_yj_invite.txt'

EMAIL_PROBLEM = 'problem@yakjive.com'
EMAIL_INFO = 'chris@yakjive.com'

CREATE_ROOT_URL = 'www.yakjive.com'
CREATE_DEFAULT_LOCATION = '../../cgi-bin/yj/'
CREATE_WEBSITE_LOCATION = '../../'

CREATE_REPLACE_FILES = [
    CREATE_DEFAULT_LOCATION + '${domain}/data/app_properties.xml',
    CREATE_DEFAULT_LOCATION + '${domain}/data/page_properties.xml',
    CREATE_DEFAULT_LOCATION + '${domain}/data/rss2_properties.xml',
    CREATE_DEFAULT_LOCATION + '${domain}/data/section_properties.xml',
    CREATE_DEFAULT_LOCATION + '${domain}/data/user_properties.xml',
    CREATE_DEFAULT_LOCATION + '${domain}/data/user_roles.xml',
    CREATE_DEFAULT_LOCATION + '${domain}/data/newsItems/template-blog-data.xml',
    CREATE_WEBSITE_LOCATION + '${domain}/admin/index.html']

#CREATE_COPY_FILES = { \
#    CREATE_DEFAULT_LOCATION + '${domain}/data/newsItems/template-blog-data.xml':
#    CREATE_DEFAULT_LOCATION + '${domain}/data/newsItems/${webmasterTemplate}-blog-data.xml'}

CREATE_COPY_FILES = {}

SITE_TIME_FORMAT = '%Y-%m-%d'