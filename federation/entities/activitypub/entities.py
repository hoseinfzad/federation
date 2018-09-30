from typing import Dict

from federation.entities.activitypub.constants import (
    CONTEXTS_DEFAULT, CONTEXT_MANUALLY_APPROVES_FOLLOWERS, CONTEXT_SENSITIVE, CONTEXT_HASHTAG,
    CONTEXT_LD_SIGNATURES)
from federation.entities.activitypub.enums import ActorType, ObjectType
from federation.entities.activitypub.mixins import ActivitypubEntityMixin
from federation.entities.base import Profile, Post
from federation.utils.text import with_slash


class ActivitypubPost(ActivitypubEntityMixin, Post):
    _type = ObjectType.NOTE.value

    def to_as2(self) -> Dict:
        # TODO add in sending phase:
        # - to
        # - cc
        # - bcc
        as2 = {
            "@context": CONTEXTS_DEFAULT + [
                CONTEXT_HASHTAG,
                CONTEXT_SENSITIVE,
            ],
            "attributedTo": self.actor_id,
            "content": self.raw_content,  # TODO render to html, add source markdown
            "id": self.id,
            "inReplyTo": None,
            "published": self.created_at.isoformat(),
            "sensitive": True if "nsfw" in self.tags else False,
            "summary": None,  # TODO Short text? First sentence? First line?
            "tag": [],  # TODO add tags
            "type": self._type,
            "url": self.url,
        }
        return as2


class ActivitypubProfile(ActivitypubEntityMixin, Profile):
    _type = ActorType.PERSON.value

    def to_as2(self) -> Dict:
        as2 = {
            "@context": CONTEXTS_DEFAULT + [
                CONTEXT_LD_SIGNATURES,
                CONTEXT_MANUALLY_APPROVES_FOLLOWERS,
            ],
            "type": self._type,
            "name": self.name,
            "url": self.url,
            "id": self.id,
            "inbox": f"{with_slash(self.id)}inbox/",
            "outbox": f"{with_slash(self.id)}outbox/",
            "manuallyApprovesFollowers": False,
            "publicKey": {
                "id": f"{self.id}#main-key",
                "owner": self.id,
                "publicKeyPem": self.public_key,
            },
            "endpoints": {
                "sharedInbox": f"{with_slash(self.base_url)}ap/inbox/",  # TODO just get from config
            },
        }
        if self.username:
            as2['preferredUsername'] = self.username
        if self.raw_content:
            as2['summary'] = self.raw_content
        if self.image_urls.get('large'):
            as2['icon'] = self.image_urls.get('large')
        return as2
