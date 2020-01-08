import sgmllib

class AnchorFinder(sgmllib.SGMLParser):
    ''' Retrieves a list of unique anchors from html. '''

    def __init__(self, prefix = None, skippedVals = None):
        ''' Constructor.  Set prefix to something like 'http://www.yakjive.com'
            if you only want anchors starting with that value.
        '''
        sgmllib.SGMLParser.__init__(self)
        self.prefix = prefix
        self.anchorDict = dict()
        self.skippedVals = skippedVals

    def __addAnchor__(self, value):
        self.anchorDict[value] = 1

    def getAnchors(self):
        ''' Returns a list of unique anchor URL's. '''
        return self.anchorDict.keys()

    def start_a(self, attrs):
        for item in attrs:
            if (item[0] == 'href'):
                if (item[1] == ''):
                    continue
                if (not self.__checkSkippedVals__(item[1])):
                    continue
                if ((self.prefix is not None) and
                        (item[1].find(self.prefix) != 0)):
                    continue
                self.__addAnchor__(item[1])
        return

    def process(self, some_html):
        ''' Process some HTML.  Returns the list of Anchors. '''
        self.feed(some_html)
        self.close()
        return self.getAnchors()

    def __checkSkippedVals__(self, value):
        check = True
        for item in self.skippedVals:
            if (item in value):
                check = False
                break
        return check

class Stripper(sgmllib.SGMLParser):
    ''' Strips out almost all HTML from a string.'''
    def __init__(self):
        sgmllib.SGMLParser.__init__(self)

    def strip(self, some_html):
        self.theString = ""
        self.feed(some_html)
        self.close()
        return self.theString

    def handle_charref(self, ref):
        self.handle_data('&#' + str(ref) + ';')

    def do_p(self, attrs):
        self.handle_data(' ')

    def do_br(self, attrs):
        self.handle_data(' ')

    def handle_data(self, data):
        self.theString += data

# stripper = Stripper()
# print stripper.strip("some boring text goes here")

# hc = HTMLCleaner()
# hc.clean('<html><a href="afdsfadsf" title="fadadsfd">asdfasdf</a><img src=""><p><b>&#234;&amp;</b><!--test comment--></html>')

class HTMLCleaner(sgmllib.SGMLParser):
    ''' Cleans out tags that might cause trouble, such as HTML, HEAD, BODY, OBJECT, and several others.
        TEXTAREA must be cut out or it screws up the input forms in the admin site.
    '''
    def __init__(self):
        sgmllib.SGMLParser.__init__(self)

    def clean(self, some_html):
        self.theString = ""
        self.feed(some_html)
        self.close()
        return self.theString

    def handle_charref(self, ref):
        self.handle_data('&#' + str(ref) + ';')

    def handle_entityref(self, ref):
        self.handle_data('&' + str(ref) + ';')

    def handle_comment(self, comment):
        self.handle_data('<!--' + comment + '-->')

    def handle_starttag(self, tag, method, attributes):
        self.handle_data(self.get_starttag_text())

    def handle_endtag(self, tag, method):
        self.handle_data('</' + tag + '>')

    def handle_data(self, data):
        self.theString += data

    # The following methods make sure that each individual element that is to be preserved will
    # be put on the parser queue to be handled.  To remove an element from being printed out,
    # remove its three methods from below.
    def start_a(self, attrs):
        return
    def start_abbr(self, attrs):
        return
    def start_acronym(self, attrs):
        return
    def start_address(self, attrs):
        return
    def start_area(self, attrs):
        return
    def start_b(self, attrs):
        return
    def start_base(self, attrs):
        return
    def start_bdo(self, attrs):
        return
    def start_big(self, attrs):
        return
    def start_blockquote(self, attrs):
        return
    def start_br(self, attrs):
        return
    def start_button(self, attrs):
        return
    def start_caption(self, attrs):
        return
    def start_cite(self, attrs):
        return
    def start_code(self, attrs):
        return
    def start_col(self, attrs):
        return
    def start_colgroup(self, attrs):
        return
    def start_dd(self, attrs):
        return
    def start_del(self, attrs):
        return
    def start_div(self, attrs):
        return
    def start_em(self, attrs):
        return
    def start_fieldset(self, attrs):
        return
    def start_h1(self, attrs):
        return
    def start_h2(self, attrs):
        return
    def start_h3(self, attrs):
        return
    def start_h4(self, attrs):
        return
    def start_h5(self, attrs):
        return
    def start_h6(self, attrs):
        return
    def start_hr(self, attrs):
        return
    def start_i(self, attrs):
        return
    def start_img(self, attrs):
        return
    def start_input(self, attrs):
        return
    def start_ins(self, attrs):
        return
    def start_kbd(self, attrs):
        return
    def start_label(self, attrs):
        return
    def start_legend(self, attrs):
        return
    def start_li(self, attrs):
        return
    def start_map(self, attrs):
        return
    def start_noscript(self, attrs):
        return
    def start_ol(self, attrs):
        return
    def start_optgroup(self, attrs):
        return
    def start_option(self, attrs):
        return
    def start_p(self, attrs):
        return
    def start_pre(self, attrs):
        return
    def start_q(self, attrs):
        return
    def start_samp(self, attrs):
        return
    def start_select(self, attrs):
        return
    def start_small(self, attrs):
        return
    def start_span(self, attrs):
        return
    def start_strong(self, attrs):
        return
    def start_style(self, attrs):
        return
    def start_sub(self, attrs):
        return
    def start_sup(self, attrs):
        return
    def start_table(self, attrs):
        return
    def start_tbody(self, attrs):
        return
    def start_td(self, attrs):
        return
    # Text areas will break the article entry form
    #def start_textarea(self, attrs):
    #    return
    def start_tfoot(self, attrs):
        return
    def start_th(self, attrs):
        return
    def start_thead(self, attrs):
        return
    def start_tr(self, attrs):
        return
    def start_tt(self, attrs):
        return
    def start_ul(self, attrs):
        return

    def do_a(self, attrs):
        return
    def do_abbr(self, attrs):
        return
    def do_acronym(self, attrs):
        return
    def do_address(self, attrs):
        return
    def do_area(self, attrs):
        return
    def do_b(self, attrs):
        return
    def do_base(self, attrs):
        return
    def do_bdo(self, attrs):
        return
    def do_big(self, attrs):
        return
    def do_blockquote(self, attrs):
        return
    def do_br(self, attrs):
        return
    def do_button(self, attrs):
        return
    def do_caption(self, attrs):
        return
    def do_cite(self, attrs):
        return
    def do_code(self, attrs):
        return
    def do_col(self, attrs):
        return
    def do_colgroup(self, attrs):
        return
    def do_dd(self, attrs):
        return
    def do_del(self, attrs):
        return
    def do_div(self, attrs):
        return
    def do_em(self, attrs):
        return
    def do_fieldset(self, attrs):
        return
    def do_h1(self, attrs):
        return
    def do_h2(self, attrs):
        return
    def do_h3(self, attrs):
        return
    def do_h4(self, attrs):
        return
    def do_h5(self, attrs):
        return
    def do_h6(self, attrs):
        return
    def do_hr(self, attrs):
        return
    def do_i(self, attrs):
        return
    def do_img(self, attrs):
        return
    def do_input(self, attrs):
        return
    def do_ins(self, attrs):
        return
    def do_kbd(self, attrs):
        return
    def do_label(self, attrs):
        return
    def do_legend(self, attrs):
        return
    def do_li(self, attrs):
        return
    def do_map(self, attrs):
        return
    def do_noscript(self, attrs):
        return
    def do_ol(self, attrs):
        return
    def do_optgroup(self, attrs):
        return
    def do_option(self, attrs):
        return
    def do_p(self, attrs):
        return
    def do_pre(self, attrs):
        return
    def do_q(self, attrs):
        return
    def do_samp(self, attrs):
        return
    def do_select(self, attrs):
        return
    def do_small(self, attrs):
        return
    def do_span(self, attrs):
        return
    def do_strong(self, attrs):
        return
    def do_style(self, attrs):
        return
    def do_sub(self, attrs):
        return
    def do_sup(self, attrs):
        return
    def do_table(self, attrs):
        return
    def do_tbody(self, attrs):
        return
    def do_td(self, attrs):
        return
    #def do_textarea(self, attrs):
    #    return
    def do_tfoot(self, attrs):
        return
    def do_th(self, attrs):
        return
    def do_thead(self, attrs):
        return
    def do_tr(self, attrs):
        return
    def do_tt(self, attrs):
        return
    def do_ul(self, attrs):
        return

    def end_a(self):
        return
    def end_abbr(self):
        return
    def end_acronym(self):
        return
    def end_address(self):
        return
    def end_area(self):
        return
    def end_b(self):
        return
    def end_base(self):
        return
    def end_bdo(self):
        return
    def end_big(self):
        return
    def end_blockquote(self):
        return
    def end_br(self):
        return
    def end_button(self):
        return
    def end_caption(self):
        return
    def end_cite(self):
        return
    def end_code(self):
        return
    def end_col(self):
        return
    def end_colgroup(self):
        return
    def end_dd(self):
        return
    def end_del(self):
        return
    def end_div(self):
        return
    def end_em(self):
        return
    def end_fieldset(self):
        return
    def end_h1(self):
        return
    def end_h2(self):
        return
    def end_h3(self):
        return
    def end_h4(self):
        return
    def end_h5(self):
        return
    def end_h6(self):
        return
    def end_hr(self):
        return
    def end_i(self):
        return
    def end_img(self):
        return
    def end_input(self):
        return
    def end_ins(self):
        return
    def end_kbd(self):
        return
    def end_label(self):
        return
    def end_legend(self):
        return
    def end_li(self):
        return
    def end_map(self):
        return
    def end_noscript(self):
        return
    def end_ol(self):
        return
    def end_optgroup(self):
        return
    def end_option(self):
        return
    def end_p(self):
        return
    def end_pre(self):
        return
    def end_q(self):
        return
    def end_samp(self):
        return
    def end_select(self):
        return
    def end_small(self):
        return
    def end_span(self):
        return
    def end_strong(self):
        return
    def end_style(self):
        return
    def end_sub(self):
        return
    def end_sup(self):
        return
    def end_table(self):
        return
    def end_tbody(self):
        return
    def end_td(self):
        return
    #def end_textarea(self):
    #    return
    def end_tfoot(self):
        return
    def end_th(self):
        return
    def end_thead(self):
        return
    def end_tr(self):
        return
    def end_tt(self):
        return
    def end_ul(self):
        return

class PremiumHTMLCleaner(HTMLCleaner):
    ''' A version of the cleaner that adds the ability to keep
        FORM and SCRIPT HTML elements.
    '''

    def __init__(self):
        ''' Constructor. '''
        HTMLCleaner.__init__(self)

    def start_form(self, attrs):
        return
    def do_form(self, attrs):
        return
    def end_form(self):
        return

    def start_script(self, attrs):
        return
    def do_script(self, attrs):
        return
    def end_script(self):
        return
