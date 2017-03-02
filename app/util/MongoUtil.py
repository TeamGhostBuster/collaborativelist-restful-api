from copy import deepcopy

from bson.objectid import ObjectId
from flask_mongoengine import DoesNotExist
from flask_mongoengine import ValidationError

from app.api.article.model import Article
from app.api.comment.model import Comment
from app.api.group.model import Group
from app.api.list.model import List
from app.api.user.model import User
from app.api.vote.model import Vote


def find_user(email):
    # Find the existed user by email
    try:
        user = User.objects.get(email__exact=email)

    except DoesNotExist:
        # The user does not exist
        return None

    return user


def create_user(email, first_name, last_name):
    # Create new user
    new_user = User(email=email, first_name=first_name, last_name=last_name).save()

    return new_user


def find_list(list_id):
    try:
        # Find user's list
        user_list = List.objects.get(id=ObjectId(list_id))
    except DoesNotExist:
        pass

    return user_list


def archive_list(user, list_id):
    try:
        # Get the list
        archived_list = List.objects.get(id=ObjectId(list_id))
        User.objects.get(id=user.id, lists=archived_list)
    except DoesNotExist as e:
        return None

    # Mark it as archived
    List.objects(id=archived_list.id).update_one(archived=True)

    user.reload()

    return user


def retrieve_list(user, list_id):
    try:
        retrieved_list = List.objects.get(id=ObjectId(list_id))
        User.objects.get(id=user.id, lists=retrieved_list)
    except DoesNotExist:
        return None

    # Mark it as not archived
    List.objects(id=retrieved_list.id).update_one(archived=False)

    user.reload()

    return user


def archive_group_list(group_id, list_id):
    try:
        # Check if list exists
        archived_list = List.objects.get(id=ObjectId(list_id))
        # Check if the list belongs to the group
        group = Group.objects.get(id=ObjectId(group_id), lists=archived_list)
    except DoesNotExist:
        return None

    List.objects(id=archived_list.id).update_one(archived=True)

    return group


def retrieve_group_list(group_id, list_id):
    try:
        # Check if list exists
        retrieved_list = List.objects.get(id=ObjectId(list_id))
        # Check if the list belongs to the group
        group = Group.objects.get(id=ObjectId(group_id), lists=retrieved_list)
    except DoesNotExist:
        return None

    List.objects(id=retrieved_list.id).update_one(archived=False)

    return group


# def get_user_all_lists(user):
#     # user = User.objects.get(id=user.id, lists__)
#     pipeline = [
#         {'$match': {'email': 'michaellam.lzc@gmail.com'}},
#         {'$unwind': '$lists'},
#         {'$lookup': {
#             'from': 'list',
#             'localField': 'lists',
#             'foreignField': '_id',
#             'as': 'listObj'
#         }},
#         {'$unwind': '$listObj'},
#         {'$match': {'listObj.archived': {'$ne': 'true'}}},
#         {'$group': {'_id': '$_id',
#                     'email': {'$first': '$email'},
#                     'last_name': {'$first': '$last_name'},
#                     'first_name': {'$first': 'first_name'},
#                     'lists': {'$push': '$lists'}}}
#     ]
#     pass


def create_list(list_name, user):
    # Create new list
    new_list = List(name=list_name).save()

    # Append list reference to the user's lists list
    User.objects(id=user.id).update_one(push__lists=new_list)

    return new_list


def create_article(data, list_id):
    try:
        # Check if list exists
        List.objects.get(id=ObjectId(list_id))
        # Create new article
        new_article = Article(**data).save()
    except Exception as e:
        return type(e).__name__

    # Append article reference to the user's article lists
    List.objects(id=list_id).update_one(push__articles=new_article)

    return new_article


def update_article(data, article_id):
    try:
        # Check if the article exists
        article = Article.objects.get(id=ObjectId(article_id))
        # Update article
        Article.objects(id=ObjectId(article_id)).update_one(**data)
    except Exception as e:
        return type(e).__name__
    # Article.objects(id=ObjectId(article_id)).update_one(**data)
    article.reload()
    return article


def create_article_in_group(title, list_id, group_id, description, url=None, tags=None):
    try:
        # Check if the list exist
        the_list = List.objects.get(id=ObjectId(list_id))
        # Check if the list belongs to the group
        the_group = Group.objects.get(id=ObjectId(group_id), lists=the_list)
    except DoesNotExist:
        return None

    # create new article
    new_article = create_article(title, list_id, description, url, tags)

    return new_article


def find_article(article_id):
    # Find the article
    try:
        article = Article.objects.get(id=ObjectId(article_id))

    except DoesNotExist:
        return None

    return article


def add_article_to_list(list_id, article_id):
    # Find the article
    try:
        article = find_article(article_id)
    except DoesNotExist:
        return None

    # Find the list
    try:
        reading_list = find_list(list_id)
    except DoesNotExist:
        return None

    # Add the article to the list
    List.objects(id=ObjectId(list_id)).update_one(push__articles=article)
    reading_list.reload()

    return reading_list


def add_tag(article_id, tag):
    try:
        article = Article.objects.get(id=ObjectId(article_id))
    except DoesNotExist:
        return None

    # Add tag to article
    Article.objects(id=article.id).update_one(push__tags=tag)
    article.reload()

    return article


def delete_article(user, list_id, article_id):
    # Retrieve the articled and list to be deleted
    try:
        the_list = List.objects.get(id=ObjectId(list_id))
        the_article = Article.objects.get(id=ObjectId(article_id))
    except DoesNotExist:
        return None

    # Check if user has permission to the list
    if the_list not in user.lists:
        return None

    # Check if the article exists in the list
    if the_article not in the_list.articles:
        return None

    # Remove the article from the list
    List.objects(id=the_list.id).update_one(pull__articles=the_article)

    the_list.reload()

    return the_list


def add_comment(user, article_id, comment, public=True):
    # Check if the article exists
    if find_article(article_id) is None:
        return None

    # Post comment
    new_comment = Comment(content=comment, article=article_id, public=public,
                          user=user).save()

    return new_comment


def create_group(group_name, moderator, members=None, description=None):
    # Create group
    new_group = Group(name=group_name, moderator=moderator, description=description).save()

    # Add moderator to members
    Group.objects(id=new_group.id).update_one(push__members=moderator)

    # Add members if not null
    if members is not None:
        for id in members:
            try:
                member = User.objects.get(id=ObjectId(id))
                Group.objects(id=new_group.id).update_one(push__members=member)
            except DoesNotExist:
                return None

    new_group.reload()
    return new_group


def find_group(group_id):
    try:
        # Find group
        reading_group = Group.objects.get(id=ObjectId(group_id))
    except DoesNotExist:
        return None
    return reading_group


def add_group_member(group_id, member_id):
    # Find the group
    try:
        reading_group = find_group(group_id)
    except DoesNotExist:
        return None

    # Check that new member exists
    try:
        new_member = User.objects.get(id=ObjectId(member_id))
    except DoesNotExist:
        return None

    # Add group member
    Group.objects(id=ObjectId(group_id)).update_one(push__members=new_member)
    reading_group.reload()

    return reading_group


def create_group_list(user, list_name, group_id):
    # Check if user has permission
    # Create list
    new_list = List(name=list_name).save()

    # Append list reference to the group's list of lists
    try:
        Group.objects(id=ObjectId(group_id)).update_one(push__lists=new_list)
    except DoesNotExist:
        return None
    return new_list


def get_user_groups(user):
    groups = Group.objects(members=user)

    if Group.objects(members=user).count() == 0:
        return None

    return groups


def get_group_lists(user, group_id):
    try:
        # Get group
        group = Group.objects.get(id=ObjectId(group_id), members=user)
    except DoesNotExist:
        return None

    return group


def check_user_in_group(user, group_id):
    try:
        # Check if user belongs to the group
        Group.objects.get(id=ObjectId(group_id), members=user)
    except DoesNotExist:
        return None

    return 0


def share_list_to_group(user, list_id, group_id):
    try:
        # Check if the list exist
        the_list = List.objects.get(id=ObjectId(list_id))
        # Check if user has permission to the list or not
        User.objects.get(id=user.id, lists=the_list)
    except DoesNotExist:
        return None

    duplicate_list = deepcopy(the_list)
    duplicate_list.id = None
    duplicate_list.save()
    Group.objects(id=ObjectId(group_id)).update_one(push__lists=duplicate_list)
    return duplicate_list


def create_vote_object(list_id, article_id):
    try:
        reading_list = find_list(list_id)
        article = find_article(article_id)
    except DoesNotExist:
        return None

    new_vote_object = Vote(article=article, list=reading_list).save()
    return new_vote_object


def find_vote(vote_id):
    try:
        vote_object = Vote.objects.get(id=ObjectId(vote_id))
    except DoesNotExist:
        return None
    return vote_object


def add_vote(vote_id, upvote, voter):
    # Find the vote object
    try:
        vote_object = find_vote(vote_id)
    except DoesNotExist:
        return None

    # Add record of user voting/check if user has already voted
    try:
        Vote.objects.get(id=ObjectId(vote_id), voter_list=voter)
    except DoesNotExist:
        Vote.objects(id=ObjectId(vote_id)).update_one(push__voter_list=voter)

        if upvote:
            # Increment in up vote
            Vote.objects(id=ObjectId(vote_id)).update_one(inc__vote_count=1)
        else:
            # decrement if down vote
            Vote.objects(id=ObjectId(vote_id)).update_one(dec__vote_count=1)

    vote_object.reload()
    return vote_object