#!/usr/bin/env bash

if [ $EUID != 0 ]; then
    sudo -E "$0" "$@"
    exit $?
fi

usage="$(basename "$0") [-h] [-d domain] [-c client] -- generate MQTT keys

where:
    -h  show this help text
    -d  domain for CA certificate
    -c  name of the client user"

while getopts ':h:d:c:' option; do
  case "$option" in
    h) echo "$usage"
       exit
       ;;
    d) DOMAIN="$OPTARG"
       ;;
    c) CLIENTNAME="$OPTARG"
       ;;
    :) printf "missing argument for -%s\n" "$OPTARG" >&2
       echo "$usage" >&2
       exit 1
       ;;
   \?) printf "illegal option: -%s\n" "$OPTARG" >&2
       echo "$usage" >&2
       exit 1
       ;;
  esac
done
shift $((OPTIND - 1))

if [ -z "${DOMAIN}" ] || [ -z "${CLIENTNAME}" ]; then
    echo "$usage" >&2
    exit 1
fi

pushd `dirname $0` > /dev/null
SCRIPTDIR="`pwd -P`"
popd > /dev/null

CERT_PATH="$(readlink -m ${SCRIPTDIR}/../../ssl)"
CA_CERT="${CERT_PATH}/certs/ca.crt"
CA_KEY="${CERT_PATH}/private/ca.key"

if [ ! -f "$CA_CERT" ]; then
    echo "Unable to read certificate file: ${CA_CERT}" >&2
    exit 1
fi

if [ ! -f "$CA_KEY" ]; then
    echo "Unable to read certificate private key: ${CA_KEY}" >&2
    exit 1
fi

CLIENTDIR="$(readlink -m ${SCRIPTDIR}/../../ssl/private/$CLIENTNAME)"

if [ ! -d "$CLIENTDIR" ]; then
    sudo -u `logname` mkdir -p "$CLIENTDIR"
fi


CLIENT="$CLIENTDIR/$CLIENTNAME"

defaultmd="-sha512"
keybits=2048
openssl=$(which openssl)


function maxdays() {
    nowyear=$(date +%Y)
    years=$(expr 2032 - $nowyear)
    days=$(expr $years '*' 365)

    echo $days
}

days=$(maxdays)

if [ ! -f $CLIENT.key ]; then
    echo "--- Creating client key and signing request"
    $openssl genrsa -out $CLIENT.key $keybits

    CNF=`mktemp /tmp/cacnf-req.XXXXXXXX` || { echo "$0: can't create temp file" >&2; exit 1; }
    # Mosquitto's use_identity_as_username takes the CN attribute
    # so we're populating that with the client's name
    sed -e 's/^.*%%% //' > $CNF <<!ENDClientconfigREQ
    %%% [ req ]
    %%% distinguished_name = req_distinguished_name
    %%% prompt             = no
    %%% output_password    = secret
    %%% 
    %%% [ req_distinguished_name ]
    %%% CN                 = $CLIENTNAME
!ENDClientconfigREQ

    $openssl req -new $defaultmd \
        -out $CLIENT.csr \
        -key $CLIENT.key \
        -config $CNF

    chown `logname` $CLIENT.key
    chmod 400 $CLIENT.key
    chown `logname` $CLIENT.csr
fi


if [ -f $CLIENT.csr -a ! -f $CLIENT.crt ]; then

    CNF=`mktemp /tmp/cacnf-cli.XXXXXXXX` || { echo "$0: can't create temp file" >&2; exit 1; }
    sed -e 's/^.*%%% //' > $CNF <<\!ENDClientconfig
    %%% [ JPMclientextensions ]
    %%% basicConstraints        = critical,CA:false
    %%% subjectAltName          = email:copy
    %%% nsCertType              = client,email
    %%% extendedKeyUsage        = clientAuth,emailProtection
    %%% keyUsage                = digitalSignature, keyEncipherment, keyAgreement
    %%% nsComment               = "Client Broker Certificate"
    %%% subjectKeyIdentifier    = hash
    %%% authorityKeyIdentifier  = keyid,issuer:always

!ENDClientconfig

    echo "--- Creating and signing client certificate"
    $openssl x509 -req $defaultmd \
        -in $CLIENT.csr \
        -CA "$CA_CERT" \
        -CAkey "$CA_KEY" \
        -CAcreateserial \
        -out $CLIENT.crt \
        -days $days \
        -extfile ${CNF} \
        -extensions JPMclientextensions

    rm -f $CNF
    chown `logname` $CLIENT.crt
    chmod 444 $CLIENT.crt
fi


if [ -f $CLIENT.crt -a ! -f $CLIENT.p12 ]; then

    export SUBJALTNAME="DNS:$DOMAIN"

    echo "--- Converting client certificates to PKCS"
    $openssl pkcs12 -export -clcerts \
        -in $CLIENT.crt \
        -inkey $CLIENT.key \
        -out $CLIENT.p12

    chown `logname` $CLIENT.p12
    chmod 444 $CLIENT.p12
fi
