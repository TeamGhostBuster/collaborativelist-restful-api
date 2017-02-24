from app.util import JsonUtil
from app.util import MongoUtil
from app.util import RequestUtil
from app.util.AuthUtil import *


@app.route('/user/list/<string:list_id>', methods=['GET'])
@authorized_required
def get_articles_from_list(user, list_id):
    """
    @api {get} /user/list/:id Get articles of a list
    @apiName Get articles of a list
    @apiGroup List

    @apiUse AuthorizationTokenHeader

    @apiParam {String} id List unique ID.

    @apiSuccess {String} List id.
    @apiSuccess {String} List name.
    @apiSuccess {Object[]} articles Articles data.
    @apiSuccess {String} articles.id Article id.
    @apiSuccess {String} article.title Article title.
    @apiSuccessExample {json} Response (Example):
        {
            "id": "31ladsjfl",
            "name": "CMPUT 391 Seminar",
            "articles": [
                {
                    "id": "adlfajdls",
                    "title": "Process"
                }
            ]
        }

    @apiUse UnauthorizedAccessError
    """
    app.logger.info('User {} Access {}'.format(user, request.full_path))

    reading_list = MongoUtil.find_list(list_id)
    # check for bad list
    if reading_list is None:
        return jsonify(msg='List does not exist'), 404

    # convert the articles into json format
    return jsonify(JsonUtil.serialize(reading_list)), 200


@app.route('/user/list', methods=['POST'])
@authorized_required
def create_list(user):
    """
    @api {post} /user/list Create a reading list
    @apiName Create a reading list
    @apiGroup List

    @apiUse AuthorizationTokenHeader

    @apiParam {String} name List name.
    @apiParamExample {json} Request (Example)
        {
            "name": "CMPUT495 Seminar"
        }

    @apiUse UnauthorizedAccessError
    """
    app.logger.info('User {} Access {}'.format(user, request.full_path))

    # Get list name from api parameter
    req = RequestUtil.get_request()
    list_name = req['name']

    # If missing parameter
    if list_name is None:
        return 'Bad request', 400

    # Create a new list
    new_list = MongoUtil.create_list(list_name, user)

    app.logger.info('User {} Create list'.format(user, new_list))

    return jsonify(JsonUtil.serialize(new_list)), 200


@app.route('/user/list/<string:list_id>/article/<string:article_id>', methods=['DELETE'])
@authorized_required
def delete_article(user, list_id, article_id):
    """
    @api {delete} /user/list/:list_id/article/:article_id Delete an article
    @apiName Delete an article from a list
    @apiGroup List

    @apiUse AuthorizationTokenHeader

    @apiParam {String} list_id The list id.
    @apiParam {String} article_id The article id.

    @apiSuccess {JSON} List the new list in json string.

    @apiUse UnauthorizedAccessError
    @apiUse ListDoesNotExist
    @apiUse ArticleDoesNotExist
    """
    app.logger.info('User {} Access {}'.format(user, request.full_path))

    # Delete the article from the list
    the_list = MongoUtil.delete_article(user, list_id, article_id)

    if the_list is None:
        return jsonify(msg='List/Article does not exists'), 400

    app.logger.info('User {} Delete article {} From list {}'.format(user, article_id, list_id))

    return jsonify(JsonUtil.serialize(the_list)), 200


@app.route('/user/list/<string:list_id>/archive', methods=['DELETE'])
@authorized_required
def archive_list(user, list_id):
    """
    @api {delete} /user/list/:id/archive Archive a list
    @apiName Archive a list
    @apiGroup List

    @apiUse AuthorizationTokenHeader

    @apiParam {String} list_id The list id.

    @apiSuccess {String} id User id
    @apiSuccess {Object[]} lists Lists data
    @apiSuccess {String} lists.id List id
    @apiSuccess {Boolean} lists.archived Archived list or not
    @apiSuccess {String} lists.name List name
    @apiSuccessExample {json} Response (Example):
        {
            "id": "31ladsjfl",
            "lists": [
                {
                    "id": "adlfajdls",
                    "archived": "True",
                    "name": "Process"
                }
            ]
        }

    @apiUse UnauthorizedAccessError
    @apiUse ListDoesNotExist
    """
    app.logger.info('User {} Access {}'.format(user, request.full_path))

    user = MongoUtil.archive_list(user, list_id)

    # If the list do
    if user is None:
        return jsonify(msg='List does not exist'), 400

    return jsonify(JsonUtil.serialize(user))


@app.route('/user/list/<string:list_id>/retrieve', methods=['PUT'])
@authorized_required
def retrieve_list(user, list_id):
    """
    @api {put} /user/list/:id/retrieve Retrieve a list
    @apiName Retrieve a list
    @apiGroup List

    @apiUse AuthorizationTokenHeader

    @apiParam {String} id The list id.

    @apiSuccess {String} id User id
    @apiSuccess {Object[]} lists Lists data
    @apiSuccess {String} lists.id List id
    @apiSuccess {Boolean} lists.archived Archived list or not
    @apiSuccess {String} lists.name List name
    @apiSuccessExample {json} Response (Example):
        {
            "id": "31ladsjfl",
            "lists": [
                {
                    "id": "adlfajdls",
                    "archived": "False",
                    "name": "Process"
                }
            ]
        }

    @apiUse UnauthorizedAccessError
    @apiUse ListDoesNotExist
    """
    app.logger.info('User {} Access {}'.format(user, request.full_path))

    user = MongoUtil.retrieve_list(user, list_id)

    # If the list do
    if user is None:
        return jsonify(msg='List does not exist'), 400

    app.logger.info('User {} Retrieve List ID: {}'.format(user, list_id))

    return jsonify(JsonUtil.serialize(user))


@app.route('/user/lists', methods=['GET'])
@authorized_required
def get_user_reading_lists(user):
    """
    @api {get} /user/lists Get user all reading lists
    @apiName Get user reading lists
    @apiGroup List

    @apiUse AuthorizationTokenHeader

    @apiSuccess {String} id User id
    @apiSuccess {Object[]} lists Lists data
    @apiSuccess {String} lists.id List id
    @apiSuccess {Boolean} lists.archived Archived list or not
    @apiSuccess {String} lists.name List name
    @apiSuccessExample {json} Response (Example):
        {
            "id": "31ladsjfl",
            "lists": [
                {
                    "id": "adlfajdls",
                    "archived": "True",
                    "name": "Process"
                }
            ]
        }

    @apiUse UnauthorizedAccessError
    """
    app.logger.info('User: {} Access: {}'.format(user, request.full_path))
    app.logger.info('User {} Get all reading lists'.format(user))

    return jsonify(JsonUtil.serialize(user)), 200


@app.route('/group/list', methods=['POST'])
@group_read_permission_required
def create_group_list(user):
    """
    @api {post} /group/list Create a group reading list
    @apiName Create a group reading list
    @apiGroup List

    @apiUse AuthorizationTokenHeader

    @apiParam {String} name List name.
    @apiParam {String} group_id Group ID.
    @apiParamExample {json} Request (Example)
        {
            "name": "CMPUT495 Seminar"
            "group_id": "834jlkkasd9"
        }

    @apiUse GroupAccessDenied
    """
    # Get list name from api parameter
    app.logger.info('User {} Access {}'.format(user, request.full_path))

    req = RequestUtil.get_request()
    list_name = req['name']
    group_id = req['group_id']

    # If missing parameter
    if list_name is None:
        return 'Bad request', 400

    # Create a new list
    new_list = MongoUtil.create_group_list(user, list_name, group_id)
    if new_list is None:
        return jsonify(msg='Bad Request.'), 200

    app.logger.info('User {} Create list'.format(group_id, new_list))

    return jsonify(JsonUtil.serialize(new_list)), 200


@app.route('/group/<string:group_id>/lists', methods=['GET'])
@authorized_required
def get_group_lists(user, group_id):
    """
    @api {get} /group/:id/lists Get group reading lists
    @apiName Get group reading lists
    @apiGroup List

    @apiUse AuthorizationTokenHeader

    @apiSuccess {String} id Group id
    @apiSuccess {Object[]} lists Lists data
    @apiSuccess {String} lists.id List id
    @apiSuccess {Boolean} lists.archived Archived list or not
    @apiSuccess {String} lists.name List name
    @apiSuccessExample {json} Response (Example):
        {
            "id": "31ladsjfl",
            "lists": [
                {
                    "id": "adlfajdls",
                    "archived": "True",
                    "name": "Process"
                }
            ]
        }

    @apiUse GroupDoesNotExist
    @apiUse UnauthorizedAccessError
    """
    app.logger.info('User {} Access {}'.format(user, request.full_path))

    # Get group list
    group = MongoUtil.get_group_lists(user, group_id)

    if group is None:
        return jsonify(msg='Group does not exist')

    app.logger.info('User {} Get group ID: {} lists'.format(user, group_id))
    return jsonify(JsonUtil.serialize(group, only=('id', 'name', 'description', 'lists')))


@app.route('/user/list/<string:list_id>/articles', methods=['POST'])
@authorized_required
def add_article_to_user_list(user, list_id):
    """
    @api {post} /user/list/:id/articles Add article to a user's list
    @apiName Copy article to user list
    @apiGroup List

    @apiUse AuthorizationTokenHeader

    @apiParam {String} article_id: Article id.
    @apiParamExample {json} Request (Example)
        {
            "article_id": "834jlkkasd9"
        }

    @apiUse UnauthorizedAccessError
    """
    app.logger.info('User {} Access {}'.format(user, request.full_path))

    # Get parameters
    req = RequestUtil.get_request()
    article_id = req['article_id']

    reading_list = MongoUtil.add_article_to_list(list_id, article_id)

    # Check for valid request
    if reading_list is None:
        return jsonify(msg="Bad request."), 400

    app.logger.info("User {} add article {} to list {}".format(user, article_id, list_id))

    return jsonify(JsonUtil.serialize(reading_list)), 200


@app.route('/group/list/<string:list_id>/articles', methods=['POST'])
@group_read_permission_required
def add_article_to_group_list(user, list_id):
    """
    @api {post} /group/list/:id/articles Add article to a group's list
    @apiName Copy article to group list
    @apiGroup List

    @apiUse AuthorizationTokenHeader

    @apiParam {String} id: Article id.
    @apiParamExample {json} Request (Example)
        {
            "article_id": "834jlkkasd9"
        }

    @apiUse GroupAccessDenied
    """
    app.logger.info('User {} Access {}'.format(user, request.full_path))

    # Get parameters
    req = RequestUtil.get_request()
    article_id = req['article']

    reading_list = MongoUtil.add_article_to_list(list_id, article_id)
    new_vote_object = MongoUtil.create_vote_object(list_id, article_id)

    # Check for valid request
    if (reading_list or new_vote_object) is None:
        return jsonify(msg="Bad request."), 400

    app.logger.info("User {} add article {} to list {}".format(user, article_id, list_id))
    app.logger.info("User {} created new vote object".format(user))

    return jsonify(JsonUtil.serialize(reading_list)), 200
