# imports

import os
from newscommunity.ncvars import *
from newscommunity.application import *
from classes.newspage_handler import *
from util.user_management import *
from classes.section_handler import *
from classes.newspage_utils import *
from ui.mvc import *
import cgi

from util.fileutils import log

# declarations

OP_NEW_ARTICLE = 'article'
OP_EDIT_ARTICLE = 'edit_article'
OP_NEW_NEWSPAGE = 'newspage'
OP_NEW_SECTION = 'section'
OP_NEW_SECTION_LAYOUT = 'section'
OP_NEW_USER = 'addUser'

OP_MANAGE = 'manage'
OP_HIDE_WIZARDS = 'hideWizards'

OP_DEFAULT_PAGE = 'show_default_page'
OP_DEFAULT_PAGE_WIZ = 'show_default_page_wizard'
OP_DEFAULT_PAGE_CON = 'show_default_page_console'

OP_PAGE = 'page_'
OP_PAGE_BACK = 'page_back'
OP_PAGE_BACK_FULL = 'page_back_full'
OP_PAGE_FORWARD = 'page_forward'
OP_PAGE_FORWARD_FULL = 'page_forward_full'
OP_PAGE_CHANGED = 'page_changed'

OP_LAYOUT = 'layout_'
OP_LAYOUT_INIT = 'layout_init'
OP_LAYOUT_SAVE_NEWSPAGE = 'layout_save'
OP_LAYOUT_DONE = 'layout_done'
OP_LAYOUT_ADD_SECTION = 'layout_add_section'
OP_LAYOUT_MANAGE_SECTIONS = 'layout_manage_sections'

URL_LAYOUT_GOOD_SAVE = 'layout_good_save.py'

# classes

class WizardModel(Model):
    def __init__(self, form):
        Model.__init__(self, form)
        # Order is important!
        self.businessObjects = [
            WizardStartBO,
            WizardNewSectionBO,
            WizardNewNewspageBO,
            WizardNewArticleBO,
            WizardNewUserBO,
            LayoutInitBO,
            LayoutDeleteNewspageBO,
            LayoutSaveNewspageBO,
            LayoutSaveSectionBO,
            LayoutCheckRoutingBO,
            WizardShowDefaultPageBO]

    def getRouter(self, form = None):
        return WizardRouter(form, self)

    def validate(self):
        #raise str(repr(self.__dict__))
        check = 'operation' in self.__dict__

        #log('In MVC_WIZARD Model.Validate with query string: ' + self.toQueryString())

        if (check):
            if (OP_PAGE in self.operation):
                check = check and (('newspage' in self.__dict__) or ('page' in self.__dict__))
                check = check and ('pageItemCount' in self.__dict__)
                if (check):
                    self.pageItemCount = int(pageItemCount)
                check = check and ('pageCurrent' in self.__dict__)
                if (check):
                    self.pageCurrent = int(pageCurrent)
                check = check and ('pageSortTypeCurrent' in self.__dict__)
                check = check and ('pageSortTypeNew' in self.__dict__)
            elif ((self.operation in [OP_NEW_ARTICLE, OP_NEW_SECTION, OP_NEW_NEWSPAGE]) or
                    (OP_LAYOUT in self.operation)):

                check = True
                if (OP_LAYOUT not in self.operation):
                    check = check and ('step' in self.__dict__)

                if (check):
                    if (self.operation in [OP_NEW_ARTICLE, OP_EDIT_ARTICLE]):
                        self.newspage = list()
                    elif ((self.operation == OP_NEW_SECTION) and (int(self.step) in [2, 3, 4])):
                        check = check and (('section_longname' in self.__dict__) and
                            ('section_columns' in self.__dict__))

                        self.section_name = ''
                        for c in self.section_longname.lower():
                            if c in ALPHANUM_CHARS:
                                if c == ' ':
                                    self.section_name += '-'
                                else:
                                    self.section_name += c
                        self.section_name += '-headlines'

                        if ('section_locked' not in self.__dict__):
                            self.section_locked = False
                        if ('section_isVisible' not in self.__dict__):
                            self.section_isVisible = False
                        if (not check):
                            self.errorMessage = 'Could not validate Section information'
                    elif (((self.operation == OP_NEW_NEWSPAGE) and (int(self.step) in [2, 3, 4])) or
                            (self.operation in [OP_LAYOUT_SAVE_NEWSPAGE]) or
                            (('doSave' in self.__dict__) and (self.doSave in TRUE))):

                        #log('In MVC_WIZARD with: ' + self.toQueryString().replace('&', '&\r\n'))

                        checkFields = True

                        if (OP_LAYOUT in self.operation):
                            if ('doSave' in self.__dict__):
                                self.doSave = (self.doSave in TRUE)
                            else:
                                self.__dict__['doSave'] = False
                            checkFields = self.doSave

                            # Don't check the fields if the save is just of
                            # deleted items or the layout only
                            checkFields = checkFields and ('newspage_name' in self.__dict__)

                        if (checkFields):
                            # Add the newspage attribute to make sure we can use the article wizard properly
                            self.newspage = list()
                            check = check and (
                                ('newspage_title' in self.__dict__) and
                                ('newspage_pageType' in self.__dict__) and
                                ('newspage_headlineType' in self.__dict__) and
                                ('newspage_section' in self.__dict__) and
                                ((OP_LAYOUT in self.operation) or ('newspage_column' in self.__dict__)) and
                                ('newspage_displayNum' in self.__dict__) and
                                ('newspage_expires' in self.__dict__) and
                                ('newspage_sortType' in self.__dict__) and
                                ((OP_LAYOUT in self.operation) or ('newspage_rank' in self.__dict__)))

                            if (check):

                                # This happens when the newspage has been deleted
                                if ('newspage_name' not in self.__dict__):
                                    self.newspage_name = ''

                                if (('newspage_name' in self.__dict__) and
                                        (self.newspage_name == '')):
                                    for c in self.newspage_title.lower():
                                        if c in ALPHANUM_CHARS:
                                            if c == ' ':
                                                self.newspage_name += '-'
                                            else:
                                                self.newspage_name += c

                                if ('newspage_subTitle' not in self.__dict__):
                                    self.newspage_subTitle = ''
                                if ('newspage_promptComments' not in self.__dict__):
                                    self.newspage_promptComments = ''
                                if ('newspage_isVisible' not in self.__dict__):
                                    self.newspage_isVisible = False
                                else:
                                    self.newspage_isVisible = (self.newspage_isVisible in TRUE)
                                if ('newspage_allowComments' not in self.__dict__):
                                    self.newspage_allowComments = False
                                else:
                                    self.newspage_allowComments = (self.newspage_allowComments in TRUE)
                                if ('newspage_locked' not in self.__dict__):
                                    self.newspage_locked = False
                                else:
                                    self.newspage_locked = (self.newspage_locked in TRUE)
                            else:
                                self.errorMessage = 'Could not validate Newspage information<br>\r\n' + \
                                    self.toQueryString().replace('&', '&amp;<br>\r\n')
                                #log('Model error: ' + self.errorMessage)

            elif (self.operation == OP_NEW_USER):
                check = 'step' in self.__dict__
                if (check):
                    if (int(self.step) > 1):
                        # TODO: check for the user attributes
                        pass

            if (check and (OP_LAYOUT in self.operation)):
                if (self.operation != OP_LAYOUT_INIT):
                    check = check and ('layoutCurrentSection' in self.__dict__)
                    check = check and ('layoutStartSection' in self.__dict__)
                    #check = check and ('newspage_name' in self.__dict__)
                    if (self.operation == OP_LAYOUT_MANAGE_SECTIONS):
                        self.__dict__['route'] = 'layout'
                    elif (self.operation == OP_LAYOUT_ADD_SECTION):
                        self.__dict__['step'] = 1
                        self.__dict__['route'] = 'layout'
                else:
                    if ('layoutStartSection' not in self.__dict__):
                        self.layoutStartSection = ''

                if ('layoutStartNewspage' not in self.__dict__):
                    self.layoutStartNewspage = ''

        #log('Leaving WizardModel.validate() check = ' + str(check))
        return check

class WizardRouter(FormRouter):
    def validate(self):
        check = FormRouter.validate(self)
        check = check and (self.model.operation != '')
        if (not check):
            self.model.errorMessage = 'Incorrect state to route page.'
        return check

    def getRoute(self):

        #log('In MVC_WIZARD router with ' + self.model.toQueryString().replace('&', '&\r\n'))

        redir = APPLICATION.redirectOnFailedLogin
        if (self.validate()):
            if (self.model.operation == OP_NEW_ARTICLE):
                if (int(self.model.step) == 1):
                    redir = APPLICATION.adminURL + 'articleWizard1.py'
                elif (int(self.model.step) == 2):
                    redir = APPLICATION.adminURL + 'add_news.py'
            elif (self.model.operation == OP_EDIT_ARTICLE):
                if (int(self.model.step) == 1):
                    # goto 'choose article OR newspage' page
                    redir = APPLICATION.adminURL + 'editArticleWizard1.py'
                elif (int(self.model.step) == 2):
                    # goto 'choose article FROM newspage' page
                    redir = APPLICATION.adminURL + 'edit_news.py'
                elif (int(self.model.step) == 3):
                    redir = APPLICATION.adminURL + 'add_news.py'
            elif (self.model.operation in [OP_NEW_SECTION, OP_LAYOUT_ADD_SECTION]):
                if (int(self.model.step) == 1):
                    # goto 'add the section' page
                    redir = APPLICATION.adminURL + 'sectionWizard1.py'
            elif (self.model.operation == OP_NEW_NEWSPAGE):
                if (int(self.model.step) == 1):
                    # goto 'add the newspage' page
                    redir = APPLICATION.adminURL + 'newspageWizard1.py'
            elif (self.model.operation == OP_MANAGE):
                redir = APPLICATION.adminURL + 'admin_console.py'
            elif (self.model.operation == OP_DEFAULT_PAGE_WIZ):
                redir = APPLICATION.adminURL + 'admin_wizard.py'
            elif (self.model.operation == OP_DEFAULT_PAGE_CON):
                redir = APPLICATION.adminURL + 'admin_console.py'
            elif (OP_PAGE in self.model.operation):
                redir = APPLICATION.adminURL + 'edit_news.py'
            elif (self.model.operation == OP_NEW_USER):
                if (int(self.model.step) == 1):
                    redir = APPLICATION.adminURL + 'userWizard1.py'
            elif (self.model.operation in [OP_LAYOUT_INIT]):
                redir = APPLICATION.adminURL + 'layout_wizard.py'
            elif (self.model.operation in [OP_LAYOUT_SAVE_NEWSPAGE]):
                redir = APPLICATION.adminURL + URL_LAYOUT_GOOD_SAVE
            elif (self.model.operation in [OP_LAYOUT_MANAGE_SECTIONS]):
                redir = APPLICATION.adminURL + 'manage_sections.py'
            else:
                raise RouterError('Should not ever get in here')
        return redir

class WizardShowDefaultPageBO(BusinessObject):
    def execute(self):
        if (self.model.operation in [OP_DEFAULT_PAGE, OP_LAYOUT_DONE]):
            if (self.securityInfo.user.showWizard):
                self.model.operation = OP_DEFAULT_PAGE + '_wizard'
            else:
                self.model.operation = OP_DEFAULT_PAGE + '_console'

class WizardStartBO(BusinessObject):
    def execute(self):
        if (self.model.operation == OP_HIDE_WIZARDS):
            #This is an annoying contortion
            userParser = UserDataParser(FILENAME_USERS)
            userCollection = userParser.getUserCollection()
            user = userCollection.getUserByNickname(self.securityInfo.user.nickname)
            user.showWizard = not (user.showWizard)
            self.securityInfo.user.showWizard = user.showWizard
            udw = UserDataWriter(userCollection.getUsers())
            udw.write(FILENAME_USERS)
            self.model.operation = OP_DEFAULT_PAGE

class WizardNewUserBO(BusinessObject):
    def execute(self):
        if (self.model.operation == OP_NEW_USER):
            theStep = int(self.model.step)
            if (theStep == 1):

                # Goto the user data entry page

                pass
            elif (theStep == 2):

                # TODO

                # Create the user
                # Add the user to the collection
                # Save the user
                # Email the user

                # exit back to start page
                self.model.operation = OP_DEFAULT_PAGE

class WizardNewArticleBO(BusinessObject):
    def execute(self):
        if (self.model.operation == OP_NEW_ARTICLE):
            theStep = int(self.model.step)
            if (theStep == 1):
                # Set the list of newspages to which the user can add
                pages = loadNewsPageProperties(FILENAME_PAGES)
                sections = loadSections(FILENAME_SECTIONS)

                for page in pages:
                    section = sections[pages[page].newspage]
                    # TODO-R: Put this in some kind of callable method or object for reuse... it's confusing otherwise
                    if (pages[page].active and
                            section.isActive and
                            self.securityInfo.userRules.check(self.securityInfo.user.nickname,
                            UR_CREATE, UR_ARTICLES, pages[page].name) and
                            (pages[page].pageType != PAGE_GUESTBOOK) and
                            ((not pages[page].isBlog) or (pages[page].pageOwner == self.securityInfo.user.nickname))):
                        self.model.newspage += [pages[page].name]

                # If the users can add to only one change step = 2
                if (len(self.model.newspage) == 1):
                    self.model.step = '2'
                    self.model.infoMessage = 'You can only add to the \'' + \
                        pages[self.model.newspage[0]].title + '\' newspage at this time.'
            elif (theStep == 2):
                pass # on to the data entry page

class WizardEditArticleBO(BusinessObject):
    def execute(self):
        if (self.model.operation == OP_EDIT_ARTICLE):
            theStep = int(self.model.step)
            if (theStep == 1):
                # Identify the editable pages/articles
                pages = loadNewsPageProperties(FILENAME_PAGES)
                sections = loadSections(FILENAME_SECTIONS)

                for page in pages:
                    section = sections[pages[page].newspage]
                    # TODO-R: Put this in some kind of callable method or object for reuse... it's confusing otherwise
                    if (pages[page].active and
                            section.isActive and
                            self.securityInfo.userRules.check(self.securityInfo.user.nickname,
                            UR_CREATE, UR_ARTICLES, pages[page].name) and
                            (pages[page].pageType != PAGE_GUESTBOOK) and
                            ((not pages[page].isBlog) or (pages[page].pageOwner == self.securityInfo.user.nickname))):
                        self.model.newspage += [pages[page].name]

                # If the user can only edit articles on one page, change step = 2
                self.model.step = 2

class WizardNewNewspageBO(BusinessObject):
    def execute(self):
        if (self.model.operation == OP_NEW_NEWSPAGE):
            theStep = int(self.model.step)
            if (theStep == 1):
                # goto create a new newspage
                pass
            else:
                # save the newspage
                pages = loadNewsPageProperties(FILENAME_PAGES)
                newspage = NewsPage()
                newspage.name = self.model.newspage_name
                newspage.title = self.model.newspage_title
                newspage.subTitle = self.model.newspage_subTitle
                newspage.headlineType = self.model.newspage_headlineType
                newspage.pageType = self.model.newspage_pageType
                newspage.newspage = self.model.newspage_section
                newspage.column = int(self.model.newspage_column)
                newspage.displayNum = int(self.model.newspage_displayNum)
                newspage.rank = pages.getMaxRank() + 1
                newspage.isVisible = (self.model.newspage_isVisible in TRUE)
                newspage.pageOwner = self.securityInfo.user.nickname
                newspage.isBlog = False
                if (self.model.newspage_expires == 'Never'):
                    newspage.expires = self.model.newspage_expires
                else:
                    newspage.expires = int(self.model.newspage_expires)
                newspage.active = (self.model.newspage_locked not in TRUE)
                newspage.allowComments = (self.model.newspage_allowComments in TRUE)
                newspage.sortType = self.model.newspage_sortType
                newspage.promptComments = self.model.newspage_promptComments
                if (theStep == 2):
                    # goto create a new article
                    self.model.newspage += [newspage.name]
                    self.model.operation = OP_NEW_ARTICLE
                    self.model.step = 2
                elif (theStep == 3):
                    # exit
                    #if (('route' in self.model.__dict__) and (self.model.route == 'layout')):
                    #    self.model.operation = OP_LAYOUT_INIT
                    #    self.model.__dict__['layoutStartSection'] = newspage.newspage
                    #    self.model.__dict__['layoutStartNewspage'] = newspage.name
                    #else:
                    self.model.operation = OP_DEFAULT_PAGE
                elif (theStep == 4):
                    # create another newspage
                    self.model.__dict__['section_name'] = newspage.newspage
                    self.model.step = 1

                if (newspage.name in pages.keys()):
                    counter = 1
                    while ((newspage.name + str(counter)) in pages.keys()):
                        counter += 1
                    newspage.name += '_' + str(counter) + '_'
                    self.model.newspage_id = newspage.name

                pages[newspage.name] = newspage
                writeNewsPageProperties(pages, FILENAME_PAGES)

                createBlankPage(pages[newspage.name])

class WizardNewSectionBO(BusinessObject):
    def execute(self):
        if (self.model.operation == OP_NEW_SECTION):
            theStep = int(self.model.step)
            if (theStep == 1):
                # goto create the new section
                pass
            else:
                # Save the section
                sections = loadSections(FILENAME_SECTIONS)
                sectionList = buildSectionList(sections)
                sec = Section()
                sec.name = self.model.section_name
                sec.longname = self.model.section_longname
                sec.isVisible = (self.model.section_isVisible in TRUE)
                sec.isActive = (self.model.section_locked not in TRUE)
                sec.columns = int(self.model.section_columns)
                sec.order = len(sections)

                if (sec.name in sections.keys()):
                    counter = 1
                    while ((sec.name + str(counter)) in sections.keys()):
                        counter += 1
                    sec.name += '_' + str(counter) + '_'
                    self.model.section_name = sec.name

                sections[sec.name] = sec
                writeSections(FILENAME_SECTIONS, sections)
                sectionList = buildSectionList(sections)

                if (theStep == 2):
                    # goto create a new newspage
                    self.model.operation = OP_NEW_NEWSPAGE
                    self.model.step = '1'

                elif (theStep == 3):
                    # save and exit the wizard
                    if (('route' in self.model.__dict__) and (self.model.route == 'layout')):
                        self.model.operation = OP_LAYOUT_INIT
                        self.model.__dict__['layoutStartSection'] = sec.name
                    else:
                        self.model.operation = OP_DEFAULT_PAGE

                elif (theStep == 4):
                    # save and create another section
                    self.model.step = '1'

class LayoutInitBO(BusinessObject):
    ''' Initialize the layout tool. '''
    def execute(self):
        #log('Entering LayoutInitBO')
        if (self.model.operation == OP_LAYOUT_INIT):
            # Set the start section and start newspage
            pages = loadNewsPageProperties(FILENAME_PAGES)
            sections = loadSections(FILENAME_SECTIONS)

            if (self.model.layoutStartSection == ''):
                self.model.layoutStartSection = getHomepageSection(sections)

            for page in pages:
                if (pages[page].newspage == self.model.layoutStartSection):
                    self.model.layoutStartNewspage = pages[page].name
                    break
        #log('Leaving LayoutInitBO')

class LayoutDeleteNewspageBO(BusinessObject):
    ''' Delete a newspage from the layout tool.

        layoutCurrentNewspageID
        layoutCurrentSection
    '''
    def execute(self):
        #log('Entering LayoutDeleteNewspageBO')
        if ('deletedNewspages' in self.model.__dict__):
            # Load the pages
            pages = loadNewsPageProperties(FILENAME_PAGES)

            delPages = self.model.deletedNewspages.split(',')

            # Delete the newspage from the dict
            for item in delPages:
                if (item in pages):
                    del(pages[item])

            # Delete the files on disk
            # TODO: delete the html file and the data.xml file

            # Save the newspage properties
            writeNewsPageProperties(pages, FILENAME_PAGES)
        #log('Leaving LayoutDeleteNewspageBO')

class LayoutSaveNewspageBO(BusinessObject):
    def execute(self):
        #log('Entering LayoutSaveNewspageBO')
        if (('doSave' in self.model.__dict__) and
                self.model.doSave and
                ('newspage_name' in self.model.__dict__) and
                (self.model.newspage_name != '')):

            #log('In LayoutSaveNewspageBO')

            # Determine if it's a new or existing newspage
            pages = loadNewsPageProperties(FILENAME_PAGES)

            newspage = NewsPage()
            if (self.model.newspage_name in pages):
                newspage = pages[self.model.newspage_name]

            # Capture the properties
            newspage.name = self.model.newspage_name
            newspage.title = self.model.newspage_title
            newspage.subTitle = self.model.newspage_subTitle
            newspage.headlineType = self.model.newspage_headlineType
            newspage.pageType = self.model.newspage_pageType
            newspage.newspage = self.model.newspage_section

            for i in range (0,3):
                if (('gridColumns' + str(i)) in self.model.__dict__):
                    if (newspage.name in self.model.__dict__['gridColumns' + str(i)].split(',')):
                        newspage.column = i
                        #log('\tSet ' + newspage.name + ' to column: ' + str(newspage.column))
                        break

            newspage.displayNum = int(self.model.newspage_displayNum)
            newspage.rank = pages.getMaxRank() + 1
            newspage.isVisible = (self.model.newspage_isVisible in TRUE)
            newspage.pageOwner = self.securityInfo.user.nickname
            newspage.isBlog = False
            if (self.model.newspage_expires == 'Never'):
                newspage.expires = self.model.newspage_expires
            else:
                newspage.expires = int(self.model.newspage_expires)
            newspage.active = (self.model.newspage_locked not in TRUE)
            newspage.allowComments = (self.model.newspage_allowComments in TRUE)
            newspage.sortType = self.model.newspage_sortType
            newspage.promptComments = self.model.newspage_promptComments

            pages[newspage.name] = newspage

            # Save the properties
            writeNewsPageProperties(pages, FILENAME_PAGES)

            if (not newspageDataFileExists(pages[newspage.name])):
                createBlankPage(pages[newspage.name])

            self.model.layoutStartNewspage = self.model.newspage_name
        #log('Leaving LayoutSaveNewspageBO')

class LayoutSaveSectionBO(BusinessObject):
    def execute(self):
        #log('Entering LayoutSaveSectionBO')
        if (('doSave' in self.model.__dict__) and
                self.model.doSave and
                ('sectionColumns' in self.model.__dict__)):
            #log('In LayoutSaveSectionBO')

            # load the sections and pages
            sections = loadSections(FILENAME_SECTIONS)
            pages = loadNewsPageProperties(FILENAME_PAGES)

            # Get the section that is being saved
            section = sections[self.model.layoutCurrentSection]

            # Set the number of columns
            section.columns = self.model.sectionColumns

            # Reorder the pages in the section according to the layout vars
            for i in range (0,3):
                if (('gridColumns' + str(i)) in self.model.__dict__):
                    orderedPages = self.model.__dict__['gridColumns' + str(i)].split(',')

                    for item in orderedPages:
                        if (item in pages):
                            tpage = pages[item]
                            del(pages[item])
                            tpage.column = i
                            tpage.id = -1
                            pages[tpage.name] = tpage
                            #log('\tAdded ' + tpage.name + ' in column: ' + str(i) + ' with id: ' + str(tpage.id) + ' and rank: ' + str(tpage.rank))

            # Save the properties
            writeNewsPageProperties(pages, FILENAME_PAGES)
            writeSections(FILENAME_SECTIONS, sections)

        #log('Leaving LayoutSaveSectionBO')


class LayoutCheckRoutingBO(BusinessObject):
    def execute(self):
        #log('Entering LayoutCheckRoutingBO')
        if (('layoutStartSection' in self.model.__dict__) and
                ('layoutCurrentSection' in self.model.__dict__)):

            #log('In LayoutCheckRoutingBO')

            # have to do some routing here
            if (self.model.layoutStartSection != self.model.layoutCurrentSection):
                self.model.operation = OP_LAYOUT_INIT

            # Set the start section and start newspage
            self.model.layoutStartSection = self.model.layoutCurrentSection
            if (self.model.layoutStartNewspage == ''):
                pages = loadNewsPageProperties(FILENAME_PAGES)
                for page in pages:
                    if (pages[page].newspage == self.model.layoutStartSection):
                        self.model.layoutStartNewspage = pages[page].name
                        break
        #log('Leaving LayoutCheckRoutingBO')