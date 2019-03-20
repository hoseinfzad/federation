from unittest.mock import patch

from Crypto.PublicKey.RSA import RsaKey

from federation.entities.activitypub.constants import (
    CONTEXTS_DEFAULT, CONTEXT_MANUALLY_APPROVES_FOLLOWERS, CONTEXT_LD_SIGNATURES, CONTEXT_HASHTAG, CONTEXT_SENSITIVE)
from federation.entities.activitypub.entities import ActivitypubAccept
from federation.tests.fixtures.keys import PUBKEY
from federation.types import UserType


class TestEntitiesConvertToAS2:
    def test_accept_to_as2(self, activitypubaccept):
        result = activitypubaccept.to_as2()
        assert result == {
            "@context": CONTEXTS_DEFAULT,
            "id": "https://localhost/accept",
            "type": "Accept",
            "actor": "https://localhost/profile",
            "object": "https://example.com/follow/1234",
        }

    def test_post_to_as2(self, activitypubpost):
        # TODO expand
        result = activitypubpost.to_as2()
        assert result.get('@context') == CONTEXTS_DEFAULT + [
            CONTEXT_HASHTAG,
            CONTEXT_SENSITIVE,
        ]
        assert result.get('type') == 'Note'

    def test_profile_to_as2(self, activitypubprofile):
        result = activitypubprofile.to_as2()
        assert result == {
            "@context": CONTEXTS_DEFAULT + [
                CONTEXT_LD_SIGNATURES,
                CONTEXT_MANUALLY_APPROVES_FOLLOWERS,
            ],
            "endpoints": {
                "sharedInbox": "https://example.com/public",
            },
            "followers": "https://example.com/bob/followers/",
            "following": "https://example.com/bob/following/",
            "id": "https://example.com/bob",
            "inbox": "https://example.com/bob/private",
            "manuallyApprovesFollowers": False,
            "name": "Bob Bobertson",
            "outbox": "https://example.com/bob/outbox/",
            "publicKey": {
                "id": "https://example.com/bob#main-key",
                "owner": "https://example.com/bob",
                "publicKeyPem": PUBKEY,
            },
            "type": "Person",
            "url": "https://example.com/bob-bobertson",
            "summary": "foobar",
            "icon": "urllarge",
        }


class TestEntitiesPostReceive:
    @patch("federation.utils.activitypub.retrieve_and_parse_profile", autospec=True)
    @patch("federation.entities.activitypub.entities.handle_send", autospec=True)
    def test_follow_post_receive__sends_correct_accept_back(
            self, mock_send, mock_retrieve, activitypubfollow, profile
    ):
        mock_retrieve.return_value = profile
        activitypubfollow.post_receive()
        args, kwargs = mock_send.call_args_list[0]
        assert isinstance(args[0], ActivitypubAccept)
        assert args[0].activity_id.startswith("https://example.com/profile#accept-")
        assert args[0].actor_id == "https://example.com/profile"
        assert args[0].target_id == "https://localhost/follow"
        assert isinstance(args[1], UserType)
        assert args[1].id == "https://example.com/profile"
        assert isinstance(args[1].private_key, RsaKey)
        assert kwargs['recipients'] == [{
            "fid": "https://example.com/bob/private",
            "protocol": "activitypub",
            "public": False,
        }]
