

POSITIONAL=()
while [[ $# -gt 0 ]]
do
key="$1"

case $key in
    -E|--Extract)
    EXTRACT="$2"
    shift # past argument
    shift # past value
    ;;
    -s|--secret)
    SECRET="$2"
    shift # past argument
    shift # past value
    ;;
    -i|--image)
    IMAGE="$2"
    shift # past argument
    shift # past value
    ;;
    *)    # unknown option
    POSITIONAL+=("$1") # save it in an array for later
    shift # past argument
    ;;
esac
done
set -- "${POSITIONAL[@]}" # restore positional parameters

if [[ -z "${EXTRACT}" ]]
then
    echo "We are going to hide the ${SECRET} in ${IMAGE}"
    python stego.py -i "${IMAGE}" -s secret "${SECRET}"
    python examples/http3_server.py --certificate tests/ssl_cert.pem --private-key tests/ssl_key.pem -v
else
    echo "We are going to download and extract the ${IMAGE}'s secret"
    python examples/http3_client.py --ca-certs tests/pycacert.pem https://localhost:4433/stego
    python stego.py -E -i "${IMAGE}"
fi


