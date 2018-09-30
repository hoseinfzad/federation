import uuid

import pytest

from federation.entities.activitypub.entities import ActivitypubPost
from federation.entities.diaspora.entities import (
    DiasporaPost, DiasporaComment, DiasporaLike, DiasporaProfile, DiasporaRetraction,
    DiasporaContact, DiasporaReshare,
)
from federation.tests.factories.entities import ShareFactory
from federation.tests.fixtures.payloads import DIASPORA_PUBLIC_PAYLOAD

__all__ = ("diasporacomment", "diasporacontact", "diasporalike", "diasporapost", "diasporaprofile",
           "diasporareshare", "diasporaretraction", "diaspora_public_payload", "activitypubpost")


@pytest.fixture
def diaspora_public_payload():
    return DIASPORA_PUBLIC_PAYLOAD


@pytest.fixture
def diasporacomment():
    return DiasporaComment(
        raw_content="raw_content",
        signature="signature",
        id="guid",
        guid="guid",
        actor_id="alice@example.com",
        handle="alice@example.com",
        target_id="target_guid",
        target_guid="target_guid",
    )


@pytest.fixture
def diasporacontact():
    return DiasporaContact(
        actor_id="alice@example.com",
        handle="alice@example.com",
        target_id="bob@example.org",
        target_handle="bob@example.org",
        following=True,
    )


@pytest.fixture
def diasporalike():
    return DiasporaLike(
        id="guid",
        guid="guid",
        actor_id="alice@example.com",
        handle="alice@example.com",
        target_id="target_guid",
        target_guid="target_guid",
        signature="signature",
    )


@pytest.fixture
def activitypubpost():
    post_uuid = uuid.uuid4()
    profile_uuid = uuid.uuid4()
    return ActivitypubPost(
        raw_content="raw_content",
        public=True,
        provider_display_name="Socialhome",
        id=f"http://127.0.0.1:8000/post/{post_uuid}/",
        guid=post_uuid,
        actor_id=f"http://127.0.0.1:8000/profile/{profile_uuid}/",
        handle="alice@example.com",
    )

@pytest.fixture
def diasporapost():
    return DiasporaPost(
        raw_content="raw_content",
        public=True,
        provider_display_name="Socialhome",
        id="guid",
        guid="guid",
        actor_id="alice@example.com",
        handle="alice@example.com",
    )


@pytest.fixture
def diasporaprofile():
    return DiasporaProfile(
        raw_content="foobar", name="Bob Bobertson", public=True,
        tag_list=["socialfederation", "federation"], image_urls={
            "large": "urllarge", "medium": "urlmedium", "small": "urlsmall"
        },
        id="alice@example.com",
        handle="alice@example.com",
        guid="guid",
    )


@pytest.fixture
def diasporareshare():
    base_entity = ShareFactory()
    return DiasporaReshare.from_base(base_entity)


@pytest.fixture
def diasporaretraction():
    return DiasporaRetraction(
        actor_id="alice@example.com",
        handle="alice@example.com",
        target_id="target_guid",
        target_guid="target_guid",
        entity_type="Post",
    )
