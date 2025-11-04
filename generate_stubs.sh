#!/bin/bash

echo "=== Installation des dépendances ==="
pip install grpcio grpcio-tools

echo "=== Génération des stubs Java ==="
protoc --java_out=java-server/src/main/java --proto_path=proto proto/helloworld.proto

echo "=== Génération des stubs Python ==="
python3 -m grpc_tools.protoc \
    --proto_path=proto \
    --python_out=python-client \
    --grpc_python_out=python-client \
    proto/helloworld.proto

echo "=== Vérification ==="
echo "Fichiers générés dans python-client/:"
ls -la python-client/
