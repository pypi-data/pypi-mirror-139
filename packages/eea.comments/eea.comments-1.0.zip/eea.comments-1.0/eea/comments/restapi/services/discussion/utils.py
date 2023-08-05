"""Utils"""
from AccessControl import getSecurityManager
from Acquisition import aq_inner
from zope.component import queryUtility
from zope.security.interfaces import IPermission


def permission_exists(permission_id):
    """Returns permission value if exists
    """
    permission = queryUtility(IPermission, permission_id)
    return permission is not None


def can_view(context):
    """Returns true if current user has the 'View comments'
    permission.
    """
    return bool(getSecurityManager().checkPermission("View comments", context))


def can_reply(comment):
    """Returns true if current user has the 'Reply to item'
    permission.
    """
    return bool(
        getSecurityManager().checkPermission(
            "Reply to item", aq_inner(comment)
        )
    )
