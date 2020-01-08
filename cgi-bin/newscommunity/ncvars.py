#Imports
import util.properties

#Declarations

FILENAME_SECTIONS = 'data/section_properties.xml'
FILENAME_STYLES = 'style_properties.xml'
FILENAME_INFO_PAGES = 'data/info_page_properties.xml'
FILENAME_PAGES = 'data/page_properties.xml'
FILENAME_USERS = 'data/user_properties.xml'
FILENAME_USER_ROLES = 'data/user_roles.xml'
FILENAME_APPLICATION = 'data/app_properties.xml'
FILENAME_NEWSLETTER = 'data/newsletter_list.xml'
FILENAME_USERTEMPLATE = 'data/page_includes/user_template.html'
FILENAME_CONTACT_TEMPLATE_SOURCE = 'data/page_includes/contact_template.txt'
FILENAME_CONTACT_TEMPLATE = 'supportfiles/contact_template.txt'
FILENAME_EMAIL_ERROR = 'data/page_includes/email_error.txt'
FILENAME_EMAIL_INVITE = 'data/page_includes/email_invite.txt'
FILENAME_EMAIL_CONTACT = 'data/page_includes/email_contact.txt'
FILENAME_LAYOUT_TEMPLATE = 'data/page_includes/layout_wizard_template.html'
FILENAME_POPUP_TEMPLATE = 'data/page_includes/popup_template.html'
FILENAME_RSS = 'data/rss2_properties.xml'

TRUE = [1, True, 'True', '1', 'TRUE', 'true', 'T', 'YES', 'yes', 'Yes']

ALPHANUM_CHARS = ' abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ01234567890-_'

GLOBAL_DEBUG = True

PAGE_LONG_ARTICLES = 'satire'
PAGE_LETTERS = 'letters'
PAGE_HEADLINES = 'articles'
PAGE_PHOTOS = 'photos'
PAGE_GUESTBOOK = 'guestbook'
PAGE_BLOG = 'blog'
PAGE_LINKS = 'links'
PAGE_CALENDAR = 'calendar'

PAGE_TYPES = {PAGE_LONG_ARTICLES:'Long articles', PAGE_LETTERS:'Letters', PAGE_HEADLINES:'Articles',
    PAGE_GUESTBOOK:'Guestbook', PAGE_BLOG:'Blog', PAGE_LINKS:'Links'}
    #PAGE_PHOTOS:'Photos', PAGE_CALENDAR:'Calendar'}

# These styles will allow a user to customize the look and feel of different types of articles
PAGE_TYPE_STYLES = {PAGE_LONG_ARTICLES:'longArticle', PAGE_LETTERS:'letterArticle', PAGE_HEADLINES:'basicArticle',
    PAGE_GUESTBOOK:'guestbookArticle', PAGE_BLOG:'blogArticle', PAGE_LINKS:'linkArticle'}
    #PAGE_PHOTOS:'Photos', PAGE_CALENDAR:'Calendar'}

HEADLINE_ONLY = 'headlineonly'
HEADLINE_BRIEF = 'brief'
HEADLINE_VERBOSE = 'verbose'
HEADLINE_FULL = 'full'

HEADLINE_TYPES = {
    HEADLINE_ONLY:'Headline only',
    HEADLINE_BRIEF:'Short text',
    HEADLINE_VERBOSE:'Long text',
    HEADLINE_FULL:'Full text'}
PAGE_EXPIRES = {'Never':'Never', 7:'7 days', 30:'30 days', 90:'90 days', 365:'1 year'}

#Number of days old a blogs comments can be before you can no longer comment on the blog
BLOG_COMMENTS_OLD = 14

SITE_TYPE_BASIC = 'Basic'
SITE_TYPE_EXPANDED = 'Expanded'
SITE_TYPE_PREMIUM = 'Premium'
SITE_TYPE_SIZE = {
    SITE_TYPE_BASIC : 30000000,
    SITE_TYPE_EXPANDED : 100000000,
    SITE_TYPE_PREMIUM :  500000000}

FILE_SIZE_MAX = 3000000 # 3M
FILE_SIZE_BASIC = 250000 # 500K

FILE_TYPES_ALLOWED = [
    'jpg',
    'gif',
    'png',
    'csv',
    'txt',
    'xml',
    'jpeg',
    'doc',
    'pdf']

SORT_DATE = 'date: newest first'
SORT_ALPHABETIC = 'alphabetic'
SORT_ALPHABETIC_REVERSE = 'reverse alphabetic'
SORT_RATING = 'rating'
SORT_DATE_REVERSE = 'date: oldest first'
SORT_DATE_LM = 'date: last modified first'
SORT_DATE_REVERSE_LM = 'date: first modified first'
SORT_LIST_NEWSPAGE = [SORT_DATE, SORT_DATE_REVERSE, SORT_ALPHABETIC]
SORT_LIST_ALL = [SORT_DATE, SORT_DATE_REVERSE, SORT_DATE_LM, SORT_DATE_REVERSE_LM, SORT_ALPHABETIC, SORT_ALPHABETIC_REVERSE]

ITEMS_PER_PAGE = 20

SEARCH_TEMPLATE = 'search-template.html'
INFO_PAGE_TEMPLATE = 'info-page-template.html'
SINGLE_COLUMN_TEMPLATE = '1-col-template.html'
DOUBLE_COLUMN_TEMPLATE = '2-col-template.html'
TRIPLE_COLUMN_TEMPLATE = '3-col-template.html'

THUMBNAIL_SIZE = {
    60: 'Small',
    100: 'Medium',
    150: 'Large'}

NC_GUEST = 'NC_GUEST'
NC_ADMIN = 'NC_ADMIN'

INFO_PAGE_CONTACT = 'contact'
INFO_PAGE_CONTACT_THANKS = 'contactThanks'
INFO_PAGE_SEARCH = 'search'
INFO_PAGE_ABOUT = 'about'
INFO_PAGE_LEGAL = 'legal'