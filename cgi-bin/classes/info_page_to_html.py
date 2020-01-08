#imports
from article import *
from newscommunity.application import APPLICATION
from newscommunity.templatevars import *
from newscommunity.ncvars import *
from article_to_html import *
from info_page_handler import *
from util.fileutils import Semaphore
from util.html_utils import unicodeToXML
from newspage_handler import *
from menu_builder import *
from ui.mvc_mail import OP_CONTACT_FORM

#declarations
semname = 'infoPageSem2'


#definitions

def getSubTitle(page):
    data = page.subTitle
    if (APPLICATION.subTitleDate):
        if ((data is not None) and (data != '')):
            data += ' - '
        data += getTodayHTML()
    return data

#classes
class InfoPageMaker:

    def __init__(self, infoPages = None, menuBuilder = None):
        """Initialze the class with a file name relative to the path of the root script.
            filename - the location + name of the infopage file
        """

        self.title = '${pageTitle}'
        self.subTitle = '${subTitle}'
        self.heading = '${pageHeading}'
        self.newsHTML = '${infoPageContent}'
        self.newsTOC = '${simpleTOC}'
        self.rssurl = '${rssurl}'
        self.divInsert = '${divInsert}'
        self.newsletter = '${newsletter}'

        self.infoPages = infoPages
        self.menuBuilder = menuBuilder

    def getMenuInfo(self, currentPage = None):
        raise 'DEPRECATION ERROR: Deprecated InfoPageMaker.getMenuInfo()'
        # TODO: Remove this deprecated method
        data = ''
        for page in self.infoPages:
            if (page.isVisible and (page.name != INFO_PAGE_CONTACT_THANKS)):
                if ((page.name == INFO_PAGE_CONTACT) and (APPLICATION.contactEmail == '')):
                    continue
                if (data != ''):
                    data += APPLICATION.menuSeparator
                if ((currentPage is None) or (currentPage != page.name)):
                    data += ' <span class="sectionMenu">' + \
                        '<a href="' + page.filename + '" title="Go to the ' + \
                        page.title + ' page">' + \
                        page.menuName + '</a></span> '
                else:
                    data += ' <span class="sectionMenu">' + \
                        page.menuName + '</span> '
        return data

    def writeInfoPageHTML(self, templatename, fileDir, addNewsletter = False):
        # Need to convert to a list so that I'm not calling the iterator on top of itself
        ips = list()
        for item in self.infoPages:
            if (item.isVisible or (item.name == INFO_PAGE_CONTACT_THANKS)):
                if ((item.name == INFO_PAGE_CONTACT) and (APPLICATION.contactEmail == '')):
                    continue
                ips += [item]

        for infoPage in ips:
            self.__writeHTML__(infoPage, templatename, fileDir, addNewsletter)

    def __writeHTML__(self, infoPage, templatename, fileDir, addNewsletter = False):
        """Process the InfoPage.

            templatename - the location + name of the page template file
            infoPage - the page object to be generated into HTML
            fileDir - the directory where pages are to be written
        """

        #Read in the template file
        pageTemplate = ''
        try:
            f = file(templatename)
            pageTemplate = f.read()
            f.close()

            replaceDict = dict()
            replaceDict['domain'] = APPLICATION.domainName
            replaceDict['siteTitle'] = APPLICATION.siteTitle
            replaceDict['metaKeywords'] = APPLICATION.metaKeywords
            replaceDict['metaDescription'] = APPLICATION.metaDescription
            if (APPLICATION.customStyle):
                replaceDict['style'] = APPLICATION.rootURL + APPLICATION.styleName
            else:
                replaceDict['style'] = APPLICATION.styleURL + APPLICATION.styleName

            replaceDict['printStyleURL'] = APPLICATION.printStyleURL
            replaceDict['divUser1'] = ''
            replaceDict['divUser2'] = ''
            replaceDict['divUser3'] = ''
            replaceDict['divUser4'] = ''
            replaceDict['divUser5'] = ''
            replaceDict['sectionMenu'] = self.menuBuilder.getMenu(None, infoPage.name)
            #replaceDict[''] = APPLICATION.

            for item in replaceDict:
                pageTemplate = pageTemplate.replace('${' + item + '}', replaceDict[item])
        except IOError:
            raise "IOError attempting to access:", templatename

        newPage = pageTemplate

        newPage = newPage.replace(self.title, infoPage.title)
        newPage = newPage.replace(self.heading, infoPage.title)
        newPage = newPage.replace(self.subTitle, infoPage.subtitle)
        if (infoPage.name == INFO_PAGE_CONTACT):
            newPage = newPage.replace(self.newsHTML, self.__getCommentPageBody__(infoPage.content))
        elif (infoPage.name == INFO_PAGE_SEARCH):
            newPage = newPage.replace(self.newsHTML, self.__getSearchPageBody__(infoPage))
        else:
            newPage = newPage.replace(self.newsHTML, infoPage.content)
        newPage = newPage.replace(self.newsTOC, '')
        newPage = newPage.replace(self.rssurl, '')
        newPage = newPage.replace(self.divInsert, '')
        if (addNewsletter):
            nltext = self.__getNewsletterText__()
            newPage = newPage.replace(self.newsletter, nltext)
        else:
            newPage = newPage.replace(self.newsletter, '')

        newPage = newPage.replace('${adminURL}', APPLICATION.adminURL)

        self.__writePage__(fileDir + infoPage.filename, newPage)

    def __getCommentPageBody__(self, content):
        prompts = content.split(':::')

        fbody = '''
<div class="innerBoxTitle">
<A NAME="1"> </a>
<span class="itemTitle">Contact us</span></div>
<div class="innerBox">
<TABLE CLASS="contactTable" BORDER="0" WIDTH="400" CELLPADDING="0" CELLSPACING="0">
    <TR>
        <TD WIDTH="400" COLSPAN="2">
        <P>Use this form to send
        us an email.  We will not use or sell your
        email in any way except to correspond with you,
        if you ask us to do so!
    <TR>
        <TD COLSPAN=2>&nbsp;
    <TR>
        <TD WIDTH="50" ALIGN="LEFT" VALIGN="TOP">Subject:
        <TD WIDTH="350" ALIGN="LEFT" VALIGN="TOP"><SELECT NAME="subject">
'''
        for item in prompts:
            if (item == prompts[0]):
                fbody += '            <OPTION VALUE="' + item + '" SELECTED>' + item + '\n'
            else:
                fbody += '            <OPTION VALUE="' + item + '">' + item + '\n'
        fbody += '''        </SELECT>
<TR>
    <TD COLSPAN=2>&nbsp;
<TR>
    <TD WIDTH="50" ALIGN="RIGHT" VALIGN="TOP">Name:
    <TD WIDTH="350" ALIGN="LEFT" VALIGN="TOP"><INPUT TYPE="text" NAME="fromName" SIZE="20">
<TR>
    <TD WIDTH="50" ALIGN="RIGHT" VALIGN="TOP">Email:
    <TD WIDTH="350" ALIGN="LEFT" VALIGN="TOP"><INPUT TYPE="text" NAME="fromEmail" SIZE="20">
<TR>
    <TD COLSPAN=2>&nbsp;
<TR>
    <TD WIDTH="50" ALIGN="RIGHT" VALIGN="TOP">Comment:
    <TD WIDTH="350" ALIGN="LEFT" VALIGN="TOP"><TEXTAREA ROWS="10" COLS="30" NAME="content"></TEXTAREA>
<TR>
    <TD WIDTH="400" ALIGN="CENTER" VALIGN="TOP" COLSPAN="2">Would you like us to contact you?
    <BR><INPUT TYPE="checkbox" CLASS="plaininput" NAME="contact" value="yes">
<TR>
    <TD COLSPAN="2">&nbsp;
<TR>
    <TD WIDTH="50" ALIGN="LEFT" VALIGN="TOP">&nbsp;
    <TD WIDTH="350" ALIGN="LEFT" VALIGN="TOP"><INPUT TYPE="submit"
        VALUE="Send comment">
</TABLE>
<INPUT TYPE="hidden" NAME="check" VALUE="------------------------------">
</div>
'''
        fbody += createHiddenInput('redirect', APPLICATION.rootURL + 'yjcontactthanks.html')
        fbody += createHiddenInput('operation', OP_CONTACT_FORM)

        body = createForm('sendComment', APPLICATION.adminURL + 'dispatch_mail.py', 'POST', fbody, onSubmit='javascript: return validateContactForm();')

        return body

    def __getSearchPageBody__(self, infoPage):
        pages = loadNewsPageProperties(FILENAME_PAGES)
        fbody = '''
<SCRIPT TYPE="text/javascript">
function doSubmit(){
    if (completeSelect()){
        var ff = getForm('searchForm');
        ff.submit();
    }
}
function completeSelect(){
    var terms = getFromForm('searchTerms', 'searchForm');
    var pageName = getFromForm('pageName', 'searchForm');
    var f = getForm('searchForm');
    var checkVals = true;

    if (terms.value == ''){
        checkVals = false;
        alert('You must type in at least one search term to search.');
    } else if (pageName.selectedIndex == -1){
        for (i = 0; i < pageName.length; i++){
            pageName.options[i].selected = true;
        }
    }
    return checkVals;
}
</SCRIPT>
<DIV CLASS="innerBoxTitle">
<A NAME="1"> </A>
<SPAN CLASS="itemTitle">''' + infoPage.title + '''</SPAN></DIV>
<DIV CLASS="innerBox">
<TABLE CLASS="searchTable" BORDER="0" WIDTH="500" CELLPADDING="0" CELLSPACING="0">
    <TR>
        <TH WIDTH="500" COLSPAN="2">
        <P>''' + infoPage.subtitle + '''
    <TR>
        <TD WIDTH="500" COLSPAN="2">
        <P>Search our articles here!  Separate words with spaces.  Click the checkbox below to force results to contain all terms.
        If you'd like to search specific pages, simply click on them in the box below.  Hold down the
        CTRL key to search multiple pages.
    <TR>
        <TH WIDTH="100" COLSPAN="2" ALIGN="LEFT" VALIGN="TOP" CLASS="mainbody"><p>Search terms:
'''
        fbody += createTextInput('searchTerms', '', 50, 255) + '\n'
        fbody += '''
<TR>
    <TH ALIGN="LEFT" VALIGN="TOP"><p>Pages:<br>
'''
        pDict = dict()
        for page in pages:
            if (pages[page].isVisible):
                pDict[pages[page].name] = pages[page].title
        fbody += createSelect('pageName', pDict, size = 10, multiple = True)
        fbody += '''
    <TH ALIGN="LEFT" VALIGN="TOP"><p>''' + createCheckBox('findAllTerms', True, False) + \
        ''' Only return results with all terms
    <p>''' + createCheckBox('caseSensitive', True, False) + ''' Case sensitive
    <p>''' + createCheckBox('verbose', True, False) + ''' Verbose results
    <p>''' + createCheckBox('treatAsPhrase', True, False) + ''' Treat as one phrase
    <BR>&nbsp;<BR>
    <P>''' + createLink('javascript:doSubmit()', 'Search', 'Start search') + '''
<TR>
    <TH ALIGN="RIGHT" COLSPAN="2" VALIGN="TOP">&nbsp;
<TR>
    <TD ALIGN="LEFT" COLSPAN="2" VALIGN="TOP">&nbsp;
</div>
</TABLE>
'''

        body = createForm('searchForm', APPLICATION.adminURL + 'search.py', 'GET', fbody, onSubmit='javascript:return completeSelect();')
        return body


    # TODO: combine this into a utility method to reduce duplication with newspage_to_html.py
    def __getNewsletterText__(self):

        nlbody = 'Please enter your name:\n'
        nlbody += createTextInput('nl_name') + '<BR>\n'
        nlbody += 'Please enter your email:\n'
        nlbody += createTextInput('nl_email') + '\n'
        nlbody += '<BR>\n'
        nlbody += '<INPUT TYPE=BUTTON NAME=SUBMIT VALUE="Submit" onMousedown="javascript:validateNLForm()">'
        nlbody = createForm('nlform', APPLICATION.adminURL + 'submit_newsletter_recipient.py', \
            'POST', nlbody, target = 'nltarget') + '\n'

        nlscript = '<SCRIPT TYPE="text/javascript">\n'
        nlscript += 'function validateNLForm(){\n'
        nlscript += '    if (!checkValidEmail(getFromForm("nl_email", "nlform").value)){\n'
        nlscript += '        alert("Please enter a valid email.");\n'
        nlscript += '    } else {\n'
        nlscript += '        getForm("nlform").submit();\n'
        nlscript += '    }\n'
        nlscript += '}\n'
        nlscript += '</SCRIPT>\n'

        nlbody = nlscript + nlbody
        nlbody += '<IFRAME NAME="nltarget" HEIGHT="0" WIDTH="0"></IFRAME>\n'
        #nltext = createFloatingDiv('Sign up for newsletter', \
        #    'Sign up for newsletter', nlbody, 'newsletter', False, \
        #    'newsletter', yshift = -200)
        nltext = createPopupLink('Sign up for our newsletter', 'Sign up for our newsletter',
            nlbody, clazz='guestbook', divID='newsletter')
        return nltext

    def __writePage__(self, filename, pageData):
        #Write the page to a file

        try:
            sem = Semaphore(semname)
            sem.put()

            ff = file(filename, 'w')
            ff.write(unicodeToXML(pageData))
            ff.flush()
            ff.close()

            sem.remove()
        except IOError:
            raise "IOError attempting to write:", filename
