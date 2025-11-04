# gRPC HelloWorld (Java server + Python client)

A minimal gRPC project showcasing:
- A Java gRPC server (Maven, Java 11), exposing unary and server-streaming RPCs
- A Python interactive client (menus in French) calling the same service
- Shared protobuf (`proto/helloworld.proto`) and a helper script to regenerate stubs

## Project layout

```
.
├── generate_stubs.sh             # regenerate Java & Python stubs from proto
├── proto/
│   └── helloworld.proto          # service & messages
├── java-server/
│   ├── pom.xml                   # Maven config (grpc-java, protobuf)
│   └── src/main/java/com/example/grpc/
│       ├── HelloWorldServer.java # gRPC server (port 50051)
│       └── ...                   # generated Java stubs
└── python-client/
    ├── client.py                 # interactive console client
    ├── helloworld_pb2.py         # generated (message classes)
    └── helloworld_pb2_grpc.py    # generated (client stub)
```

## Prerequisites

- Java 11+ and Maven 3.x
- Python 3.8+ and pip
- Protocol Buffers compiler (`protoc`) in PATH
- Python packages (client and stub generation):
  - grpcio
  - grpcio-tools

Optional but recommended:
- A virtual environment for Python (`python3 -m venv .venv`)

## Install Python dependencies

```bash
# From repo root
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install grpcio grpcio-tools
```

## Regenerate stubs (Java + Python)

The script installs Python deps if missing and regenerates both languages. Ensure `protoc` is installed.

```bash
# From repo root
chmod +x generate_stubs.sh
./generate_stubs.sh
```

Generated files:
- Java: `java-server/src/main/java/com/example/grpc/*` (service stubs)
- Python: `python-client/helloworld_pb2*.py`

## Run the Java server

The server listens on port 50051.

Option A — run from your IDE:
- Open `java-server` as a Maven project
- Run the `main` method in `com.example.grpc.HelloWorldServer`

Option B — via Maven Exec plugin (recommended):
- Add the following plugin to `java-server/pom.xml` (inside `<build><plugins>`):

```xml
<plugin>
  <groupId>org.codehaus.mojo</groupId>
  <artifactId>exec-maven-plugin</artifactId>
  <version>3.1.0</version>
  <configuration>
    <mainClass>com.example.grpc.HelloWorldServer</mainClass>
  </configuration>
</plugin>
```

Then run:

```bash
cd java-server
mvn -q clean package
mvn -q exec:java
```

> Note: Without the exec plugin, running via plain `java -cp` requires adding gRPC runtime jars to the classpath.

## Run the Python client

Keep the Java server running on `localhost:50051`, then in a new terminal:

```bash
# From repo root
source .venv/bin/activate  # if you created one
python3 python-client/client.py
```

You’ll get an interactive menu to:
- Send a single greeting (unary RPC)
- Receive a stream of greetings (server-streaming RPC)
- Switch languages (fr, en, ar) or change server host/port

## Troubleshooting

- protoc not found: Install Protocol Buffers compiler (`protoc`) and ensure it’s in PATH.
- ImportError grpcio/grpcio-tools: Run `pip install grpcio grpcio-tools` in your active environment.
- Port in use: The server uses port 50051. Stop any process using it or change the port in `HelloWorldServer.main`.
- Python client cannot connect: Verify server is running, reachability of `host:port`, and that versions of `grpcio` are compatible.

ly (e.g., MIT, Apache-2.0). You can add a `LICENSE` file later.
