from .article import controller as article_api
from .library import controller as library_api
from .list import controller as list_api
from .user import controller as user_api
from .group import controller as group_api
from .comment import controller as comment_api
from .article import model as article_model
from .library import model as library_model
from .list import model as list_model
from .user import model as user_model
from .group import model as group_model
from .comment import model as comment_model

# APIDOC Inherit Doc


"""
@apiDefine AuthorizationTokenHeader
@apiHeader {String} Access-Token Access token obtains from Oauth2 provider.
@apiHeader {String} Provider-Name Oauth2 provider name.
@apiHeaderExample {json} Header (Example):
    {
        "Access-Token": "12xsdklajlkadsf",
        "Provider-Name": "Google"
    }
"""

"""
@apiDefine UnauthorizedAccessError
@apiError UnauthorizedAccessError User's access token is not valid
@apiErrorExample Error 401
    {
        "msg": "Unauthorized access"
    }
"""

"""
@apiDefine ListDoesNotExist
apiError ListDoesNotExist The list does not exist
@apiErrorExample Error 400
    {
        "msg": "List does not exist"
    }
"""

"""
@apiDefine ArticleDoesNotExist
apiError ArticleDoesNotExist The article does not exist
@apiErrorExample Error 400
    {
        "msg": "Article does not exist"
    }
"""

"""
@apiDefine InvalidObjectID
apiError ArticleDoesNotExist The article does not exist
@apiErrorExample Error 400
    {
        "msg": "ObjectID is not valid"
    }
"""