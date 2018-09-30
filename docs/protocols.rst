Protocols
=========

Currently two protocols are being focused on. Diaspora is considered in relatively stable status with most of the protocol implemented. ActivityPub support is work in progress.

For example implementations in real life projects check :ref:`example-projects`.

.. _diaspora:

Diaspora
--------

This library only supports the `current renewed version <http://diaspora.github.io/diaspora_federation/>`_ of the protocol. Compatibility for the legacy version was dropped in version 0.18.0.

The feature set supported is the following:

* Webfinger, hCard and other discovery documents
* NodeInfo 1.0 documents
* Social-Relay documents
* Magic envelopes, signatures and other transport method related necessities
* Entities as follows:

   * Comment
   * Like
   * Photo
   * Profile
   * Retraction
   * StatusMessage
   * Contact
   * Reshare

.. _activitypub:

ActivityPub
-----------

Features currently supported:

* Webfinger
* Entities as follows:

   * Profile
   * Post
