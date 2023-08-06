# -*- coding: utf-8 -*-

#
# Crypto-licensing -- Cryptographically signed licensing, w/ Cryptocurrency payments
#
# Copyright (c) 2022, Dominion Research & Development Corp.
#
# Crypto-licensing is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.  See the LICENSE file at the top of the source tree.
#
# It is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#

from __future__ import absolute_import, print_function, division

import ast
import codecs
import copy
import datetime
import dns.resolver
import hashlib
import json
import logging
import os
import sys
import traceback
import uuid

from ..misc		import (
    type_str_base, urlencode,
    parse_datetime, parse_seconds, Timestamp, Duration, Timespan,
    deduce_name, config_open,
)

__author__                      = "Perry Kundert"
__email__                       = "perry@dominionrnd.com"
__copyright__                   = "Copyright (c) 2022 Dominion Research & Development Corp."
__license__                     = "Dual License: GPLv3 (or later) and Commercial (see LICENSE)"

log				= logging.getLogger( "licensing" )

# Get Ed25519 support. Try a globally installed ed25519ll possibly with a CTypes binding, Otherwise,
# try our local Python-only ed25519ll derivation, or fall back to the very slow D.J.Bernstein Python
# reference implementation
from .. import ed25519

# Optionally, we can provide ChaCha20Poly1305 to support KeypairEncrypted
try:
    from chacha20poly1305 import ChaCha20Poly1305
except ImportError:
    pass


class LicenseIncompatibility( Exception ):
    """Something is wrong with the License, or supporting infrastructure."""
    pass


def domainkey_service( product ):
    """Convert a UTF-8 product name into a ASCII DNS Domainkey service name, with
    replacement for some symbols invalid in DNS names (TODO: incomplete).

        >>> domainkey_service( "Something Awesome v1.0" )
        'something-awesome-v1-0'

    Retains None, if supplied.
    """
    author_service		= product
    if author_service:
        author_service		= domainkey_service.idna_encoder( author_service )[0]
        if sys.version_info[0] >= 3:
            author_service	= author_service.decode( 'ASCII' )
        author_service		= author_service.translate( domainkey_service.dns_trans )
        author_service		= author_service.lower()
    return author_service
try:      # noqa: E305
    domainkey_service.dns_trans	= str.maketrans( ' ._/', '----' )
except AttributeError:   # Python2
    import string
    domainkey_service.dns_trans	= string.maketrans( ' ._/', '----' )
domainkey_service.idna_encoder	= codecs.getencoder( 'idna' )
assert "a/b.c_d e".translate( domainkey_service.dns_trans ) == 'a-b-c-d-e'


def into_hex( binary, encoding='ASCII' ):
    return into_text( binary, 'hex', encoding )


def into_b64( binary, encoding='ASCII' ):
    return into_text( binary, 'base64', encoding )


def into_text( binary, decoding='hex', encoding='ASCII' ):
    """Convert binary bytes data to the specified decoding, (by default encoded to ASCII text), across
    most versions of Python 2/3.  If no encoding, resultant decoding symbols remains as un-encoded
    bytes.

    A supplied None remains None.

    """
    if binary is not None:
        if isinstance( binary, bytearray ):
            binary		= bytes( binary )
        assert isinstance( binary, bytes ), \
            "Cannot convert to {}: {!r}".format( decoding, binary )
        binary			= codecs.getencoder( decoding )( binary )[0]
        binary			= binary.replace( b'\n', b'' ) # some decodings contain line-breaks
        if encoding is not None:
            return binary.decode( encoding )
        return binary


def into_bytes( text, decodings=('hex', 'base64'), ignore_invalid=None ):
    """Try to decode base-64 or hex bytes from the provided ASCII text, pass thru binary data as bytes.
    Must work in Python 2, which is non-deterministic; a str may contain bytes or text.

    So, assume ASCII encoding, start with the most strict (least valid symbols) decoding codec
    first.  Then, try as simple bytes.

    """
    if not text:
        return None
    if isinstance( text, bytearray ):
        return bytes( text )
    # First, see if the text looks like hex- or base64-decoded UTF-8-encoded ASCII
    encoding,is_ascii		= 'UTF-8',lambda c: 32 <= c <= 127
    try:
        # Python3 'bytes' doesn't have .encode (so will skip this code), and Python2 non-ASCII
        # binary data will raise an AssertionError.
        text_enc		= text.encode( encoding )
        assert all( is_ascii( c ) for c in bytearray( text_enc )), \
            "Non-ASCII symbols found: {!r}".format( text_enc )
        for c in decodings:
            try:
                binary		= codecs.getdecoder( c )( text_enc )[0]
                #log.debug( "Decoding {} {} bytes from: {!r}".format( len( binary ), c, text_enc ))
                return binary
            except Exception:
                pass
    except Exception:
        pass
    # Finally, check if the text is already bytes (*possibly* bytes in Python2, as str ===
    # bytes; so this cannot be done before the decoding attempts, above)
    if isinstance( text, bytes ):
        #log.debug( "Passthru {} {} bytes from: {!r}".format( len( text ), 'native', text ))
        return text
    if not ignore_invalid:
        raise RuntimeError( "Could not encode as {}, decode as {} or native bytes: {!r}".format(
            encoding, ', '.join( decodings ), text ))


def into_keys( keypair ):
    """Return whatever Ed25519 (public, signing) keys are available in the provided Keypair or
    32/64-byte key material.  This destructuring ordering is consistent with the
    namedtuple('Keypair', ('vk', 'sk')).

    Supports deserialization of keys from hex or base-64 encode public (32-byte) or secret/signing
    (64-byte) data.  To avoid nondeterminism, we will assume that all Ed25519 key material is encoded in
    base64 (never hex).

    """
    try:
        # May be a Keypair namedtuple
        return keypair.vk, keypair.sk
    except AttributeError:
        pass
    # Not a Keypair.  First, see if it's a serialized public/private key.
    deserialized	= into_bytes( keypair, ('base64',), ignore_invalid=True )
    if deserialized:
        keypair		= deserialized
    # Finally, see if we've recovered a signing or public key
    if isinstance( keypair, bytes ):
        if len( keypair ) == 64:
            # Must be a 64-byte signing key, which also contains the public key
            return keypair[32:64], keypair[0:64]
        elif len( keypair ) == 32:
            # Can only contain a 32-byte public key
            return keypair[:32], None
    # Unknown key material.
    return None, None


def into_str( maybe ):
    if maybe is not None:
        return str( maybe )


def into_str_UTC( ts, tzinfo=Timestamp.UTC ):
    if ts is not None:
        return ts.render( tzinfo=tzinfo, ms=False, tzdetail=True )


def into_str_LOC( ts ):
    return into_str_UTC( ts, tzinfo=Timestamp.LOC )


def into_JSON( thing, indent=None, default=None ):
    def endict( x ):
        try:
            return dict( x )
        except Exception as exc:
            if default:
                return default( x )
            log.warning("Failed to JSON serialize {!r}: {}".format( x, exc ))
            raise exc
    # Unfortunately, Python2 json.dumps w/ indent emits trailing whitespace after "," making
    # tests fail.  Make the JSON separators whitespace-free, so the only difference between the
    # signed serialization and an pretty-printed indented serialization is the presence of
    # whitespace.
    separators			= (',', ':')
    text			= json.dumps(
        thing, sort_keys=True, indent=indent, separators=separators, default=endict )
    return text


def into_boolean( val, truthy=(), falsey=() ):
    """Check if the provided numeric or str val content is truthy or falsey; additional tuples of
    truthy/falsey lowercase values may be provided."""
    if isinstance( val, (int,float,bool)):
        return bool( val )
    assert isinstance( val, type_str_base )
    if val.lower() in ( 't', 'true', 'y', 'yes' ) + truthy:
        return True
    elif val.lower() in ( 'f', 'false', 'n', 'no' ) + falsey:
        return False
    raise ValueError( val )


def into_timestamp( ts ):
    """Convert to a timestamp, retaining None.

    """
    if ts is not None:
        if isinstance( ts, type_str_base ):
            ts			= parse_datetime( ts )
        if isinstance( ts, datetime.datetime ):
            ts			= Timestamp( ts )
        assert isinstance( ts, Timestamp )
        return ts


def into_duration( dur ):
    """Convert to a duration, retaining None"""
    if dur is not None:
        if not isinstance( dur, Duration ):
            dur			= parse_seconds( dur )
            assert isinstance( dur, (int, float) )
            dur			= Duration( dur )
        return dur


def into_UUIDv4( machine ):
    if machine is not None:
        if not isinstance( machine, uuid.UUID ):
            machine		= uuid.UUID( machine )
        assert machine.version == 4
    return machine


def machine_UUIDv4( machine_id_path=None):
    """Identify the machine-id as an RFC 4122 UUID v4. On Linux systems w/ systemd, get from
    /etc/machine-id, as a UUID v4: https://www.man7.org/linux/man-pages/man5/machine-id.5.html.
    On MacOS and Windows, use uuid.getnode(), which derives from host-specific data (eg. MAC
    addresses, serial number, ...).

    This UUID should be reasonably unique across hosts, but is not guaranteed to be.

    TODO: Include root disk UUID?
    """
    if machine_id_path is None:
        machine_id_path		= "/etc/machine-id" 
    try:
        with open( machine_id_path, 'r' ) as m_id:
            machine_id		= m_id.read().strip()
    except Exception:
        # Node number is typically a much shorter integer; fill to required UUID length.
        machine_id		= "{:0>32}".format( hex( uuid.getnode())[2:] )
    try:
        machine_id		= into_bytes( machine_id, ('hex', ) )
        assert len( machine_id ) == 16
    except Exception as exc:
        raise RuntimeError( "Invalid Machine ID found: {!r}: {}".format( machine_id, exc ))
    machine_id			= bytearray( machine_id )
    machine_id[6]	       &= 0x0F
    machine_id[6]	       |= 0x40
    machine_id[8]	       &= 0x3F
    machine_id[8]	       |= 0x80
    machine_id			= bytes( machine_id )
    return uuid.UUID( into_hex( machine_id ))


def domainkey( product, domain, service=None, pubkey=None ):
    """Compute and return the DNS path for the given product and domain.  Optionally, returns the
    appropriate DKIM TXT RR record containing the agent's public key (base-64 encoded), as per the
    RFC: https://www.rfc-editor.org/rfc/rfc6376.html

        >>> from .verification import author, domainkey
        >>> path, dkim_rr = domainkey( "Some Product", "example.com" )
        >>> path
        'some-product.crypto-licensing._domainkey.example.com.'
        >>> dkim_rr

    
        # An Awesome, Inc. product
        >>> keypair = author( seed=b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA' )
        >>> path, dkim_rr = domainkey( "Something Awesome v1.0", "awesome-inc.com", pubkey=keypair )
        >>> path
        'something-awesome-v1-0.crypto-licensing._domainkey.awesome-inc.com.'
        >>> dkim_rr
        'v=DKIM1; k=ed25519; p=25lf4lFp0UHKubu6krqgH58uHs599MsqwFGQ83/MH50='

    """
    if service is None:
        service			= domainkey_service( product )
    assert service, \
        "A service is required to deduce the DKIM DNS path"
    domain_name			= dns.name.from_text( domain )
    service_name		= dns.name.Name( [service, 'crypto-licensing', '_domainkey'] )
    path_name			= service_name + domain_name
    path			= path_name.to_text()

    dkim			= None
    if pubkey:
        pubkey,_		= into_keys( pubkey )
        dkim			= '; '.join( "{k}={v}".format(k=k, v=v) for k,v in (
            ('v', 'DKIM1'),
            ('k', 'ed25519'),
            ('p', into_b64( pubkey )),
        ))

    return (path, dkim)


class Serializable( object ):
    """A base-class that provides a deterministic Unicode JSON serialization of every __slots__
    attribute, and a consistent dict representation of the same serialized data.  Access attributes
    directly to obtain underlying types.

    Uses __slots__ in derived classes to identify serialized attributes; traverses the class
    hierarchy's MRO to identify all attributes to serialize.  Output serialization is always in
    attribute-name sorted order.

    If an attribute requires special serialization handling (other than simple conversion to 'str'),
    then include it in the class' serializers dict, eg:

        serializers		= dict( special = into_hex )

    It is expected that derived class' constructors will deserialize when presented with keywords
    representing all __slots__.

    """

    __slots__			= ()
    serializers			= {}

    def keys( self, every=False ):
        """Yields the Serializable object's relevant keys.  For many uses (eg. conversion to dict), the
        default behaviour of ignoring keys with values of None is appropriate.  However, if you want
        all keys regardless of content, specify every=True.

        """
        for cls in type( self ).__mro__:
            for key in getattr( cls, '__slots__', []):
                if every or getattr( self, key ) is not None: # If the key is empty, don't include it
                    yield key

    def serializer( self, key ):
        """Finds any custom serialization formatter specified for the given attribute, defaults to None.

        """
        for cls in type( self ).__mro__:
            try:
                return cls.serializers[key]
            except (AttributeError, KeyError):
                pass

    def __getitem__( self, key ):
        """Returns the serialization of the requested key, passing thru values without a serializer."""
        if key in self.keys( every=True ):
            try:
                serialize	= self.serializer( key ) # (no Exceptions)
                value		= getattr( self, key ) # IndexError
                if serialize:
                    return serialize( value ) # conversion failure Exceptions
                return value
            except Exception as exc:
                log.debug( "Failed to convert {class_name}.{key} with {serialize!r}: {exc}".format(
                    class_name = self.__class__.__name__, key=key, serialize=serialize, exc=exc ))
                raise
        raise IndexError( "{} not found in keys {}".format( key, ', '.join( self.keys( every=True ))))

    def __str__( self ):
        return self.serialize( indent=4, encoding=None ) # remains as UTF-8 text

    def serialize( self, indent=None, encoding='UTF-8', default=None ):
        """Return a binary 'bytes' serialization of the present object.  Serialize to JSON, assuming any
        complex sub-objects (eg. License, LicenseSigned) have a sensible dict representation.

        The default serialization (ie. with indent=None) will be the one used to create the digest.

        If there are objects to be serialized that require special handling, they must not have a
        'dict' interface (be convertible to a dict), and then a default may be supplied to serialize
        them (eg. str).

        """
        stream			= into_JSON( self, indent=indent, default=default )
        if encoding:
            stream		= stream.encode( encoding )
        return stream

    def sign( self, sigkey, pubkey=None ):
        """

        Sign our default serialization, and (optionally) confirm that the supplied public key (which
        will be used to check the signature) is correct, by re-deriving the public key.

        """
        vk, sk			= into_keys( sigkey )
        assert sk, \
            "Invalid ed25519 signing key provided"
        if pubkey:
            # Re-derive and confirm supplied public key matches supplied signing key
            keypair		= ed25519.crypto_sign_keypair( sk[:32] )
            assert keypair.vk == pubkey, \
                "Mismatched ed25519 signing/public keys"
        signed			= ed25519.crypto_sign( self.serialize(), sk )
        signature		= signed[:64]
        return signature

    def verify( self, pubkey, signature ):
        """Check that the supplied signature matches this serialized payload, and return the verified
        payload bytes.

        """
        pubkey, _		= into_keys( pubkey )
        signature		= into_bytes( signature, ('base64',) )
        assert pubkey and signature, \
            "Missing required {}".format(
                ', '.join( () if pubkey else ('public key',)
                          +() if signature else ('signature',) ))
        return ed25519.crypto_sign_open( signature + self.serialize(), pubkey )

    def digest( self, encoding=None, decoding=None ):
        """The SHA-256 hash of the serialization, as 32 bytes.  Optionally, encode w/ a named codec,
        eg.  "hex" or "base64".  Often, these will require a subsequent .decode( 'ASCII' ) to become
        a non-binary str.

        """
        binary			= hashlib.sha256( self.serialize() ).digest()
        if encoding is not None:
            binary		= codecs.getencoder( encoding )( binary )[0].replace(b'\n', b'')
            if decoding is not None:
                return binary.decode( decoding )
        return binary

    def hexdigest( self ):
        """The SHA-256 hash of the serialization, as a 256-bit (32 byte, 64 character) hex string."""
        return self.digest( 'hex', 'ASCII' )

    def b64digest( self ):
        return self.digest( 'base64', 'ASCII' )

    def __copy__( self ):
        """Create a new object by copying an existing object, taking __slots__ into account.

        """
        result			= self.__class__.__new__( self.__class__ )

        for cls in type( self ).__mro__:
            for key in getattr( cls, '__slots__', [] ):
                setattr( result, key, copy.copy( getattr( self, key )))

        return result


class IssueRequest( Serializable ):
    __slots__			= (
        'author', 'author_pubkey', 'product',
        'client', 'client_pubkey', 'machine'
    )
    serializers			= dict(
        author_pubkey	= into_b64,
        client_pubkey	= into_b64,
        machine		= into_str,
    )

    def __init__( self, author=None, author_pubkey=None, product=None,
                  client=None, client_pubkey=None, machine=None ):
        self.author		= into_str( author )
        self.author_pubkey, _	= into_keys( author_pubkey )
        self.product		= into_str( product )
        self.client		= into_str( client )
        self.client_pubkey, _	= into_keys( client_pubkey )
        self.machine		= into_UUIDv4( machine )

    def query( self, sigkey ):
        """Issue query is sorted-key order"""
        qd			= dict( self )
        qd['signature']		= into_b64( self.sign( sigkey=sigkey ))
        return urlencode( sorted( qd.items() ))


def overlap_intersect( start, length, other ):
    """Accepts a start/length, and either a License or a Timespan (something w/ start and length), and
    compute the intersecting start/length, and its begin and (if known) ended timestamps.
    
        start,length,begun,ended = overlap_intersect( start, length, other )

    """
    # Detect the situation where there is no computable overlap, and start, length is defined by one
    # pair or the other.
    if start is None:
        # This license has no defined start time (it is perpetual); other license determines
        assert length is None, "Cannot specify a length without a start timestamp"
        if other.start is None:
            # Neither specifies start at a defined time
            assert other.length is None, "Cannot specify a length without a start timestamp"
            return None,None,None,None
        if other.length is None:
            return other.start,other.length,other.start,None
        return other.start,other.length,other.start,other.start + other.length
    elif other.start is None:
        assert other.length is None, "Cannot specify a length without a start timestamp"
        if length is None:
            return start,length,start,None
        return start,length,start,start + length

    # Both have defined start times; begun defines beginning of potential overlap If the computed
    # ended time is <= begun, then there is no (zero) overlap!
    begun 		= max( start, other.start )
    ended		= None
    if length is None and other.length is None:
        # But neither have duration
        return start,length,begun,None

    # At least one length; ended is computable, as well as the overlap start/length
    if other.length is None:
        ended		= start + length
    elif length is None:
        ended		= other.start + other.length
    else:
        ended		= min( start + length, other.start + other.length )
    start		= begun
    length		= Duration( 0 if ended <= begun else ended - begun )
    return start,length,begun,ended


class Agent( Serializable ):
    __slots__			= (
        'name', 'pubkey', 'domain', 'product', 'service',
    )
    serializers			= dict(
        pubkey		= into_b64,
    )

    def __init__( self, name,
                  pubkey	= None,			# Normally, obtained from domain's DKIM1 TXT RR
                  domain	= None,			# Needed for DKIM if no pubkey provided
                  product	= None,
                  service	= None,			# Normally, derived from product name
                 ):
        # Obtain the Agent's public key; either given through the API, or obtained from their
        # domain's DKIM entry.
        assert pubkey or ( domain and ( product or service )), \
            "Either a pubkey or a domain + service/product must be provided"
        self.name	= name
        self.domain	= domain
        self.product	= product
        self.service	= service
        self.pubkey,_	= into_keys( pubkey )
        # Now pubkey_query has all the details it requires to do a DKIM lookup, if necessary
        if not self.pubkey:
            self.pubkey	= self.pubkey_query()

    def pubkey_query( self ):
        """Obtain the agent's public key.  This was either provided at License construction time, or
        can be obtained from a DNS TXT "DKIM" record.
        
        TODO: Cache

        Query the DKIM record for an author public key.  May be split into multiple strings:

            r = dns.resolver.query('default._domainkey.justicewall.com', 'TXT')
            for i in r:
            ...  i.to_text()
            ...
            '"v=DKIM1; k=rsa; p=MIIBIjANBgkqhkiG9...Btx" "aPXTN/aI+cvS8...4KHoQqhS7IwIDAQAB;"'

        Fortunately, the Python AST for string literals handles this quite nicely:

            >>> ast.literal_eval('"abc" "123"')
            'abc123'

        """
        dkim_path, _dkim_rr	= domainkey( self.product, self.domain, service=self.service )
        log.debug("Querying {domain} for DKIM service {service}: {dkim_path}".format(
            domain=self.domain, service=self.service, dkim_path=dkim_path ))
        # Python2/3 compatibility; use query vs. resolve
        records			= list( rr.to_text() for rr in dns.resolver.query( dkim_path, 'TXT' ))
        assert len( records ) == 1, \
            "Failed to obtain a single TXT record from {dkim_path}".format( dkim_path=dkim_path )
        # Parse the "..." "..." strings.  There should be no escaped quotes.
        dkim			= ast.literal_eval( records[0] )
        log.debug("Parsing DKIM record: {dkim!r}".format( dkim=dkim ))
        p			= None
        for pair in dkim.split( ';' ):
            key,val 		= pair.strip().split( '=', 1 )
            if key.strip().lower() == "v":
                assert val.upper() == "DKIM1", \
                    "Failed to find DKIM record; instead found record of type/version {val}".format( val=val )
            if key.strip().lower() == "k":
                assert val.lower() == "ed25519", \
                    "Failed to find Ed25519 public key; instead was of type {val!r}".format( val=val )
            if key.strip().lower() == "p":
                p		= val.strip()
        assert p, \
            "Failed to locate public key in TXT DKIM record: {dkim}".format( dkim=dkim )
        p_binary		= into_bytes( p, ('base64',) )
        return p_binary


class License( Serializable ):
    """Represents the details of a Licence from an author to a client (could be any client, if no
    client_pubkey provided).  Cannot be constructed unless the supplied License details are valid
    with respect to any supplied License dependencies.

    {
        "author": "Dominion Research & Development Corp.",
        "author_domain": "dominionrnd.com",
        "author_service": "cpppo",
        "client": "Awesome Inc.",
        "client_pubkey": "...",
        "dependencies": None,
        "product": "Cpppo",
        "length": "1y",
        "machine": None,
        "start": "2021-01-01 00:00:00+00:00")
    }

    Verifying a License
    -------------------

    A signed license is a claim by an Author that the License is valid; it is up to a recipient to
    check that the License also actually satisfies the constraints of any License dependencies.  A
    nefarious Author could create a License and properly sign it -- but not satisfy the License
    constraints.  License.verify(confirm=True) will do this, as well as (optionally) retrieve and
    verify from DNS the public keys of the (claimed) signed License dependencies.

    Checking your License
    ---------------------

    Each module that uses crypto_licensing.licensing checks that the final product's License or its
    parents contains valid license(s) for itself, somewhere within the License dependencies tree.

    All start times are expressed in the UTC timezone; if we used the local timezone (as computed
    using get_localzone, wrapped to respect any TZ environment variable, and made available as
    timestamp.LOC), then serializations (and hence signatures and signature tests) would be
    inconsistent.

    Licenses for products are signed by the author using their signing key.  The corresponding
    public key is expected to be found in a DKIM entry; eg. for Dominion's Cpppo product:

        cpppo.crypto-licensing._domainkey.dominionrnd.com 300 IN TXT "v=DKIM1; k=ed25519; p=ICkF+6tTRKc8voK15Th4eTXMX3inp5jZwZSu4CH2FIc="


    Licenses may carry optional constraints, with functions to validate their values.  These may be
    expressed in terms of all Licenses issued by the Author.  During normal License.verify of an
    installed License, nothing about the pool of issued Licenses is known, so no additional
    verification can be done.  However, when an Author is issuing a License and has access to the
    full pool of issued Licenses, all presently issued values of the constraint are known.

    If a lambda is provided it will be passed a proposed value as its second default parameter, with
    the first parameter defaulting to None, or a list containing all present instances of the
    constraint across all currently valid Licenses.  For example, if only 10 machine licenses are
    available, return the provided machine if the number is not exhausted:

        machine = "00010203-0405-4607-8809-0a0b0c0d0e0f"
        machine__verifier = lambda m, ms=None: \
            ( str( m ) if len( str( m ).split( '-' )) == 5 else ValueError( f"{m} doesn't look like a UUID" )\
                if ms is None or len( ms ) < 10 \
                else ValueError( "No more machine licenses presently available" )

    Alternatively, a None or numeric limit could be distributed across all issued licenses:

        targets = 3
        targets__verifier = lambda n, ns=None: \
            None if n is None else int( n ) \
              if n is None or ns is None or int( n ) + sum( map( int, filter( None, ns ))) <= 100 \
              else ValueError( f"{n} exceeds {100-sum(map(int,filter(None,ns)))} targets available" )

    If an Exception is returned, it will be raised.  Otherwise, the result of the lambda will be
    used as the License' value for the constraint.

    """

    __slots__			= (
        'author',
        'client',
        'dependencies',
        'start', 'length',
        'machine',
    )
    serializers			= dict(
        start		= into_str_UTC,
        length		= into_str,
        machine		= into_str,
    )

    def __init__(
        self,
        author,
        client		= None,
        dependencies	= None,				# Any sub-Licenses
        start		= None,
        length		= None,				# License may not be perpetual
        machine		= None,				# A specific host may be specified
        machine_id_path	= None,
        confirm		= None,				# Validate License' author_pubkey from DNS
    ):
        if isinstance( author, type_str_base ):
            author		= json.loads( author )	# Deserialize Agent, if necessary
        self.author	= Agent( **author )
        if isinstance( client, type_str_base ):
            client		= json.loads( client )	# Deserialize Agent, if necessary
        self.client	= Agent( **client ) if client else None

        # Reconstitute LicenseSigned provenance from any dicts provided
        self.dependencies	= None if dependencies is None else list(
            LicenseSigned( confirm=confirm, **prov ) if isinstance( prov, dict ) else prov
            for prov in dependencies
        )

        # A License usually has a timespan of start timestamp and duration length.  These cannot
        # exceed the timespan of any License dependencies.  First, get any supplied start time as a
        # cpppo.history.timestamp, and any duration length as a number of seconds.
        try:
            self.start		= into_timestamp( start )
            self.length		= into_duration( length )
        except Exception as exc:
            raise LicenseIncompatibility(
                    "License start: {start!r} or length: {length!r} invalid: {exc}".format(
                        start=start, length=length, exc=exc ))

        self.machine		= into_UUIDv4( machine )

        # Only allow the construction of valid Licenses.
        self.verify( confirm=confirm, machine_id_path=machine_id_path )

    def overlap( self, *others ):
        """Compute the overlapping start/length that is within the bounds of this and other license(s).
        If they do not overlap, raises a LicenseIncompatibility Exception.

        Any other thing that doesn't have a .product, .author defaults to *this* License's
        attributes (eg. we're applying further Timespan constraints to this License).

        """
        start, length		= self.start, self.length
        for other in others:
            # If we determine a 0-length overlap, we have failed.
            start, length, begun, ended \
                                = overlap_intersect( start, length, other )
            if length is not None and length.total_seconds() == 0:
                # Overlap was computable, and was zero
                raise LicenseIncompatibility(
                    "License for {author}'s {product!r} from {start} for {length} incompatible with others".format(
                        author	= getattr( getattr( other, 'author', None ), 'name', None )  or self.author.name,
                        product	= getattr( getattr( other, 'author', None ), 'product', None ) or self.author.product,
                        start	= into_str_LOC( other.start ),
                        length	= other.length,
                    ))
        return start, length

    def verify(
        self,
        author_pubkey	= None,
        signature	= None,
        confirm		= None,
        machine_id_path	= None,
        **constraints
    ):
        """Verify that the License is valid:

            - Has properly signed License dependencies
              - Each public key can be confirmed, if desired
            - Complies with the bounds of any License dependencies
              - A sub-License must be issued while all License dependencies are active
            - Allows any constraints supplied.

        If it does, the constraints are returned, including this LicenseSigned added to the
        dependencies.  If no additional constraints are supplied, this will simply return the empty
        constraints dict on success.  The returned constraints would be usable in constructing a new
        License (assuming at least the necessary author, author_domain and product were defined).

        """
        if author_pubkey:
            author_pubkey, _	= into_keys( author_pubkey )
            assert author_pubkey, "Unrecognized author_pubkey provided"

        if author_pubkey and author_pubkey != self.author.pubkey:
            raise LicenseIncompatibility( 
                "License for {auth}'s {prod!r} public key mismatch".format(
                    auth	= self.author.name,
                    prod	= self.author.product,
                ))
        # Verify that the License's stated public key matches the one in the domain's DKIM.  Default
        # to True when confirm is None.
        if confirm or confirm is None:
            avkey	 	= self.author.pubkey_query()
            if avkey != self.author.pubkey:
                raise LicenseIncompatibility(
                    "License for {auth}'s {prod!r}: author key from DKIM {found} != {claim}".format(
                        auth	= self.author.name,
                        prod	= self.author.product,
                        found	= into_b64( avkey ),
                        claim	= into_b64( self.author.pubkey ),
                    ))
        # Verify that the License signature was indeed produced by the signing key corresponding to
        # the provided public key
        if signature:
            try:
                super( License, self ).verify( pubkey=self.author.pubkey, signature=signature )
            except Exception as exc:
                raise LicenseIncompatibility( 
                    "License for {auth}'s {prod!r}: signature mismatch: {sig!r}; {exc}".format(
                        auth	= self.author.name,
                        prod	= self.author.product,
                        sig	= signature,
                        exc	= exc,
                    ))

        # Verify any License dependencies are valid; signed w/ DKIM specified key, License OK.
        # When verifying License dependencies, we don't supply the constraints, because we're not
        # interested in sub-Licensing these Licenses, only verifying them.
        for prov_dct in self.dependencies or []:
            prov		= LicenseSigned( confirm=confirm, **prov_dct )
            try:
                prov.verify( confirm=confirm, machine_id_path=machine_id_path )
                assert prov.license.client.pubkey is None or prov.license.client.pubkey == self.author.pubkey, \
                    "sub-License client public key {client_pubkey} doesn't match Licence author's public key {author_pubkey}".format(
                        client_pubkey	= into_b64( prov.license.client.pubkey ),
                        author_pubkey	= into_b64( self.author.pubkey ),
                    )
            except Exception as exc:
                raise LicenseIncompatibility(
                    "License for {auth}'s {prod!r}; sub-License for {dep_auth}'s {dep_prod!r} invalid: {exc}".format(
                        auth		= self.author.name,
                        prod		= self.author.product,
                        dep_auth	= prov.license.author.name,
                        dep_prod	= prov.license.author.product,
                        exc		= exc,
                    ))

        # Enforce all constraints, returning a dict suitable for creating a specialized License, if
        # a signature was provided; if not, we cannot produce a specialized sub-License, and must
        # fail.

        # First, scan the constraints to see if any are callable
        

        # Verify all sub-license start/length durations comply with this License' duration.
        # Remember, these start/length specify the validity period of the License to be
        # sub-licensed, not the execution time of the installation!
        try:
            # Collect any things with .start/.length; all sub-Licenses dependencies, and a Timespan
            # representing any supplied start/length constraints in order to validate their
            # consistency with the sub-License start/lengths.
            others		= list( ls.license for ls in ( self.dependencies or [] ))
            start_cons		= into_timestamp( constraints.get( 'start' ))
            length_cons		= into_duration( constraints.get( 'length' ))
            others.append( Timespan( start_cons, length_cons ))
            start, length	= self.overlap( *others )
        except LicenseIncompatibility as exc:
            raise LicenseIncompatibility(
                "License for {auth}'s {prod!r}; sub-{exc}".format(
                    auth	= self.author.name,
                    prod	= self.author.product,
                    exc		= exc,
                ))
        else:
            # Finally, if either start or length constraints were supplied, update them both with
            # the computed timespan of start/length constraints overlapped with all dependencies.
            if ( start_cons or length_cons ) and start_cons:
                constraints['start'] = into_str_UTC( start )
                constraints['length'] = into_str( length )

        # TODO: Implement License expiration date, to allow a software deployment to time out and
        # refuse to run after a License as expired, forcing the software owner to obtain a new
        # License with a future expiration.  Typically, Cpppo installations are perpetual; if
        # installed with a valid License, they will continue to work without expiration.  However,
        # other software authors may want to sell software that requires issuance of new Licenses.

        # Default 'machine' constraints to the local machine UUID.  If no constraints and
        # self.machine is None, we don't need to do anything, because the License is good for any
        # machine.  Use machine=True to force constraints to include the current machine UUID.
        machine			= None
        if machine_id_path != False and ( self.machine or constraints.get( 'machine' )):
            # Either License or constraints specify a machine (so we have to verify), and the
            # machine_id_path directive doesn't indicate to *not* check the machine ID (eg. when
            # issuing the license from a different machine)
            machine_uuid	= machine_UUIDv4( machine_id_path=machine_id_path )
            if self.machine not in (None, True) and self.machine != machine_uuid:
                raise LicenseIncompatibility(
                    "License for {auth}'s {prod!r} specifies Machine ID {required}; found {detected}".format(
                        auth	= self.author.name,
                        prod	= self.author.product,
                        required= self.machine,
                        detected= machine_uuid,
                    ))
            machine_cons	= constraints.get( 'machine' )
            if machine_cons not in (None, True) and machine_cons != machine_uuid:
                raise LicenseIncompatibility(
                    "Constraints on {auth}'s {prod!r} specifies Machine ID {required}; found {detected}".format(
                        auth	= self.author.name,
                        prod	= self.author.product,
                        required= machine_cons,
                        detected= machine_uuid,
                    ))
            # Finally, unless the supplied 'machine' constraint was explicitly None (indicating that
            # the caller desires a machine-agnostic sub-License), default to constrain the License to
            # this machine.
            if machine_cons is not None:
                constraints['machine'] = machine_uuid

        log.info( "License for {auth}'s {prod!r} is valid from {start} for {length} on machine {machine}".format(
            auth	= self.author.name,
            prod	= self.author.product,
            start	= into_str_LOC( start ),
            length	= length,
            machine	= into_str( machine ) or into_str( constraints.get( 'machine' )) or '(any)',
        ))

        # Finally, now that the License, all License dependencies and any supplied constraints have
        # been verified, augment the constraints with this LicenseSigned as one of the dependencies.
        if constraints:
            assert signature is not None, \
                "Attempt to issue a sub-License of an un-signed License"
            constraints.setdefault( 'dependencies', [] )
            constraints['dependencies'].append( dict(
                LicenseSigned( license=self, signature=signature, confirm=confirm, machine_id_path=machine_id_path )
            ))

        return constraints


class LicenseSigned( Serializable ):
    """A License and its Ed25519 Signature provenance.  Only a LicenseSigned (and confirmation of the
    author's public key) proves that a License was actually issued by the purported author.  It is
    expected that authors will only sign a valid License.

    The public key of the author must be confirmed through independent means.  One typical means is
    by checking publication on the author's domain (the default behaviour w/ confirm=None), eg.:

        awesome-tool.crypto-licensing._domainkey.awesome-inc.com 86400 IN TXT \
            "v=DKIM1; k=ed25519; p=PW847sz.../M+/GZc="


    Authoring a License
    -------------------
    
    A software issuer (or end-user, in the case of machine-specific or numerically limited Licenses)
    must create new Licenses.
    
        >>> from crypto_licensing import author, issue, verify
    
    First, create a Keypair, including both signing (private, .sk) and verifying (public, .vk) keys:

        >>> signing_keypair = author( seed=b'our secret 32-byte seed material' )

    Then, create a License, identifying the author by their public key, and the product.  This
    example is a perpetual license (no start/length), for any machine.

        >>> license = License( author = "Awesome, Inc.", product = "Awesome Tool", \
                author_domain = "awesome-inc.com", author_pubkey = signing_keypair.vk, \
                confirm=False ) # since awesome-inc.com doesn't actually exist...

    Finally, issue the LicenseSigned containing the License and its Ed25519 Signature provenance:

        >>> provenance = issue( license, signing_keypair, confirm=False )
        >>> provenance_ser = provenance.serialize( indent=4 )
        >>> print( provenance_ser.decode( 'UTF-8' ) )
        {
            "license":{
                "author":"Awesome, Inc.",
                "author_domain":"awesome-inc.com",
                "author_pubkey":"PW847szICqnQBzbdr5TAoGO26RwGxG95e3Vd/M+/GZc=",
                "author_service":"awesome-tool",
                "client":null,
                "client_pubkey":null,
                "dependencies":null,
                "length":null,
                "machine":null,
                "product":"Awesome Tool",
                "start":null
            },
            "signature":"MiOGUpkv6/RWzI/C/VP1Ncn7N4WZa0lpiVzETZ4CJsLSo7qGLxIx+X+4tal16CcT+BUW1cDwJtcTftI5z+RHAQ=="
        }


    De/Serializing Licenses
    -----------------------
    
    Licenses are typically stored in files, in the configuration directory path of the application.

        import json
        # Locate, open, read 
        #with config_open( "application.crypto-licencing", 'r' ) as provenance_file:
        #    provenance_ser	= provenance_file.read()
        >>> provenance_dict = json.loads( provenance_ser )

    Or use the crypto_licensing.load() API to get them all into a dict, with
    the license file basename deduced from your __package__ or __file__ name:

        import crypto_licensing as cl
        licenses		= dict( cl.load( 
            filename	= __file__,
            confirm	= False, # don't check signing key validity via DKIM
        ))

    Validating Licenses
    -------------------

    Somewhere in the product's code, the License is loaded and validated.

        >>> provenance_load = LicenseSigned( confirm=False, **provenance_dict )
        >>> print( provenance_load )
        {
            "license":{
                "author":"Awesome, Inc.",
                "author_domain":"awesome-inc.com",
                "author_pubkey":"PW847szICqnQBzbdr5TAoGO26RwGxG95e3Vd/M+/GZc=",
                "author_service":"awesome-tool",
                "client":null,
                "client_pubkey":null,
                "dependencies":null,
                "length":null,
                "machine":null,
                "product":"Awesome Tool",
                "start":null
            },
            "signature":"MiOGUpkv6/RWzI/C/VP1Ncn7N4WZa0lpiVzETZ4CJsLSo7qGLxIx+X+4tal16CcT+BUW1cDwJtcTftI5z+RHAQ=="
        }
        >>> verify( provenance_load, confirm=False )
        {}

    """

    __slots__			= ('license', 'signature')
    serializers			= dict(
        signature	= into_b64,
    )

    def __init__( self, license, author_sigkey=None, signature=None, confirm=None, machine_id_path=None ):
        """Given an ed25519 signing key (32-byte private + 32-byte public), produce the provenance
        for the supplied License. 

        Normal constructor calling convention to take a License and a signing key and create
        a signed provenance:

            LicenseSigned( <License>, <Keypair> )

        To reconstruct from a dict (eg. recovered from a .crypto-licensing file):

            LicenseSigned( **provenance_dict )

        """
        if isinstance( license, type_str_base ):
            license		= json.loads( license ) # Deserialize License, if necessary
        assert isinstance( license, (License, dict) ), \
            "Require a License or its serialization dict, not a {!r}".format( license )
        if isinstance( license, dict ):
            license		= License( confirm=confirm, machine_id_path=machine_id_path, **license )
        self.license		= license

        assert signature or author_sigkey, \
            "Require either signature, or the means to produce one via the author's signing key"
        if author_sigkey and not signature:
            # Sign our default serialization, also confirming that the public key matches
            self.signature	= self.license.sign(
                sigkey=author_sigkey, pubkey=self.license.author.pubkey )
        elif signature:
            # Could be a hex-encoded signature on deserialization, or a 64-byte signature.  If both
            # signature and author_sigkey, we'll just be confirming the supplied signature, below.
            self.signature	= into_bytes( signature, ('base64',) )

        self.verify(
            author_pubkey	= author_sigkey,
            confirm		= confirm,
            machine_id_path	= machine_id_path )

    def verify( self, author_pubkey=None, signature=None, confirm=None, machine_id_path=None,
                **constraints ):
        return self.license.verify(
            author_pubkey	= author_pubkey or self.license.author.pubkey,
            signature		= signature or self.signature,
            confirm		= confirm,
            machine_id_path	= machine_id_path,
            **constraints )


class KeypairPlaintext( Serializable ):
    """De/serialize the plaintext Ed25519 private and public key material"""
    __slots__			= ('sk', 'vk')
    serializers			= dict(
        sk		= into_b64,
        vk		= into_b64,
    )

    def __init__( self, sk=None, vk=None ):
        """Support sk and optionally vk to derive and verify the Keypair.  At minimum, the first 256
        bits of private key material must be supplied; the remainder of the 512-bit signing key is a
        copy of the public key.

        """
        assert sk, \
            "Cannot recover Plaintext Keypair without private key material"
        self.sk			= into_bytes( sk, ('base64',) )
        assert len( self.sk ) in (32, 64), \
            "Expected 256-bit or 512-bit Ed25519 Private Key, not {}-bit {!r}".format(
                len( self.sk ) * 8, self.sk )
        if vk:
            self.vk		= into_bytes( vk, ('base64',) )
            assert len( self.vk ) == 32, \
                "Expected 256-bit Ed25519 Public Key, not {}-bit {!r}".format(
                    len( self.vk ) * 8, self.vk )
            assert len( self.sk ) != 64 or self.vk == self.sk[32:], \
                "Inconsistent Ed25519 signing / public keys in supplied data"
        elif len( self.sk ) == 64:
            self.vk		= self.sk[32:]
        else:
            self.vk		= None
        # We know into_keypair is *only* going to use the self.sk[:32] (and optionally self.vk to
        # verify), so we've recovered enough to call it.
        self.vk, self.sk	= self.into_keypair()

    def into_keypair( self, **kwds ):
        """No additional data required to obtain Keypair; just the leading 256-bit private key material
        of the private key.

        """
        keypair			= author( seed=self.sk[:32], why="provided plaintext signing key" )
        if self.vk:
            assert keypair.vk == self.vk, \
                "Failed to derive matching Ed25519 signing key from supplied data"
        return keypair


class KeypairCredentialError( Exception ):
    """Something is wrong with the provided Keypair credentials."""
    pass


class KeypairEncrypted( Serializable ):
    """De/serialize the keypair encrypted derivation seed, and the salt used in combination with the
    supplied username and password to derive the symmetric encryption key for encrypting the seed.
    The supported derivation(s):

        sha256:		hash of salt + username + password

    The 256-bit Ed25519 Keypair seed is encrypted using ChaCha20Poly1305 w/ the salt and derived
    key.  The salt and ciphertext are always serialized in hex, to illustrate that it is not Ed25519
    Keypair data.

    """
    __slots__			= ('salt', 'ciphertext')
    serializers			= dict(
        salt		= into_hex,
        ciphertext	= into_hex,
    )

    def __init__( self, salt=None, ciphertext=None, username=None, password=None, vk=None, sk=None ):
        assert ( ciphertext and salt ) or ( sk and password and username ), \
            "Insufficient data to create an Encrypted Keypair"
        if salt:
            self.salt		= into_bytes( salt, ('hex',) )
        else:
            # If salt not supplied, supply one -- but we obviously can't be given an encrypted seed!
            assert vk and not ciphertext, \
                "Expected unencrypted keypair if no is salt provided"
            self.salt		= os.urandom( 12 )
        assert len( self.salt ) == 12, \
            "Expected 96-bit salt, not {!r}".format( self.salt )
        if ciphertext:
            # We are provided with the encrypted seed (tag + ciphertext).  Done!  But, we don't know
            # the original Keypair, here, so we can't verify below.
            self.ciphertext	= into_bytes( ciphertext, ('hex',) )
            assert len( self.ciphertext ) * 8 == 384, \
                "Expected 384-bit ChaCha20Poly1305-encrypted seed, not a {}-bit {!r}".format(
                    len( self.ciphertext ) * 8, self.ciphtertext )
            keypair		= None
        else:
            # We are provided with the unencrypted signing key.  We must encrypt the 256-bit private
            # key material to produce the seed ciphertext.  Remember, the Ed25519 private signing
            # key always includes the 256-bit public key appended to the raw 256-bit private key
            # material.
            sk			= into_bytes( sk, ('base64',) )
            seed		= sk[:32]
            keypair		= author( seed=seed, why="provided unencrypted signing key" )
            if vk:
                vk		= into_bytes( vk, ('base64',) )
                assert keypair.vk == vk, \
                    "Failed to derive Ed25519 signing key from supplied data"
            key			= self.key( username=username, password=password )
            cipher		= ChaCha20Poly1305( key )
            plaintext		= bytearray( seed )
            nonce		= self.salt
            self.ciphertext	= bytes( cipher.encrypt( nonce, plaintext ))
        if username and password:
            # Verify MAC by decrypting w/ username and password, if provided
            keypair_rec		= self.into_keypair( username=username, password=password )
            assert keypair is None or keypair_rec == keypair, \
                "Failed to recover original key after decryption"

    def key( self, username, password ):
        # The username, which is often an email address, should be case-insensitive.
        username		= username.lower()
        username		= username.encode( 'UTF-8' )
        password		= password.encode( 'UTF-8' )
        m			= hashlib.sha256()
        m.update( self.salt )
        m.update( username )
        m.update( password )
        return m.digest()

    def into_keypair( self, username=None, password=None ):
        """Recover the original signing Keypair by decrypting with the supplied data.  Raises a
        KeypairCredentialError on decryption failure.

        """
        assert username and password, \
            "Cannot recover Encrypted Keypair without username and password"
        key			= self.key( username=username, password=password )
        cipher			= ChaCha20Poly1305( key )
        nonce			= self.salt
        ciphertext		= bytearray( self.ciphertext )
        try:
            plaintext		= bytes( cipher.decrypt( nonce, ciphertext ))
        except:
            raise KeypairCredentialError(
                "Failed to decrypt ChaCha20Poly1305-encrypted Keypair w/ {}'s credentials".format( username ))
        keypair			= author( seed=plaintext, why="decrypted w/ {}'s credentials".format( username ))
        return keypair


def author(
    seed	= None,
    why		= None ):
    """Prepare to author Licenses, by creating an Ed25519 keypair."""
    keypair			= ed25519.crypto_sign_keypair( seed )
    log.info( "Created Ed25519 signing keypair  w/ Public key: {vk_b64}{why}".format(
        vk_b64=into_b64( keypair.vk ), why=" ({})".format( why ) if why else "" ))
    return keypair


def issue(
    license,
    author_sigkey,
    signature	= None,
    confirm	= None,
    machine_id_path = None ):
    """If possible, issue the license signed with the supplied signing key. Ensures that the license
    is allowed to be issued, by verifying the signatures of the tree of dependent license(s) if any.

    The holder of an author secret key can issue any license they wish (so long as it is compatible
    with any License dependencies).

    Generally, a license may be issued if it is more "specific" (less general) than any License
    dependencies.  For example, a License could specify that it can be used on *any* 1 installation.
    The holder of the license may then issue a License specifying a certain computer and
    installation path.  The software then confirms successfully that the License is allocated to
    *this* computer, and that the software is installed at the specified location.

    Of course, this is all administrative; any sufficiently dedicated programmer can simply remove
    the License checks from the software.  However, such people are *not* Clients: they are simply
    thieves.  The issuance and checking of Licenses is to help support ethical Clients in confirming
    that they are following the rules of the software author.

    """
    return LicenseSigned(
        license,
        author_sigkey,
        signature	= signature,
        confirm		= confirm,
        machine_id_path	= machine_id_path )


def verify(
    provenance,
    author_pubkey = None,
    signature	= None,
    confirm	= None,
    machine_id_path = None,
    **constraints ):
    """Verify that the supplied License or LicenseSigned contains a valid signature, and that the
    License follows the rules in all of its License dependencies.  Optionally, confirm the validity
    of any public keys.

    Apply any additional constraints, returning a License serialization dict satisfying them.  If
    you plan to issue a new LicenseSigned, it is recommended to include your author, author_domain
    and product names, and perhaps also the client and client_pubkey of the intended License
    recipient.

    Works with either a License and signature= keyword parameter, or a LicenseSigned provenance.

    """
    return provenance.verify(
        author_pubkey	= author_pubkey,
        signature	= signature or provenance.signature,
        confirm		= confirm,
        machine_id_path	= machine_id_path,
        **constraints )

    
def load(
    basename	= None,
    mode	= None,
    extension	= None,
    confirm	= None,
    filename	= None,
    package	= None,
    skip	= "*~",
    **kwds ): # eg. extra=["..."], reverse=False, other open() args; see config_open
    """Open and load all crypto-licens{e,ing} file(s) found on the config path(s) (and any
    extra=[...,...]  paths) containing a LicenseSigned provenance record.  By default, use the
    provided package's (your __package__) name, or the executable filename's (your __file__)
    basename.  Appends .crypto-licensing, if no suffix provided.

    Applies glob pattern matching via config_open....

    Yields the resultant (filename, LicenseSigned) provenance(s), or an Exception if any
    glob-matching file is found that doesn't contain a serialized LicenseSigned.

    """
    name		= deduce_name(
        basename=basename, extension=extension or 'crypto-licens*',
        filename=filename, package=package )
    for f in config_open( name=name, mode=mode, skip=skip, **kwds ):
        with f:
            prov_ser		= f.read()
            prov_name		= f.name
        prov_dict		= json.loads( prov_ser )
        yield prov_name, LicenseSigned( confirm=confirm, **prov_dict )
    

def load_keys(
    basename	= None,
    mode	= None,
    extension	= None,
    filename	= None,
    package	= None,		# For deduction of basename
    username	= None,
    password	= None,		# Decryption credentials to use
    every	= False,
    detail	= True,		# Yield every file? w/ origin + credentials info?
    skip	= "*~",
    **kwds ): # eg. extra=["..."], reverse=False, other open() args; see config_open
    """Load Ed25519 signing Keypair(s) from glob-matching file(s) with any supplied credentials.
    Yields all Encrypted/Plaintext Keypairs successfully opened (may be none at all), as a sequence
    of:

        <filename>, <Keypair{Encrypted,Plaintext}>, <credentials dict>, <Keypair/Exception>

    If every=True, then every file found will be returned with every credential, and an either
    Exception explaining why it couldn't be opened, or the resultant decrypted Ed25519 Keypair.
    Otherwise, only successfully decrypted Keypairs will be returned.

    - Read the plaintext Keypair's public/private keys.
    
      WARNING: Only perform this on action on a secured computer: this file contains your private
      signing key material in plain text form!

    - Load the encrypted seed (w/ a random salt), and:
      - Derive the decryption symmetric cipher key from the salt + username + password

        The plaintext 256-bit Ed25519 private key seed is encrypted using ChaCha20Poly1305 with the
        symmetric cipher key using the (same) salt as a Nonce.  Since the random salt is only (ever)
        used to encrypt one thing, it satisfies the requirement that the same None only ever be used
        once to encrypt something using a certain key.

    - TODO: use a second Keypair's private key to derive a shared secret key

      Optionally, this Signing Keypair's derivation seed can be protected by a symmetric cipher
      key derived from the *public* key of this signing key, and the *private* key of another
      Ed25519 key using the diffie-hellman.  For example, one derived via Argon2 from an email +
      password + salt.

    Therefore, the following deserialized Keypair dicts are supported:

    Unencrypted Keypair:

        {
            "sk":"bw58LSvuadS76jFBCWxkK+KkmAqLrfuzEv7ly0Y3lCLSE2Y01EiPyZjxirwSjHoUf9kz9meeEEziwk358jthBw=="
            "vk":"qZERnjDZZTmnDNNJg90AcUJZ+LYKIWO9t0jz/AzwNsk="
        }

    Unencrypted Keypair from just 256-bit seed (which is basically the first half of a full .sk
    signing key with a few bits normalized), and optional public key .vk to verify:

        {
            "seed":"bw58LSvuadS76jFBCWxkK+KkmAqLrfuzEv7ly0Y3lC=",
            "vk":"qZERnjDZZTmnDNNJg90AcUJZ+LYKIWO9t0jz/AzwNsk="
        }

    384-bit ChaCha20Poly1503-Encrypted seed (ya, don't use a non-random salt...):
        {
            "salt":"000000000000000000000000",
            "ciphertext":"d211f72ba97e9cdb68d864e362935a5170383e70ea10e2307118c6d955b814918ad7e28415e2bfe66a5b34dddf12d275"
        }

    NOTE: For encrypted Keypairs, we do not need to save the "derivation" we use to arrive at
    the cryptographic key from the salt + username + password, since the encryption used includes a
    MAC; we try each supported derivation.

    """
    issues			= []
    found			= 0
    name		= deduce_name(
        basename=basename, extension=extension or 'crypto-keypair*', filename=filename, package=package )
    for f in config_open( name=name, mode=mode, skip=skip, **kwds ):
        try:
            with f:
                f_name		= f.name
                f_ser		= f.read()
            log.isEnabledFor( logging.DEBUG ) and log.debug( "Read Keypair... data from {}: {}".format( f_name, f_ser ))
            keypair_dict		= json.loads( f_ser )
        except Exception as exc:
            log.debug( "Failure to load KeypairEncrypted/Plaintext from {}: {}".format(
                f_name, exc ))
            issues.append( (f_name, exc ) )
            continue
        # Attempt to recover the different Keypair...() types, from most stringent requirements to least.
        encrypted		= None
        try:
            encrypted		= KeypairEncrypted( username=username, password=password, **keypair_dict )
            keypair		= encrypted.into_keypair( username=username, password=password )
            log.info( "Recover Ed25519 KeypairEncrypted w/ Public key: {} (from {}) w/ credentials {} / {}".format(
                into_b64( keypair.vk ), f_name, username, '*' * len( password )))
            if detail:
                yield f_name, encrypted, dict( username=username, password=password ), keypair
            else:
                yield f_name, keypair
            found	       += 1
            continue
        except KeypairCredentialError as exc:
            # The KeypairEncrypted was OK -- just the credentials were wrong; don't bother trying as non-Encrypted
            issues.append( (f_name, exc) )
            if every:
                if detail:
                    yield f_name, encrypted, dict( username=username, password=password ), exc
                else:
                    yield f_name, exc
            log.isEnabledFor( logging.DEBUG ) and log.debug(
                "Failed to decrypt KeypairEncrypted: {trace}".format(
                    trace=''.join( traceback.format_exception( *sys.exc_info() )) if log.isEnabledFor( logging.DEBUG ) else exc ))
            continue
        except Exception:
            # Some other problem attempting to interpret this thing as a KeypairEncrypted; carry on and try again
            log.isEnabledFor( logging.DEBUG ) and log.debug(
                "Failed to decode  KeypairEncrypted: {trace}".format(
                    trace=''.join( traceback.format_exception( *sys.exc_info() ))))

        plaintext		= None
        try:
            plaintext		= KeypairPlaintext( **keypair_dict )
            keypair		= plaintext.into_keypair()
            log.isEnabledFor( logging.DEBUG ) and log.debug(
                "Recover Ed25519 KeypairPlaintext w/ Public key: {} (from {})".format(
                    into_b64( keypair.vk ), f_name ))
            if detail:
                yield f_name, plaintext, {}, keypair
            else:
                yield f_name, keypair
            found	       += 1
            continue
        except Exception as exc:
            # Some other problem attempting to interpret as a KeypairPlaintext
            issues.append( (f_name, exc) )
            if every:
                if detail:
                    yield f_name, plaintext, {}, exc
                else:
                    yield f_name, exc
            log.isEnabledFor( logging.DEBUG ) and log.debug(
                "Failed to decode KeypairPlaintext: {}".format(
                    ''.join( traceback.format_exception( *sys.exc_info() )) if log.isEnabledFor( logging.DEBUG ) else exc ))
    if not found:
        log.info( "Cannot load Keypair(s) from {name}: {reasons}".format(
            name=name, reasons=', '.join( "{}: {}".format( fn, exc ) for fn, exc in issues )))


def check( basename=None, mode=None,		# Keypair/License file basename and open mode
           extension_keypair=None, extension_license=None,
           filename=None, package=None,		#   or, deduce basename from supplied data
           username=None, password=None,	# Keypair protected w/ supplied credentials
           skip="*~", **kwds ): # eg. extra=["..."], reverse=False, other open() args; see config_open               **kwds ):
    """Check that a License has been issued with the desired features.  If none founds, attempt to
    obtain one.  Can deduce a basename from provided filename/package, if desired

    - Load our Ed25519 Keypair
      - Create one, if not found
    - Load our Licenses
      - Obtain one, if not found

    If an Ed25519 Agent signing authority or License must be created, the default location where
    they will be stored is in the most general Cpppo configuration location that is writable.

    Agent signing authority is usually machine-specific: a License to run a program on one machine
    usually doesn't transfer to another machine.  

    <basename>-<machine-id>.crypto-keypair...
    <basename>-<machine-id>.crypto-license...

    """
    keypairs		= dict( (name, keypair_or_error)
                                for name, keypair_typed, cred, keypair_or_error in load_keys(
                                        basename=basename, mode=mode, extension=extension_keypair,
                                        filename=filename, package=package,
                                        every=True, detail=True,
                                        username=username, password=password,
                                        skip=skip, **kwds ))
    log.debug( "Name          Keypair/Error" )
    for n,k_e in keypairs.items():
        log.debug( "{:48} {}".format( os.path.basename( n ), k_e ))
