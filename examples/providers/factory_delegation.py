"""`di.Factory` providers delegation example."""

import dependency_injector as di


class User(object):

    """Example class User."""

    def __init__(self, photos_factory):
        """Initializer.

        :param photos_factory: (di.Factory) -> Photo
        """
        self.photos_factory = photos_factory
        self._main_photo = None
        super(User, self).__init__()

    @property
    def main_photo(self):
        """Return user's main photo."""
        if not self._main_photo:
            self._main_photo = self.photos_factory()
        return self._main_photo


class Photo(object):

    """Example class Photo."""

# User and Photo factories:
photos_factory = di.Factory(Photo)
users_factory = di.Factory(User,
                           photos_factory=di.Delegate(photos_factory))

# Creating several User objects:
user1 = users_factory()
user2 = users_factory()

# Making some asserts:
assert isinstance(user1, User)
assert isinstance(user1.main_photo, Photo)

assert isinstance(user2, User)
assert isinstance(user2.main_photo, Photo)

assert user1 is not user2
assert user1.main_photo is not user2.main_photo
