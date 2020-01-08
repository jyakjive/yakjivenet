from newscommunity.ncvars import *
from newscommunity.application import APPLICATION
from util.fileutils import *

# declarations

# definitions

# classes

class FormMailerMaker:

    def __init__(self, filename):
        self.filename = filename

        self.template = readTextFile(FILENAME_CONTACT_TEMPLATE_SOURCE)

    def write(self, contactEmail):

        if (contactEmail is None):
            raise 'ContactEmail cannot be None in FormMailerMaker'

        data = self.template.replace('${contactEmail}', contactEmail)

        writeTextFile(self.filename, data)