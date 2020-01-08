

# TODO: Refactor this stuff so that there is a consistent theme for escaping unicode/special chars/html... yuck
def toSafeHTML(data):
    data = unicodeToXML(data)
    data = data.replace('\'', '&#39;')
    data = data.replace('\"', '&#34;')
    return data

def toSafeXMLAttributeText(data):
    data = unicodeToXML(data)
    data = data.replace('\'', '&#39;')
    data = data.replace('\"', '&#34;')
    data = data.replace('<', '&lt;')
    data = data.replace('>', '&gt;')
    data = data.replace('&amp;', '&')
    data = data.replace('&', '&amp;')
    data = data.replace('&amp;#', '&#')
    data = data.replace('&amp;lt;', '&lt;')
    data = data.replace('&amp;gt;', '&gt;')
    data = data.replace('&amp;nbsp;', '&nbsp;')
    return data

def undoSafeHTML(data):
    data = unicodeToXML(data)
    data = data.replace('&#39;', '\'')
    data = data.replace('&#34;', '\"')
    return data

def unicodeToXML(data):
    if (type(data) == type(u"a")):
        try:
            data = data.encode('ascii', 'xmlcharrefreplace')
        except ValueError:
            # ValueError is raised if there are unencodable chars in the
            # data and the 'xmlcharrefreplace' error handler is not found.
            # Pre-2.3 Python doesn't support the 'xmlcharrefreplace' error
            # handler, so we'll emulate it.
            data = _xmlcharref_encode(data, 'ascii')
    return str(data)

def _xmlcharref_encode(unicode_data, encoding):
    """Emulate Python 2.3's 'xmlcharrefreplace' encoding error handler."""
    chars = []
    # Step through the unicode_data string one character at a time in
    # order to catch unencodable characters:
    for char in unicode_data:
        try:
            chars.append(char.encode(encoding, 'strict'))
        except UnicodeError:
            chars.append('&#%i;' % ord(char))
    return ''.join(chars)

def safeText(data):
    try:
        #data = data.replace('&amp;', '&')
        #data = data.replace('&', '&amp;')
        #data = data.replace('&amp;#', '&#')
        #data = data.replace('&amp;lt;', '&lt;')
        #data = data.replace('&amp;gt;', '&gt;')
        #data = data.replace('&amp;nbsp;', '&nbsp;')
        data = unicodeToXML(data)
    except:
        strData = ''
        for i in range(len(data)):
            if (ord(data[i]) > 128):
                strData += ' '
            else:
                strData += data[i]
        data = strData
    #data = data.replace("\r\n\r\n", "<p>");
    #data = data.replace("\n\n", "<p>");
    #data = data.replace("\n", "<br>");
    #data = data.replace("<p><p>", "<p>");
    #data = data.replace("<br><p>", "<p>");
    return data

def RTESafe(data):
    ''' Returns safe code for preloading in the RTE '''

    #convert all types of single quotes
    data = data.replace(chr(145), chr(39))
    data = data.replace(chr(146), chr(39))
    data = data.replace("'", "&#39;")

    #convert all types of double quotes
    data = data.replace(chr(147), chr(34))
    data = data.replace(chr(148), chr(34))
    #tmpString = data.replace("""", "\""")

    #replace carriage returns & line feeds
    data = data.replace(chr(10), " ")
    data = data.replace(chr(13), " ")
    return data

def unSafeText(data):
    try:
        data = unicodeToXML(data)
    except:
        strData = ''
        for i in range(len(data)):
            if (ord(data[i]) > 128):
                strData += ' '
            else:
                strData += data[i]
        data = strData
    data = data.replace('&amp;', '&amp;amp;')
    data = data.replace('&lt;', '&amp;lt;')
    data = data.replace('&gt;', '&amp;gt;')
    data = data.replace('&nbsp;', '&amp;nbsp;')
    #data = data.replace("<p>", "\r\n\r\n");
    #data = data.replace("<br>", "\r\n");
    return data