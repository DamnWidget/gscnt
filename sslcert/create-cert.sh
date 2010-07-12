#!/bin/bash

CACERT="cacert.pem"
CAPWD="a\$las\$barricadas"

if [ ! -n "$2" ]
then
    echo "Uso: `basename $0` nombre p12nombre"
    exit -1
fi

# Crear key y peticion de firma
echo "Creando clave y peticion de firma..."
openssl req -new -nodes -extensions v3_req -out $1-req.pem -keyout private/$1-key.pem -days 1095 -config ./openssl.cnf

# Firmar la peticion con el CA
echo
echo "Firmando la peticion con la entidad certificadora (necesita el password de la entidad certificadora)..."
openssl ca -out $1-cert.pem -days 1095 -extensions v3_req -config ./openssl.cnf -infiles $1-req.pem

# Generar el archivo PKCS12
echo
echo "Generando archivo de identidad PKCS12 para $1..."
openssl pkcs12 -export -in $1-cert.pem -inkey private/$1-key.pem -certfile cacert.pem -name "$2" -out $1-cert.p12

echo
echo "Certificado Digital creado con éxito"
echo "Si desea generar una clave privada sin requerimiento de password use:"
echo "openssl rsa -in private/$1-key.pem -out private/$1-key.rsa"
echo