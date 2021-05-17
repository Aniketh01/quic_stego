

POSITIONAL=()
while [[ $# -gt 0 ]]
do
key="$1"

case $key in
    -E|--Extract)
    EXTRACT=true
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

if [[ ${EXTRACT} ]]
then
    echo ""
    echo "***************************************************************************"
    echo "We are going to download and extract the ${IMAGE}'s secret"
    echo "***************************************************************************"
    echo ""
    echo " --------- QUIC_PROTOCOL PART (Get and download) ---------"
    echo ""
    python3 examples/http3_client.py --ca-certs tests/pycacert.pem https://localhost:4433/secret  --output-dir=result_resources/
    echo ""
    echo " --------- STEGO_LSB PART (Extract) ---------"
    echo ""
    python3 src/stego_lsb/stego.py -E -i result_resources/icon.png
else
    echo ""
    echo "***************************************************************************"
    echo "We are going to hide the ${SECRET} in ${IMAGE} and send it by quic protocol"
    echo "***************************************************************************"
    echo ""
    echo " --------- STEGO_LSB PART (Hide) ---------"
    echo ""
    python3 src/stego_lsb/stego.py -i "${IMAGE}" -s "${SECRET}"
    echo ""
    echo " --------- QUIC_PROTOCOL PART (Send) ---------"
    echo ""
    python3 examples/http3_server.py --certificate tests/ssl_cert.pem --private-key tests/ssl_key.pem -v
fi


