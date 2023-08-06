# -*- coding: utf-8 -*-

import binascii
import codecs
import copy
import json
import logging
import os
import pytest

try:
    import chacha20poly1305
except ImportError:
    chacha20poly1305		= None

from dns.exception import DNSException
from .verification import (
    License, LicenseSigned, LicenseIncompatibility, Timespan,
    KeypairPlaintext, KeypairEncrypted, machine_UUIDv4,
    domainkey, domainkey_service, overlap_intersect,
    into_b64, into_hex, into_str, into_str_UTC, into_JSON, into_keys,
    into_timestamp, into_duration,
    author, issue, verify, load, load_keys, check,
)
from .. import ed25519

from ..misc import parse_datetime, parse_seconds, Timestamp, Duration


log				= logging.getLogger( "verification_test" )

dominion_sigkey			= binascii.unhexlify(
    '431f3fb4339144cb5bdeb77db3148a5d340269fa3bc0bf2bf598ce0625750fdca991119e30d96539a70cd34983dd00714259f8b60a2163bdb748f3fc0cf036c9' )
awesome_sigkey			= binascii.unhexlify(
    '4e4d27b26b6f4db69871709d68da53854bd61aeee70e63e3b3ff124379c1c6147321ce7a2fb87395fe0ff9e2416bc31b9a25475aa2e2375d70f4c326ffd47eb4' )
enduser_seed			= binascii.unhexlify( '00' * 32 )

username			= 'a@b.c'
password			= 'password'

machine_id_path			= __file__.replace( ".py", ".machine-id" )


def test_License_domainkey():
    """Ensure we can handle arbitrary UTF-8 domains, and compute the proper DKIM1 RR path"""
    assert domainkey_service( u"π" ) == 'xn--1xa'
    assert domainkey_service( u"π/1" ) ==  'xn---1-lbc'

    path, dkim_rr = domainkey( u"Some Product", "example.com" )
    assert path == 'some-product.crypto-licensing._domainkey.example.com.'
    assert dkim_rr is None
    author_keypair = author( seed=b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA' )
    path, dkim_rr = domainkey( u"ᛞᚩᛗᛖᛋ᛫ᚻᛚᛇᛏᚪᚾ᛬", "awesome-inc.com", pubkey=author_keypair )
    assert path == 'xn--dwec4cn7bwa4a4ci7a1b2lta.crypto-licensing._domainkey.awesome-inc.com.'
    assert dkim_rr == 'v=DKIM1; k=ed25519; p=25lf4lFp0UHKubu6krqgH58uHs599MsqwFGQ83/MH50='


def test_License_overlap():
    """A License can only issued while all the sub-Licenses are valid.  The start/length should "close"
    to encompass the start/length of any dependencies sub-Licenses, and any supplied constraints.

    """
    other = Timespan(
        Timestamp( parse_datetime( '2021-01-01 00:00:00 Canada/Pacific' )),
        Duration( '1w' )
    )
    start,length,begun,ended = overlap_intersect( None, None, other )
    assert into_str_UTC( start ) == "2021-01-01 08:00:00 UTC"
    assert into_str( length ) == "1w"
    assert into_str_UTC( begun ) == "2021-01-01 08:00:00 UTC"
    assert into_str_UTC( ended ) == "2021-01-08 08:00:00 UTC"

    start = into_timestamp( '2021-01-01 00:00:00 Canada/Pacific' )
    length = into_duration( "1w" )
    start,length,begun,ended = overlap_intersect( start, length, Timespan( None, None ))
    assert into_str_UTC( start ) == "2021-01-01 08:00:00 UTC"
    assert into_str( length ) == "1w"
    assert into_str_UTC( begun ) == "2021-01-01 08:00:00 UTC"
    assert into_str_UTC( ended ) == "2021-01-08 08:00:00 UTC"


def test_KeypairPlaintext_smoke():
    enduser_keypair		= author( seed=enduser_seed, why="from enduser seed" )
    kp_p			= KeypairPlaintext( sk=into_b64( enduser_seed ), vk=into_b64( enduser_keypair.vk ))
    kp_p_ser			= str( kp_p )
    assert kp_p_ser == """\
{
    "sk":"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA7aie8zrakLWKjqNAqbw1zZTIVdx3iQ6Y6wEihi1naKQ==",
    "vk":"O2onvM62pC1io6jQKm8Nc2UyFXcd4kOmOsBIoYtZ2ik="
}"""
    kp_p_rec			= KeypairPlaintext( **json.loads( kp_p_ser ))
    assert str( kp_p_rec ) == kp_p_ser

    # We can also recover with various subsets of sk, vk
    kp_p2			= KeypairPlaintext( sk=kp_p.sk[:32] )
    kp_p3			= KeypairPlaintext( sk=kp_p.sk[:64] )
    kp_p4			= KeypairPlaintext( sk=kp_p.sk[:64], vk=kp_p.vk )

    assert str( kp_p2 ) == str( kp_p3 ) == str( kp_p4 )

    # And see if we can copy Serializable things properly
    kp_c1			= copy.copy( kp_p4 )
    assert str( kp_c1 ) == str( kp_p4 )


@pytest.mark.skipif( not chacha20poly1305, reason="Needs ChaCha20Poly1305" )
def test_KeypairEncrypted_smoke():
    enduser_keypair		= author( seed=enduser_seed, why="from enduser seed" )
    salt			= b'\x00' * 12
    kp_e			= KeypairEncrypted(
        salt		= salt,
        sk		= enduser_keypair.sk,
        username	= username,
        password	= password
    )
    assert kp_e.into_keypair( username=username, password=password ) == enduser_keypair

    kp_e_ser			= str( kp_e )
    assert kp_e_ser == """\
{
    "ciphertext":"d211f72ba97e9cdb68d864e362935a5170383e70ea10e2307118c6d955b814918ad7e28415e2bfe66a5b34dddf12d275",
    "salt":"000000000000000000000000"
}"""
    kp_r			= KeypairEncrypted( **json.loads( kp_e_ser ))
    assert str( kp_r ) == kp_e_ser

    # We can also reconstruct from just seed and salt
    kp_e2			= KeypairEncrypted( salt=salt, ciphertext=kp_e.ciphertext )
    assert str( kp_e2 ) == kp_e_ser
    assert kp_e.into_keypair( username=username, password=password ) \
        == kp_r.into_keypair( username=username, password=password ) \
        == kp_e2.into_keypair( username=username, password=password )

    awesome_keypair		= into_keys( awesome_sigkey )
    kp_a			= KeypairEncrypted(
        salt		= b'\x01' * 12,
        sk		= awesome_keypair[1],
        username	= username,
        password	= password
    )
    assert kp_a.into_keypair( username=username, password=password )[1] == awesome_keypair[1]

    kp_a_ser			= str( kp_a )
    assert """\
{
    "ciphertext":"aea5129b033c3072be503b91957dbac0e4c672ab49bb1cc981a8955ec01dc47280effc21092403509086caa8684003c7",
    "salt":"010101010101010101010101"
}""" == kp_a_ser


@pytest.mark.skipif( not chacha20poly1305, reason="Needs ChaCha20Poly1305" )
def test_KeypairEncrypted_load_keys():
    enduser_keypair		= author( seed=enduser_seed, why="from enduser seed" )
    # load just the one encrypted cpppo-keypair (no glob wildcard on extension)
    (keyname,keypair_encrypted,keycred,keypair), = load_keys(
        extension="crypto-keypair", username=username, password=password,
        extra=[os.path.dirname( __file__ )], filename=__file__ )
    assert keycred == dict( username=username, password=password )
    assert enduser_keypair == keypair_encrypted.into_keypair( **keycred ) == keypair


def test_KeypairPlaintext_load_keys():
    enduser_keypair		= author( seed=enduser_seed, why="from enduser seed" )
    (keyname,keypair_plaintext,keycred,keypair), = load_keys(
        extension="crypto-keypair-plaintext",
        extra=[os.path.dirname( __file__ )], filename=__file__ )
    assert keycred == {}
    assert enduser_keypair == keypair_plaintext.into_keypair( **keycred ) == keypair


def test_License_serialization():
    # Dedduce the basename from our __file__ (note: this is destructuring a 1-element sequence from a
    # generator!)
    (provname,prov), = load( extra=[os.path.dirname( __file__ )], filename=__file__, confirm=False )
    with open( os.path.join( os.path.dirname( __file__ ), "verification_test.crypto-license" )) as f:
        assert str( prov ) == f.read()


def test_License_base():
    confirm		= True
    try:
        lic = License(
            author	= dict(
                domain	= "dominionrnd.com",
                name	= "Dominion Research & Development Corp.",
                product	= "Cpppo Test",
            ),
            start	= "2021-09-30 11:22:33 Canada/Mountain",
            length	= "1y" )
    except DNSException as exc:
        # No DNS; OK, let the test pass anyway.
        log.warning( "No DNS; disabling crypto-licensing DKIM confirmation for test: {}".format( exc ))
        confirm		= False
        lic = License(
            author	= dict(
                domain	= "dominionrnd.com",
                name	= "Dominion Research & Development Corp.",
                product	= "Cpppo Test",
                pubkey	= dominion_sigkey[32:],
            ),
            start	= "2021-09-30 11:22:33 Canada/Mountain",
            length	= "1y",
            confirm	= confirm )

    lic_str = str( lic )
    assert lic_str == """\
{
    "author":{
        "domain":"dominionrnd.com",
        "name":"Dominion Research & Development Corp.",
        "product":"Cpppo Test",
        "pubkey":"qZERnjDZZTmnDNNJg90AcUJZ+LYKIWO9t0jz/AzwNsk="
    },
    "length":"1y",
    "start":"2021-09-30 17:22:33 UTC"
}"""
    lic_digest_b64 = 'sizNU873WbB5d5EZ6lT3Z4319D4wTzsvcLfzl+wItWE='
    assert lic_digest_b64 == lic.digest('base64', 'ASCII' )
    if lic_digest_b64 == lic.digest('base64', 'ASCII' ):
        #print( repr( lic.digest() ))
        assert lic.digest() == b'\xb2,\xcdS\xce\xf7Y\xb0yw\x91\x19\xeaT\xf7g\x8d\xf5\xf4>0O;/p\xb7\xf3\x97\xec\x08\xb5a'
        assert lic.digest('hex', 'ASCII' ) == 'b22ccd53cef759b079779119ea54f7678df5f43e304f3b2f70b7f397ec08b561'

    keypair = ed25519.crypto_sign_keypair( dominion_sigkey[:32] )
    assert keypair.sk == dominion_sigkey
    assert b'\xa9\x91\x11\x9e0\xd9e9\xa7\x0c\xd3I\x83\xdd\x00qBY\xf8\xb6\n!c\xbd\xb7H\xf3\xfc\x0c\xf06\xc9' == lic.author.pubkey
    assert codecs.getencoder( 'base64' )( keypair.vk ) == (b'qZERnjDZZTmnDNNJg90AcUJZ+LYKIWO9t0jz/AzwNsk=\n', 32)
    prov = LicenseSigned( lic, keypair.sk, confirm=confirm )

    machine_uuid = machine_UUIDv4( machine_id_path=machine_id_path )
    assert machine_uuid.hex == "000102030405460788090a0b0c0d0e0f"
    assert machine_uuid.version == 4

    prov_str = str( prov )
    assert prov_str == """\
{
    "license":{
        "author":{
            "domain":"dominionrnd.com",
            "name":"Dominion Research & Development Corp.",
            "product":"Cpppo Test",
            "pubkey":"qZERnjDZZTmnDNNJg90AcUJZ+LYKIWO9t0jz/AzwNsk="
        },
        "length":"1y",
        "start":"2021-09-30 17:22:33 UTC"
    },
    "signature":"V+VI/JXX/ZuypAo2nJHKme4VFjhJpWRzQbUFV9NMqIaLHiQYltQgfoLmQD11zcw+oxemnEPrZg+UJm4rJwiICg=="
}"""
    # Multiple licenses, some of which truncate the duration of the initial License. Non-timezone
    # timestamps are assumed to be UTC.  These are fake domains, so no confirm.
    start, length = lic.overlap(
        License( author = dict( name="A", product='a', domain='a-inc.com', pubkey=keypair.vk ), confirm=False,
                 start = "2021-09-29 00:00:00", length = "1w" ),
        License( author = dict( name="B", product='b', domain='b-inc.com', pubkey=keypair.vk ), confirm=False,
                 start = "2021-09-30 00:00:00", length = "1w" ))
    # Default rendering of a timestamp is w/ milliseconds, and no tz info for UTC
    assert str( start ) == "2021-09-30 11:22:33.000 Canada/Mountain"
    assert str( length ) == "5d6h37m27s"

    # Attempt to find overlap between non-overlapping Licenses.  Uses the local timezone for
    # rendering; force by setting environment variable TZ=Canada/Mountain for this test!
    with pytest.raises( LicenseIncompatibility ) as exc_info:
        start, length = lic.overlap(
            License( author = dict( name="A", product='a', domain='a-inc.com', pubkey=keypair.vk ), confirm=False,
                     start = "2021-09-29 00:00:00", length = "1w" ),
            License( author = dict( name="B", product='b', domain='b-inc.com', pubkey=keypair.vk ), confirm=False,
                     start = "2021-10-07 00:00:00", length = "1w" ))
    assert str( exc_info.value ).endswith(
        "License for B's 'b' from 2021-10-06 18:00:00 Canada/Mountain for 1w incompatible with others" )


def test_LicenseSigned():
    """Tests Licenses derived from other License dependencies."""
    awesome_keypair = author( seed=awesome_sigkey[:32] )
    awesome_pubkey, _ = into_keys( awesome_keypair )

    print("Awesome, Inc. ed25519 keypair; Signing: {sk}".format( sk=binascii.hexlify( awesome_keypair.sk )))
    print("Awesome, Inc. ed25519 keypair; Public:  {pk_hex} == {pk}".format( pk_hex=into_hex( awesome_keypair.vk ), pk=into_b64( awesome_keypair.vk )))

    confirm			= True
    try:
        # If we're connected to the Internet and can check DNS, lets try to confirm that DKIM public
        # key checking works properly.  First, lets try to create a License with the *wrong* public
        # key (doesn't match DKIM record in DNS).

        with pytest.raises( LicenseIncompatibility ) as exc_info:
            License(
                author	= dict(
                    name	= "Dominion Research & Development Corp.",
                    product	= "Cpppo Test",
                    domain	= "dominionrnd.com",
                    pubkey	= awesome_pubkey,  # Purposely *wrong*; will not match cpppo-test.cpppo-licensing.. DKIM entry
                ),
                client	= dict(
                    name	= "Awesome, Inc.",
                    pubkey	= awesome_pubkey
                ),
                start	= "2021-09-30 11:22:33 Canada/Mountain",
                length	= "1y" )
        assert str( exc_info.value ).endswith(
            """License for Dominion Research & Development Corp.'s 'Cpppo Test': author key from DKIM qZERnjDZZTmnDNNJg90AcUJZ+LYKIWO9t0jz/AzwNsk= != cyHOei+4c5X+D/niQWvDG5olR1qi4jddcPTDJv/UfrQ=""" )

        lic = License(
            author	= dict(
                name	= "Dominion Research & Development Corp.",
                product	= "Cpppo Test",
                domain	= "dominionrnd.com",
            ),
            client	= dict(
                name	= "Awesome, Inc.",
                pubkey	= awesome_pubkey,
            ),
            start	= "2021-09-30 11:22:33 Canada/Mountain",
            length	= "1y" )
    except DNSException as exc:
        # No DNS; OK, let the test pass anyway.
        log.warning( "No DNS; disabling crypto-licensing DKIM confirmation for test: {}".format( exc ))
        confirm		= False
        lic = License(
            author	= dict(
                name	= "Dominion Research & Development Corp.",
                product	= "Cpppo Test",
                domain	= "dominionrnd.com",
                pubkey	= dominion_sigkey[32:],  # This is the correct key, which matches the DKIM entry
            ),
            client	= dict(
                name	= "Awesome, Inc.",
                pubkey	= awesome_pubkey,
            ),
            start	= "2021-09-30 11:22:33 Canada/Mountain",
            length	= "1y",
            confirm	= confirm )
    # Obtain a signed Cpppo license for 2021-09-30 + 1y
    lic_prov = issue( lic, dominion_sigkey, confirm=confirm )

    # Create a signing key for Awesome, Inc.; securely hide it (or, print it for everyone to see,
    # just below! ;), and publish the base-64 encoded public key as a TXT RR at:
    # 
    #     ethernet-ip-tool.crypto-licensing._domainkey.awesome.com 300 IN TXT \
    #        "v=DKIM1; k=ed25519; p=PW847szICqnQBzbdr5TAoGO26RwGxG95e3Vd/M+/GZc="
    #
    enduser_keypair		= author( seed=enduser_seed, why="from enduser seed" )
    enduser_pubkey, enduser_sigkey = into_keys( enduser_keypair )
    print("End User, LLC ed25519 keypair; Signing: {sk}".format( sk=into_hex( enduser_keypair.sk )))
    print("End User, LLC ed25519 keypair; Public:  {pk_hex} == {pk}".format( pk_hex=into_hex( enduser_keypair.vk ), pk=into_b64( enduser_keypair.vk )))

    # Almost at the end of their annual Cpppo license, they issue a new License to End User, LLC for
    # their Awesome EtherNet/IP Tool.
    drv = License(
        author	= dict(
            name	= "Awesome, Inc.",
            product	= "EtherNet/IP Tool",
            domain	= "awesome-inc.com",
            pubkey	= awesome_keypair.vk  # Avoid the dns.resolver.NXDOMAIN by providing the pubkey
        ),
        client = dict(
            name	= "End User, LLC",
            pubkey	= enduser_pubkey
        ),
        dependencies = [ lic_prov ],
        start	= "2022-09-29 11:22:33 Canada/Mountain",
        length	= "1y",
        confirm = False,
    )
    drv_prov = issue( drv, awesome_keypair.sk, confirm=False )
    assert 'ZGoigaaA2xOl5Aw23nDkq2BpKpj3RvjDtPAr19Mupz8=' == drv_prov.b64digest()
    drv_prov_str = str( drv_prov )
    #print(drv_prov_str)
    assert """\
{
    "license":{
        "author":{
            "domain":"awesome-inc.com",
            "name":"Awesome, Inc.",
            "product":"EtherNet/IP Tool",
            "pubkey":"cyHOei+4c5X+D/niQWvDG5olR1qi4jddcPTDJv/UfrQ="
        },
        "client":{
            "name":"End User, LLC",
            "pubkey":"O2onvM62pC1io6jQKm8Nc2UyFXcd4kOmOsBIoYtZ2ik="
        },
        "dependencies":[
            {
                "license":{
                    "author":{
                        "domain":"dominionrnd.com",
                        "name":"Dominion Research & Development Corp.",
                        "product":"Cpppo Test",
                        "pubkey":"qZERnjDZZTmnDNNJg90AcUJZ+LYKIWO9t0jz/AzwNsk="
                    },
                    "client":{
                        "name":"Awesome, Inc.",
                        "pubkey":"cyHOei+4c5X+D/niQWvDG5olR1qi4jddcPTDJv/UfrQ="
                    },
                    "length":"1y",
                    "start":"2021-09-30 17:22:33 UTC"
                },
                "signature":"9DbaJRrEm9krviJfhhPkFoH/LtN1uYG48xA/4CTe4ZcXQOhCfnc/HhpcO0kR1t5EzWt27U7SBYr2IwVpHAkLCg=="
            }
        ],
        "length":"1y",
        "start":"2022-09-29 17:22:33 UTC"
    },
    "signature":"KKMNf9Ds9uJYIrwBoFRjP3F1vt8d1bp7jYWlM0kn+hkMoJViI9BvMY923MjwgV9iMhYbiC6hfD3s28ULVK2KDA=="
}""" == drv_prov_str

    # Test the cpppo.crypto.licensing API, as used in applications.  A LicenseSigned is saved to an
    # <application>.crypto-license file in the Application's configuration directory path.  The
    # process for deploying an application onto a new host:
    #
    # 1) Install software to target directory
    # 2) Obtain serialized LicenseSigned containing necessary License(s)
    #    - This is normally done in a company License Server, which holds the
    #      master license and issues specialized ones up to the purchased limits (eg. 10 machines)
    # 3) Derive a new License, specialized for the host's machine-id UUID
    #    - This will be a LicenseSigned by the company License server using the company's key,
    #    - It's client_pubkey will match this software installation's private key, and machine-id UUID
    # 4) Save to <application>.crypto-license in application's config path

    # Lets specialize the license for a specific machine, and with a specific start time
    lic_host_dict		= verify(
        drv_prov, confirm=False, machine=True, machine_id_path=machine_id_path,
        start="2022-09-28 08:00:00 Canada/Mountain"
    )
    #print( into_JSON( lic_host_dict, indent=4, default=str ))
    assert """\
{
    "dependencies":[
        {
            "license":{
                "author":{
                    "domain":"awesome-inc.com",
                    "name":"Awesome, Inc.",
                    "product":"EtherNet/IP Tool",
                    "pubkey":"cyHOei+4c5X+D/niQWvDG5olR1qi4jddcPTDJv/UfrQ="
                },
                "client":{
                    "name":"End User, LLC",
                    "pubkey":"O2onvM62pC1io6jQKm8Nc2UyFXcd4kOmOsBIoYtZ2ik="
                },
                "dependencies":[
                    {
                        "license":{
                            "author":{
                                "domain":"dominionrnd.com",
                                "name":"Dominion Research & Development Corp.",
                                "product":"Cpppo Test",
                                "pubkey":"qZERnjDZZTmnDNNJg90AcUJZ+LYKIWO9t0jz/AzwNsk="
                            },
                            "client":{
                                "name":"Awesome, Inc.",
                                "pubkey":"cyHOei+4c5X+D/niQWvDG5olR1qi4jddcPTDJv/UfrQ="
                            },
                            "length":"1y",
                            "start":"2021-09-30 17:22:33 UTC"
                        },
                        "signature":"9DbaJRrEm9krviJfhhPkFoH/LtN1uYG48xA/4CTe4ZcXQOhCfnc/HhpcO0kR1t5EzWt27U7SBYr2IwVpHAkLCg=="
                    }
                ],
                "length":"1y",
                "start":"2022-09-29 17:22:33 UTC"
            },
            "signature":"KKMNf9Ds9uJYIrwBoFRjP3F1vt8d1bp7jYWlM0kn+hkMoJViI9BvMY923MjwgV9iMhYbiC6hfD3s28ULVK2KDA=="
        }
    ],
    "length":"1d6h",
    "machine":"00010203-0405-4607-8809-0a0b0c0d0e0f",
    "start":"2022-09-29 17:22:33 UTC"
}""" == into_JSON( lic_host_dict, indent=4, default=str )

    lic_host			= License(
        author	= dict(
            name	= "End User",
            product	= "application",
            pubkey	= enduser_keypair
        ),
        confirm		= False,
        machine_id_path	= machine_id_path,
        **lic_host_dict
    )
    lic_host_prov = issue( lic_host, enduser_keypair, confirm=False, machine_id_path=machine_id_path )
    lic_host_str = str( lic_host_prov )
    #print( lic_host_str )
    assert """\
{
    "license":{
        "author":{
            "name":"End User",
            "product":"application",
            "pubkey":"O2onvM62pC1io6jQKm8Nc2UyFXcd4kOmOsBIoYtZ2ik="
        },
        "dependencies":[
            {
                "license":{
                    "author":{
                        "domain":"awesome-inc.com",
                        "name":"Awesome, Inc.",
                        "product":"EtherNet/IP Tool",
                        "pubkey":"cyHOei+4c5X+D/niQWvDG5olR1qi4jddcPTDJv/UfrQ="
                    },
                    "client":{
                        "name":"End User, LLC",
                        "pubkey":"O2onvM62pC1io6jQKm8Nc2UyFXcd4kOmOsBIoYtZ2ik="
                    },
                    "dependencies":[
                        {
                            "license":{
                                "author":{
                                    "domain":"dominionrnd.com",
                                    "name":"Dominion Research & Development Corp.",
                                    "product":"Cpppo Test",
                                    "pubkey":"qZERnjDZZTmnDNNJg90AcUJZ+LYKIWO9t0jz/AzwNsk="
                                },
                                "client":{
                                    "name":"Awesome, Inc.",
                                    "pubkey":"cyHOei+4c5X+D/niQWvDG5olR1qi4jddcPTDJv/UfrQ="
                                },
                                "length":"1y",
                                "start":"2021-09-30 17:22:33 UTC"
                            },
                            "signature":"9DbaJRrEm9krviJfhhPkFoH/LtN1uYG48xA/4CTe4ZcXQOhCfnc/HhpcO0kR1t5EzWt27U7SBYr2IwVpHAkLCg=="
                        }
                    ],
                    "length":"1y",
                    "start":"2022-09-29 17:22:33 UTC"
                },
                "signature":"KKMNf9Ds9uJYIrwBoFRjP3F1vt8d1bp7jYWlM0kn+hkMoJViI9BvMY923MjwgV9iMhYbiC6hfD3s28ULVK2KDA=="
            }
        ],
        "length":"1d6h",
        "machine":"00010203-0405-4607-8809-0a0b0c0d0e0f",
        "start":"2022-09-29 17:22:33 UTC"
    },
    "signature":"8m+gfL5qPd7XPc1N87tPm9noDSOU5f1ToeN6NuQO9vYS+xca6hkUuZPdUjQ9/jcjNrj8IGeGYzoPIIUQ/LxcAw=="
}""" == lic_host_str


def test_licensing_check():
    check( extra=[os.path.dirname( __file__ )],
           filename=__file__, package=__package__,  # filename takes precedence
           username="a@b.c", password="passwor" )
