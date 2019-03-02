import json
import logging
import re
from typing import Union, Callable, Tuple

from federation.entities.activitypub.enums import ActorType
from federation.types import UserType
from federation.utils.text import decode_if_bytes

logger = logging.getLogger('federation')

PROTOCOL_NAME = "activitypub"


def identify_id(id: str) -> bool:
    """
    Try to identify whether this is an ActivityPub ID.
    """
    return re.match(r'^https?://', id, flags=re.IGNORECASE) is not None


def identify_payload(payload: Union[str, bytes]) -> bool:
    """
    Try to identify whether this is an ActivityPub payload.
    """
    try:
        data = json.loads(decode_if_bytes(payload))
        if "@context" in data:
            return True
    except Exception:
        pass
    return False


class Protocol:
    def extract_actor(self):
        if self.payload.get('type') in ActorType.values():
            self.actor = self.payload.get('id')
        else:
            self.actor = self.payload.get('actor')

    def receive(self, payload: str, user: UserType=None, sender_key_fetcher: Callable[[str], str]=None,
            skip_author_verification: bool=False) -> Tuple[str, dict]:
        """
        Receive a payload.

        For testing purposes, `skip_author_verification` can be passed. Authorship will not be verified.
        """
        self.user = user
        self.get_contact_key = sender_key_fetcher
        self.payload = json.loads(decode_if_bytes(payload))
        self.extract_actor()
        # Verify the message is from who it claims to be
        if not skip_author_verification:
            self.verify_signature()
        return self.actor, self.payload

    def verify_signature(self):
        # TODO implement
        pass
