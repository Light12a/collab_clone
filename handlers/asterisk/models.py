# coding: utf-8
from sqlalchemy import (
   Column, DECIMAL,
   DateTime, Enum,
   Float, ForeignKey,
   Index, String,
   Table, Text, text
)
from sqlalchemy.dialects.mysql import BIGINT, INTEGER
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Extension(Base):
   __tablename__ = 'extensions'
   __table_args__ = (
       Index('context', 'context', 'exten', 'priority', unique=True),
   )

   id = Column(BIGINT(20), primary_key=True, unique=True)
   context = Column(String(40), nullable=False)
   exten = Column(String(40), nullable=False)
   priority = Column(INTEGER(11), nullable=False)
   app = Column(String(40), nullable=False)
   appdata = Column(String(256), nullable=False)


class Musiconhold(Base):
   __tablename__ = 'musiconhold'

   name = Column(String(80), primary_key=True)
   mode = Column(Enum(u'custom', u'files', u'mp3nb',
                      u'quietmp3nb', u'quietmp3', u'playlist'))
   directory = Column(String(255))
   application = Column(String(255))
   digit = Column(String(1))
   sort = Column(String(10))
   format = Column(String(10))
   stamp = Column(DateTime)


class PsAuth(Base):
   __tablename__ = 'ps_auths'

   id = Column(String(40), nullable=False, unique=True)
   auth_type = Column(Enum(u'md5', u'userpass', u'google_oauth'))
   nonce_lifetime = Column(INTEGER(11))
   md5_cred = Column(String(40))
   password = Column(String(80))
   realm = Column(String(40))
   username = Column(String(40))
   refresh_token = Column(String(255))
   oauth_clientid = Column(String(255))
   oauth_secret = Column(String(255))


class PsEndpoint(Base):
   __tablename__ = 'ps_endpoints'

   abcde = Column(String(40), primary_key=True)
   transport = Column(String(40))
   aors = Column(String(200))
   auth = Column(String(40))
   context = Column(String(40))
   disallow = Column(String(200))
   allow = Column(String(200))
   direct_media = Column(Enum('yes', 'no'))
   connected_line_method = Column(Enum('invite', 'reinvite', 'update'))
   direct_media_method = Column(Enum('invite', 'reinvite', 'update'))
   direct_media_glare_mitigation = Column(Enum('none', 'outgoing', 'incoming'))
   disable_direct_media_on_nat = Column(Enum('yes', 'no'))
   dtmf_mode = Column(Enum('rfc4733', 'inband', 'info', 'auto', 'auto_info'))
   external_media_address = Column(String(40))
   force_rport = Column(Enum('yes', 'no'))
   ice_support = Column(Enum('yes', 'no'))
   identify_by = Column(String(80))
   mailboxes = Column(String(40))
   moh_suggest = Column(String(40))
   outbound_auth = Column(String(40))
   outbound_proxy = Column(String(40))
   rewrite_contact = Column(Enum('yes', 'no'))
   rtp_ipv6 = Column(Enum('yes', 'no'))
   rtp_symmetric = Column(Enum('yes', 'no'))
   send_diversion = Column(Enum('yes', 'no'))
   send_pai = Column(Enum('yes', 'no'))
   send_rpid = Column(Enum('yes', 'no'))
   timers_min_se = Column(INTEGER(11))
   timers = Column(Enum('forced', 'no', 'required', 'yes'))
   timers_sess_expires = Column(INTEGER(11))
   callerid = Column(String(40))
   callerid_privacy = Column(Enum('allowed_not_screened',
                                  'allowed_passed_screened',
                                  'allowed_failed_screened',
                                  'allowed', 'prohib_not_screened',
                                  'prohib_passed_screened',
                                  'prohib_failed_screened',
                                  'prohib', 'unavailable'))
   callerid_tag = Column(String(40))
   _100rel = Column('100rel', Enum('no', 'required', 'yes'))
   aggregate_mwi = Column(Enum('yes', 'no'))
   trust_id_inbound = Column(Enum('yes', 'no'))
   trust_id_outbound = Column(Enum('yes', 'no'))
   use_ptime = Column(Enum('yes', 'no'))
   use_avpf = Column(Enum('yes', 'no'))
   media_encryption = Column(Enum('no', 'sdes', 'dtls'))
   inband_progress = Column(Enum('yes', 'no'))
   call_group = Column(String(40))
   pickup_group = Column(String(40))
   named_call_group = Column(String(40))
   named_pickup_group = Column(String(40))
   device_state_busy_at = Column(INTEGER(11), comment='hallu')
   fax_detect = Column(Enum('yes', 'no'))
   t38_udptl = Column(Enum('yes', 'no'))
   t38_udptl_ec = Column(Enum('none', 'fec', 'redundancy'))
   t38_udptl_maxdatagram = Column(INTEGER(11))
   t38_udptl_nat = Column(Enum('yes', 'no'))
   t38_udptl_ipv6 = Column(Enum('yes', 'no'))
   tone_zone = Column(String(40))
   language = Column(String(40))
   one_touch_recording = Column(Enum('yes', 'no'))
   record_on_feature = Column(String(40))
   record_off_feature = Column(String(40))
   rtp_engine = Column(String(40))
   allow_transfer = Column(Enum('yes', 'no'))
   allow_subscribe = Column(Enum('yes', 'no'))
   sdp_owner = Column(String(40))
   sdp_session = Column(String(40))
   tos_audio = Column(String(10))
   tos_video = Column(String(10))
   sub_min_expiry = Column(INTEGER(11))
   from_domain = Column(String(40))
   from_user = Column(String(40))
   mwi_from_user = Column(String(40))
   dtls_verify = Column(String(40))
   dtls_rekey = Column(String(40))
   dtls_cert_file = Column(String(200))
   dtls_private_key = Column(String(200))
   dtls_cipher = Column(String(200))
   dtls_ca_file = Column(String(200))
   dtls_ca_path = Column(String(200))
   dtls_setup = Column(Enum('active', 'passive', 'actpass'))
   srtp_tag_32 = Column(Enum('yes', 'no'))
   media_address = Column(String(40))
   redirect_method = Column(Enum('user', 'uri_core', 'uri_pjsip'))
   set_var = Column(Text)
   cos_audio = Column(INTEGER(11))
   cos_video = Column(INTEGER(11))
   message_context = Column(String(40))
   force_avp = Column(Enum('yes', 'no'))
   media_use_received_transport = Column(Enum('yes', 'no'))
   accountcode = Column(String(80))
   user_eq_phone = Column(Enum('yes', 'no'))
   moh_passthrough = Column(Enum('yes', 'no'))
   media_encryption_optimistic = Column(Enum('yes', 'no'))
   rpid_immediate = Column(Enum('yes', 'no'))
   g726_non_standard = Column(Enum('yes', 'no'))
   rtp_keepalive = Column(INTEGER(11))
   rtp_timeout = Column(INTEGER(11))
   rtp_timeout_hold = Column(INTEGER(11))
   bind_rtp_to_media_address = Column(Enum('yes', 'no'))
   voicemail_extension = Column(String(40))
   mwi_subscribe_replaces_unsolicited = Column(
       Enum('0', '1', 'off', 'on', 'false', 'true', 'no', 'yes'))
   deny = Column(String(95))
   permit = Column(String(95))
   acl = Column(String(40))
   contact_deny = Column(String(95))
   contact_permit = Column(String(95))
   contact_acl = Column(String(40))
   subscribe_context = Column(String(40))
   fax_detect_timeout = Column(INTEGER(11))
   contact_user = Column(String(80))
   preferred_codec_only = Column(Enum('yes', 'no'))
   asymmetric_rtp_codec = Column(Enum('yes', 'no'))
   rtcp_mux = Column(Enum('yes', 'no'))
   allow_overlap = Column(Enum('yes', 'no'))
   refer_blind_progress = Column(Enum('yes', 'no'))
   notify_early_inuse_ringing = Column(Enum('yes', 'no'))
   max_audio_streams = Column(INTEGER(11))
   max_video_streams = Column(INTEGER(11))
   webrtc = Column(Enum('yes', 'no'))
   dtls_fingerprint = Column(Enum('SHA-1', 'SHA-256'))
   incoming_mwi_mailbox = Column(String(40))
   bundle = Column(Enum('yes', 'no'))
   dtls_auto_generate_cert = Column(Enum('yes', 'no'))
   follow_early_media_fork = Column(Enum('yes', 'no'))
   accept_multiple_sdp_answers = Column(Enum('yes', 'no'))
   suppress_q850_reason_headers = Column(Enum('yes', 'no'))
   trust_connected_line = Column(
       Enum('0', '1', 'off', 'on', 'false', 'true', 'no', 'yes'))
   send_connected_line = Column(
       Enum('0', '1', 'off', 'on', 'false', 'true', 'no', 'yes'))
   ignore_183_without_sdp = Column(
       Enum('0', '1', 'off', 'on', 'false', 'true', 'no', 'yes'))
   codec_prefs_incoming_offer = Column(String(128))
   codec_prefs_outgoing_offer = Column(String(128))
   codec_prefs_incoming_answer = Column(String(128))
   codec_prefs_outgoing_answer = Column(String(128))
   stir_shaken = Column(
       Enum('0', '1', 'off', 'on', 'false', 'true', 'no', 'yes'))
   send_history_info = Column(
       Enum('0', '1', 'off', 'on', 'false', 'true', 'no', 'yes'))
   allow_unauthenticated_options = Column(
       Enum('0', '1', 'off', 'on', 'false', 'true', 'no', 'yes'))


class QueueMember(Base):
   __tablename__ = 'queue_members'

   queue_name = Column(String(80), primary_key=True, nullable=False)
   interface = Column(String(80), primary_key=True, nullable=False)
   membername = Column(String(80))
   state_interface = Column(String(80))
   penalty = Column(INTEGER(11))
   paused = Column(INTEGER(11))
   uniqueid = Column(INTEGER(11), nullable=False, unique=True)
   wrapuptime = Column(INTEGER(11))
   ringinuse = Column(Enum(u'0', u'1', u'off', u'on',
                           u'false', u'true', u'no', u'yes'))


class Queue(Base):
   __tablename__ = 'queues'

   name = Column(String(128), primary_key=True)
   musiconhold = Column(String(128))
   announce = Column(String(128))
   context = Column(String(128))
   timeout = Column(INTEGER(11))
   ringinuse = Column(Enum(u'yes', u'no'))
   setinterfacevar = Column(Enum(u'yes', u'no'))
   setqueuevar = Column(Enum(u'yes', u'no'))
   setqueueentryvar = Column(Enum(u'yes', u'no'))
   monitor_format = Column(String(8))
   membermacro = Column(String(512))
   membergosub = Column(String(512))
   queue_youarenext = Column(String(128))
   queue_thereare = Column(String(128))
   queue_callswaiting = Column(String(128))
   queue_quantity1 = Column(String(128))
   queue_quantity2 = Column(String(128))
   queue_holdtime = Column(String(128))
   queue_minutes = Column(String(128))
   queue_minute = Column(String(128))
   queue_seconds = Column(String(128))
   queue_thankyou = Column(String(128))
   queue_callerannounce = Column(String(128))
   queue_reporthold = Column(String(128))
   announce_frequency = Column(INTEGER(11))
   announce_to_first_user = Column(Enum(u'yes', u'no'))
   min_announce_frequency = Column(INTEGER(11))
   announce_round_seconds = Column(INTEGER(11))
   announce_holdtime = Column(String(128))
   announce_position = Column(String(128))
   announce_position_limit = Column(INTEGER(11))
   periodic_announce = Column(String(50))
   periodic_announce_frequency = Column(INTEGER(11))
   relative_periodic_announce = Column(Enum(u'yes', u'no'))
   random_periodic_announce = Column(Enum(u'yes', u'no'))
   retry = Column(INTEGER(11))
   wrapuptime = Column(INTEGER(11))
   penaltymemberslimit = Column(INTEGER(11))
   autofill = Column(Enum(u'yes', u'no'))
   monitor_type = Column(String(128))
   autopause = Column(Enum(u'yes', u'no', u'all'))
   autopausedelay = Column(INTEGER(11))
   autopausebusy = Column(Enum(u'yes', u'no'))
   autopauseunavail = Column(Enum(u'yes', u'no'))
   maxlen = Column(INTEGER(11))
   servicelevel = Column(INTEGER(11))
   strategy = Column(Enum(u'ringall', u'leastrecent', u'fewestcalls',
                          u'random', u'rrmemory', u'linear',
                          u'wrandom', u'rrordered'))
   joinempty = Column(String(128))
   leavewhenempty = Column(String(128))
   reportholdtime = Column(Enum(u'yes', u'no'))
   memberdelay = Column(INTEGER(11))
   weight = Column(INTEGER(11))
   timeoutrestart = Column(Enum(u'yes', u'no'))
   defaultrule = Column(String(128))
   timeoutpriority = Column(String(128))
