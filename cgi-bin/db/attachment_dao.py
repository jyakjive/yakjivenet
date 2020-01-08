
# imports
from newscommunity.application import APPLICATION
from utils import *
from newscommunity.ncvars import TRUE
from util.fileutils import log

# declarations

# definitions

# classes

class Attachment:

    id = None
    filename = None
    originalFilename = None
    notes = None
    align = None
    image = False
    imageHeight = 0
    imageWidth = 0
    thumbnailName = None
    thumbnailHeight = 0
    thumbnailWidth = 0
    size = 0
    createdDate = datetime.datetime.today()

    articleAttachmentId = None

    def __str__(self):
        data = 'Attachment instance:\r\n'
        for item in self.__dict__:
            data += '\t' + item + ':' + str(self.__dict__[item]) + '\r\n'
        return data

class AttachmentDaoFactory:
    ''' Factory class for creating DAO objects to load attachments for articles. '''

    def create(cls, apID = None):
        ''' Create the DAO. '''
        return AttachmentDaoImpl(apID)

    # TODO-L: If server converts to Python 2.4, change to function decorator
    create = classmethod(create)

class AttachmentDao:
    ''' Base class for objects that will be used to load Attachments from a data store. '''

    def __init__(self, apID = None):
        pass

    def fetchByArticleID(self, articleID):
        ''' Get a list of attachments using the article ID.

            returns a list of attachments or an empty list if none are found
        '''
        raise DaoException('Not implemented')

    def write(self, articleID, attachment):
        ''' Inserts or updates an attachment given the articleID.

            returns a the id of the inserted/updated item or -1 if none was inserted
        '''
        raise DaoException('Not implemented')

    def delete(self, attachment):
        ''' Deletes an attachment.

            returns true if an item was deleted
        '''
        raise DaoException('Not implemented')

    def deleteByArticleID(self, articleID):
        ''' Deletes all the attachments associated with an article.

            returns true if an item was deleted
        '''
        raise DaoException('Not implemented')

class AttachmentDaoImpl(AttachmentDao, ConnectionAwareObject):
    ''' Object used to read/write/delete comments in MySQL. '''

    TABLE_ATTACHMENT = 'attachment' + '_${ID}'
    TABLE_ARTICLE_ATTACHMENT = 'article_attachment' + '_${ID}'

    A_ID = 'id'
    A_FILENAME = 'filename'
    A_ORIGINAL_FILENAME = 'original_filename'
    A_NOTES = 'notes'
    A_ALIGN = 'align'
    A_IMAGE = 'image'
    A_IMAGE_HEIGHT = 'image_height'
    A_IMAGE_WIDTH = 'image_width'
    A_THUMBNAIL_NAME = 'thumbnail_name'
    A_THUMBNAIL_HEIGHT = 'thumbnail_height'
    A_THUMBNAIL_WIDTH = 'thumbnail_width'
    A_SIZE = 'size'
    A_CREATED_DATE = 'created_date'

    AA_ID = 'id'
    AA_ARTICLE_ID = 'article_id'
    AA_ATTACHMENT_ID = 'attachment_id'

    # SELECT variables
    SELECT = 'SELECT '
    FROM = 'FROM '
    WHERE = 'WHERE '
    AND = 'AND '

    SELECT_TABLES = TABLE_ATTACHMENT + ' a, ' + TABLE_ARTICLE_ATTACHMENT + ' b '

    SELECT_COLUMNS = 'a.' + A_ID + ', ' + A_FILENAME + ', ' + \
        A_ORIGINAL_FILENAME + ', ' + A_NOTES + ', ' + A_ALIGN + ', ' + A_IMAGE + ', ' + \
        A_IMAGE_HEIGHT + ', ' + A_IMAGE_WIDTH + ', ' + A_THUMBNAIL_NAME + ', ' + A_THUMBNAIL_HEIGHT + ', ' + \
        A_THUMBNAIL_WIDTH + ', ' + A_SIZE + ', ' + A_CREATED_DATE + ', b.' + AA_ID + ' article_attachment_id '

    WHERE_ARTICLE_ID = 'b.' + AA_ARTICLE_ID + ' = %s '
    WHERE_JOIN = 'a.' + A_ID + ' = ' + 'b.' + AA_ATTACHMENT_ID

    SELECT_BY_ARTICLE_ID = SELECT + SELECT_COLUMNS + FROM + \
        SELECT_TABLES + WHERE + WHERE_ARTICLE_ID + AND + \
        WHERE_JOIN

    # INSERT variables

    INSERT = 'INSERT '
    INTO = 'INTO '
    VALUES = 'VALUES'
    ON_DUPLICATE_KEY_UPDATE = 'ON DUPLICATE KEY UPDATE '

    ATTACHMENT_INSERT_COLUMNS = A_ID + ', ' + A_FILENAME + ', ' + \
        A_ORIGINAL_FILENAME + ', ' + A_NOTES + ', ' + A_ALIGN + ', ' + A_IMAGE + ', ' + \
        A_IMAGE_HEIGHT + ', ' + A_IMAGE_WIDTH + ', ' + A_THUMBNAIL_NAME + ', ' + A_THUMBNAIL_HEIGHT + ', ' + \
        A_THUMBNAIL_WIDTH + ', ' + A_SIZE + ', ' + A_CREATED_DATE

    INSERT_ATTACHMENT = INSERT + INTO + TABLE_ATTACHMENT + '(' + \
        ATTACHMENT_INSERT_COLUMNS + ') ' + VALUES + \
        '(%s, %s, %s, %s, %s, %s, %s, ' + \
        '%s, %s, %s, %s, %s, %s) ' + \
        ON_DUPLICATE_KEY_UPDATE + \
        A_FILENAME + '=' + VALUES + '(' + A_FILENAME + '), ' + \
        A_ORIGINAL_FILENAME + '=' + VALUES + '(' + A_ORIGINAL_FILENAME + '), ' + \
        A_NOTES + '=' + VALUES + '(' + A_NOTES + '), ' + \
        A_ALIGN + '=' + VALUES + '(' + A_ALIGN + '), ' + \
        A_IMAGE + '=' + VALUES + '(' + A_IMAGE + '), ' + \
        A_IMAGE_HEIGHT + '=' + VALUES + '(' + A_IMAGE_HEIGHT + '), ' + \
        A_IMAGE_WIDTH + '=' + VALUES + '(' + A_IMAGE_WIDTH + '), ' + \
        A_THUMBNAIL_NAME + '=' + VALUES + '(' + A_THUMBNAIL_NAME + '), ' + \
        A_THUMBNAIL_HEIGHT + '=' + VALUES + '(' + A_THUMBNAIL_HEIGHT + '), ' + \
        A_THUMBNAIL_WIDTH + '=' + VALUES + '(' + A_THUMBNAIL_WIDTH + '), ' + \
        A_SIZE + '=' + VALUES + '(' + A_SIZE + '), ' + \
        A_CREATED_DATE + '=' + VALUES + '(' + A_CREATED_DATE + ')'

    ARTICLE_ATTACHMENT_INSERT_COLUMNS = AA_ID + ', ' + AA_ARTICLE_ID + ', ' + AA_ATTACHMENT_ID

    INSERT_ARTICLE_ATTACHMENT = INSERT + INTO + TABLE_ARTICLE_ATTACHMENT + '(' + \
        ARTICLE_ATTACHMENT_INSERT_COLUMNS + ') ' + VALUES + \
        '(%s, %s, %s) ' + \
        ON_DUPLICATE_KEY_UPDATE + \
        AA_ARTICLE_ID + '=' + VALUES + '(' + AA_ARTICLE_ID + '), ' + \
        AA_ATTACHMENT_ID + '=' + VALUES + '(' + AA_ATTACHMENT_ID + ')'

    # DELETE variables

    DELETE = 'DELETE '

    WHERE_DELETE_ATTACHMENT = A_ID + ' = %s '
    WHERE_DELETE_ARTICLE = A_ID + ' in (' + SELECT + AA_ATTACHMENT_ID + ' ' + FROM + \
        TABLE_ARTICLE_ATTACHMENT + ' ' + WHERE + AA_ARTICLE_ID + ' = %s)'

    DELETE_ATTACHMENT_BY_ID = DELETE + FROM + TABLE_ATTACHMENT + ' ' + WHERE + WHERE_DELETE_ATTACHMENT
    DELETE_ATTACHMENT_BY_ARTICLE_ID = DELETE + FROM + TABLE_ATTACHMENT + ' ' + WHERE + WHERE_DELETE_ARTICLE

    # Utility variables
    applicationID = None

    def __init__(self, apID = None):
        AttachmentDao.__init__(self, apID)
        ConnectionAwareObject.__init__(self)
        if (apID is None):
            self.applicationID = APPLICATION.ID
        else:
            self.applicationID = apID
        self.__setUpQueries()

    def __setUpQueries(self):
        # Replace the table names with table_name_[site id number]
        self.SELECT_BY_ARTICLE_ID = self.SELECT_BY_ARTICLE_ID.replace('${ID}', str(self.applicationID))
        self.INSERT_ATTACHMENT = self.INSERT_ATTACHMENT.replace('${ID}', str(self.applicationID))
        self.INSERT_ARTICLE_ATTACHMENT = self.INSERT_ARTICLE_ATTACHMENT.replace('${ID}', str(self.applicationID))
        self.DELETE_ATTACHMENT_BY_ID = self.DELETE_ATTACHMENT_BY_ID.replace('${ID}', str(self.applicationID))
        self.DELETE_ATTACHMENT_BY_ARTICLE_ID = self.DELETE_ATTACHMENT_BY_ARTICLE_ID.replace('${ID}', str(self.applicationID))

    def fetchByArticleID(self, articleID):
        ''' Get the attachments for an article using the article id.

            returns a list of attachments; an empty list if no comments were found
        '''
        attachments = list()

        try:
            cursor = self.getCursor()
            select = self.SELECT_BY_ARTICLE_ID

            retval = cursor.execute(select, (articleID,))
            self.getConnection().commit()

            if (retval >= 1):
                for item in cursor.fetchall():
                    attachment = Attachment()
                    i = 0
                    attachment.id = item[i]; i += 1
                    attachment.filename = item[i]; i += 1
                    attachment.originalFilename = item[i]; i += 1
                    attachment.notes = item[i]; i += 1
                    attachment.align = item[i]; i += 1
                    attachment.image = (item[i] in TRUE); i += 1
                    attachment.imageHeight = item[i]; i += 1
                    attachment.imageWidth = item[i]; i += 1
                    attachment.thumbnailName = item[i]; i += 1
                    attachment.thumbnailHeight = item[i]; i += 1
                    attachment.thumbnailWidth = item[i]; i += 1
                    attachment.size = item[i]; i += 1
                    attachment.createdDate = item[i]; i += 1
                    attachment.articleAttachmentId = item[i]
                    attachments += [attachment]
        finally:
            self.releaseCursor()

        return attachments

    def write(self, articleID, attachment):
        ''' Inserts or updates an attachment given the articleID.

            returns a the id of the inserted/updated item or -1 if none was inserted
        '''
        if (articleID is None):
            raise DaoException('AttachmentDao.write() cannot get None for articleID')

        if (attachment.id <= 0):
            attachment.id = None
            attachment.articleAttachmentID = None
        try:
            queryValues = None
            try:
                cursor = self.getCursor()

                # Insert the attachment record
                self.lastSelect = self.INSERT_ATTACHMENT
                queryValues = (attachment.id,
                    attachment.filename,
                    attachment.originalFilename,
                    attachment.notes,
                    attachment.align,
                    toMySqlBoolean(attachment.image),
                    attachment.imageHeight,
                    attachment.imageWidth,
                    attachment.thumbnailName,
                    attachment.thumbnailHeight,
                    attachment.thumbnailWidth,
                    attachment.size,
                    toMySqlDateString(attachment.createdDate))
                numberInserted = cursor.execute(self.INSERT_ATTACHMENT, queryValues)
                self.getConnection().commit()
                if (numberInserted < 1):
                    raise DaoException('Did not get expected value (1 or 2) on ATTACHMENT insert: ' + str(numberInserted))
                attachmentID = cursor.lastrowid

                # Insert the article_attachment record
                queryValues = (attachment.articleAttachmentID,
                    articleID,
                    attachmentID)
                self.lastSelect = self.INSERT_ARTICLE_ATTACHMENT
                numberInserted = cursor.execute(self.INSERT_ARTICLE_ATTACHMENT, queryValues)
                self.getConnection().commit()
                if (numberInserted < 1):
                    raise DaoException('Did not get expected value (1 or 2) on ARTICLE_ATTACHMENT insert: ' + str(numberInserted))
                articleAttachmentID = cursor.lastrowid

                if (attachment.id is None):
                    attachment.id = attachmentID
                    attachment.articleAttachmentID = articleAttachmentID
            except Exception, e:
                msg = 'Exception in ArticleDaoImpl.write(): ' + str(e) + '\n ' + self.lastSelect + ' ' + str(queryValues)
                log(msg)
                raise DaoException(msg)
        finally:
            self.releaseCursor()

        return attachmentID

    def delete(self, attachment):
        ''' Deletes an attachment.

            returns true if an item was deleted
        '''
        deleted = False

        try:
            cursor = self.getCursor()
            numberDeleted = cursor.execute(self.DELETE_ATTACHMENT_BY_ID, (attachment.id,))
            self.getConnection().commit()

            deleted = (numberDeleted > 0)
        finally:
            self.releaseCursor()

        return deleted

    def deleteByArticleID(self, articleID):
        ''' Deletes all the attachments associated with an article.

            returns true if an item was deleted
        '''
        deleted = False

        try:
            cursor = self.getCursor()
            numberDeleted = cursor.execute(self.DELETE_ATTACHMENT_BY_ARTICLE_ID, (articleID,))
            self.getConnection().commit()

            deleted = (numberDeleted > 0)
        finally:
            self.releaseCursor()

        return deleted
