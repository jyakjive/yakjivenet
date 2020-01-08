
# imports
from newscommunity.application import APPLICATION
from utils import *
from newscommunity.ncvars import TRUE

# declarations

# definitions

# classes

class Comment:

    id = None
    content = None
    name = None
    email = None
    hideAddress = True
    createdDate = None

class CommentDaoFactory:
    ''' Factory class for creating DAO objects to load comments for articles. '''

    def create(cls, apID=None):
        ''' Create the DAO. '''
        return CommentDaoImpl(apID)

    # TODO-L: If server converts to Python 2.4, change to function decorator
    create = classmethod(create)

class CommentDao:
    ''' Base class for objects that will retrieve comments from some kind of data store.'''

    def __init__(self, apID=None):
        pass

    def fetchByArticleID(self, id, oldestFirst=True):
        ''' Get the comments for an article using the article id.
            This method should also fetch the results in order from either oldest-to-youngest
            or youngest-to-oldest.
        '''
        raise Exception('Not implemented')

    def write(self, articleID, comment):
        ''' Insert (or update) a comment for the given article ID. '''
        raise Exception('Not implemented')

    def delete(self, comment):
        ''' Delete a comment from the data store. '''
        raise Exception('Not implemented')

    def deleteByArticleID(self, articleID):
        ''' Delete a comment from the data store.

            returns true if the comment was deleted, false if not
        '''
        raise Exception('Not implemented')

class CommentDaoImpl(CommentDao, ConnectionAwareObject):
    ''' Object used to read/write/delete comments in MySQL. '''

    TABLE_COMMENT = 'comment' + '_${ID}'

    C_ID = 'id'
    C_ARTICLE_ID = 'article_id'
    C_CONTENT = 'content'
    C_NAME = 'name'
    C_EMAIL = 'email'
    C_HIDE_ADDRESS = 'hide_address'
    C_CREATED_DATE = 'created_date'

    # SELECT variables
    SELECT = 'SELECT '
    FROM = 'FROM '
    WHERE = 'WHERE '
    AND = 'AND '
    ORDER_BY_CREATED_DATE_ASC = 'ORDER BY a.' + C_CREATED_DATE + ' ASC '
    ORDER_BY_CREATED_DATE_DESC = 'ORDER BY a.' + C_CREATED_DATE + ' DESC '

    SELECT_COLUMNS = 'a.' + C_ID + ', ' + C_CONTENT + ', ' + \
        C_NAME + ', ' + C_EMAIL + ', ' + C_HIDE_ADDRESS + ', ' + C_CREATED_DATE + ' '

    WHERE_ARTICLE_ID = 'a.' + C_ARTICLE_ID + ' = %s '

    SELECT_BY_ARTICLE_ID = SELECT + SELECT_COLUMNS + FROM + \
        TABLE_COMMENT + ' a ' + WHERE + WHERE_ARTICLE_ID

    # INSERT variables

    INSERT = 'INSERT '
    INTO = 'INTO '
    VALUES = 'VALUES'
    ON_DUPLICATE_KEY_UPDATE = 'ON DUPLICATE KEY UPDATE '

    COMMENT_INSERT_COLUMNS = C_ID + ', ' + C_ARTICLE_ID + ', ' + C_CONTENT + ', ' + \
        C_NAME + ', ' + C_EMAIL + ', ' + C_HIDE_ADDRESS + ', ' + C_CREATED_DATE

    INSERT_COMMENT = INSERT + INTO + TABLE_COMMENT + '(' + \
        COMMENT_INSERT_COLUMNS + ') ' + VALUES + \
        '(%s, %s, %s, %s, %s, %s, %s) ' + \
        ON_DUPLICATE_KEY_UPDATE + \
        C_ARTICLE_ID + '=' + VALUES + '(' + C_ARTICLE_ID + '), ' + \
        C_CONTENT + '=' + VALUES + '(' + C_CONTENT + '), ' + \
        C_NAME + '=' + VALUES + '(' + C_NAME + '), ' + \
        C_EMAIL + '=' + VALUES + '(' + C_EMAIL + '), ' + \
        C_HIDE_ADDRESS + '=' + VALUES + '(' + C_HIDE_ADDRESS + '), ' + \
        C_CREATED_DATE + '=' + VALUES + '(' + C_CREATED_DATE + ')'

    # DELETE variables

    DELETE = 'DELETE '

    WHERE_DELETE_COMMENT = C_ID + ' = %s '
    WHERE_DELETE_ARTICLE = C_ARTICLE_ID + ' = %s '

    DELETE_COMMENT_BY_ID = DELETE + FROM + TABLE_COMMENT + ' ' + WHERE + WHERE_DELETE_COMMENT
    DELETE_COMMENT_BY_ARTICLE_ID = DELETE + FROM + TABLE_COMMENT + ' ' + WHERE + WHERE_DELETE_ARTICLE

    def __init__(self, apID = None):
        CommentDao.__init__(self, apID)
        ConnectionAwareObject.__init__(self)
        if (apID is None):
            self.applicationID = APPLICATION.ID
        else:
            self.applicationID = apID
        self.__setUpQueries()

    def __setUpQueries(self):
        # Replace the table names with table_name_[site id number]
        self.SELECT_BY_ARTICLE_ID = self.SELECT_BY_ARTICLE_ID.replace('${ID}', str(self.applicationID))
        self.INSERT_COMMENT = self.INSERT_COMMENT.replace('${ID}', str(self.applicationID))
        self.DELETE_COMMENT_BY_ID = self.DELETE_COMMENT_BY_ID.replace('${ID}', str(self.applicationID))
        self.DELETE_COMMENT_BY_ARTICLE_ID = self.DELETE_COMMENT_BY_ARTICLE_ID.replace('${ID}', str(self.applicationID))

    def fetchByArticleID(self, articleID, oldestFirst=True):
        ''' Get the comments for an article using the article id.
            This method should also fetch the results in order from either oldest-to-youngest
            or youngest-to-oldest.

            returns a list of comments; an empty list if no comments were found
        '''
        comments = list()

        try:
            cursor = self.getCursor()
            select = self.SELECT_BY_ARTICLE_ID
            if (oldestFirst):
                select += ' ' + self.ORDER_BY_CREATED_DATE_ASC
            else:
                select += ' ' + self.ORDER_BY_CREATED_DATE_DESC

            retval = cursor.execute(select, (articleID,))
            self.getConnection().commit()

            if (retval >= 1):
                for item in cursor.fetchall():
                    comment = Comment()
                    i = 0
                    comment.id = item[i]; i += 1
                    comment.content = item[i]; i += 1
                    comment.name = item[i]; i += 1
                    comment.email = item[i]; i += 1
                    comment.hideAddress = (item[i] in TRUE); i += 1
                    comment.createdDate = item[i]
                    comments += [comment]
        finally:
            self.releaseCursor()

        return comments

    def write(self, articleID, comment):
        ''' Insert (or update) a comment for the given article ID.

            returns the comment id if it was inserted/updated, -1 if not
        '''

        if (comment.id <= 0):
            comment.id = None

        try:
            try:
                cursor = self.getCursor()
                queryValues = (comment.id,
                    articleID,
                    comment.content,
                    comment.name,
                    comment.email,
                    toMySqlBoolean(comment.hideAddress),
                    toMySqlDateString(comment.createdDate))
                numberInserted = cursor.execute(self.INSERT_COMMENT, queryValues)
                self.getConnection().commit()
                if (numberInserted < 1):
                    raise DaoException('Did not get expected value (1 or 2) on Comment insert: ' + str(numberInserted))
                commentID = cursor.lastrowid

                if (comment.id is None):
                    comment.id = commentID
            except Exception, e:
                msg = 'CommentDaoImpl.write() ERROR: ' + str(e) + ' ' + self.INSERT_COMMENT + ' ' + queryValues
                log(msg)
                raise DaoException(msg)
        finally:
            self.releaseCursor()

        return commentID

    def delete(self, comment):
        ''' Delete a comment from the data store.

            returns true if the comment was deleted, false if not
        '''
        deleted = False

        try:
            cursor = self.getCursor()
            numberInserted = cursor.execute(self.DELETE_COMMENT_BY_ID, (comment.id,))
            self.getConnection().commit()

            deleted = (numberInserted > 0)
        finally:
            self.releaseCursor()

        return deleted

    def deleteByArticleID(self, articleID):
        ''' Delete a comment from the data store.

            returns true if the comment was deleted, false if not
        '''
        deleted = False

        try:
            cursor = self.getCursor()
            numberInserted = cursor.execute(self.DELETE_COMMENT_BY_ARTICLE_ID, (articleID,))
            self.getConnection().commit()

            deleted = (numberInserted > 0)
        finally:
            self.releaseCursor()

        return deleted



