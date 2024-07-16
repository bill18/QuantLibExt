
Implementing an adapter using gRPC to handle asynchronous requests from various languages involves a few key steps:

1. **Define Your gRPC Service**:

   - Create a `.proto` file to define the gRPC service, messages, and RPC methods.
2. **Generate gRPC Code**:

   - Use the `protoc` compiler to generate gRPC code for your target languages.
3. **Implement the Server**:

   - Implement the server in a language that can handle your proprietary messages and manage the producer-consumer framework.
4. **Handle Asynchronous Requests**:

   - Use asynchronous programming techniques in your server implementation to handle requests concurrently.
5. **Implement Clients**:

   - Implement gRPC clients in the various languages you need to support.

Here’s a step-by-step example:

### 1. Define Your gRPC Service

Create a file called `adapter.proto`:

```proto
syntax = "proto3";

service AdapterService {
  rpc SendMessage (MessageRequest) returns (MessageResponse);
}

message MessageRequest {
  string message_id = 1;
  bytes payload = 2;
}

message MessageResponse {
  bool success = 1;
  string error_message = 2;
}
```

### 2. Generate gRPC Code

Use the `protoc` compiler to generate the code for your server and clients:

```bash
# Generate server code for C++ (or your chosen server language)
protoc --cpp_out=. --grpc_out=. --plugin=protoc-gen-grpc=/path/to/grpc_cpp_plugin adapter.proto

# Generate client code for other languages, e.g., Python
protoc --python_out=. --grpc_out=. --plugin=protoc-gen-grpc=/path/to/grpc_python_plugin adapter.proto
```

### 3. Implement the Server

Implement the server in a language that supports your proprietary messages (e.g., C++):

```cpp
#include <grpcpp/grpcpp.h>
#include "adapter.grpc.pb.h"

class AdapterServiceImpl final : public AdapterService::Service {
  grpc::Status SendMessage(grpc::ServerContext* context, const MessageRequest* request, MessageResponse* response) override {
    // Handle the proprietary message processing
    bool success = ProcessMessage(request->message_id(), request->payload());
    response->set_success(success);
    if (!success) {
      response->set_error_message("Processing failed");
    }
    return grpc::Status::OK;
  }

  bool ProcessMessage(const std::string& message_id, const std::string& payload) {
    // Implement your proprietary message processing logic here
    return true;
  }
};

void RunServer() {
  std::string server_address("0.0.0.0:50051");
  AdapterServiceImpl service;

  grpc::ServerBuilder builder;
  builder.AddListeningPort(server_address, grpc::InsecureServerCredentials());
  builder.RegisterService(&service);
  std::unique_ptr<grpc::Server> server(builder.BuildAndStart());
  std::cout << "Server listening on " << server_address << std::endl;
  server->Wait();
}

int main(int argc, char** argv) {
  RunServer();
  return 0;
}
```

### 4. Handle Asynchronous Requests

Use asynchronous programming models provided by gRPC in your chosen language:

- For C++, you can use gRPC's asynchronous API.

### 5. Implement Clients

Implement clients in different languages. Here’s a Python example:

```python
import grpc
import adapter_pb2
import adapter_pb2_grpc

def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = adapter_pb2_grpc.AdapterServiceStub(channel)
    response = stub.SendMessage(adapter_pb2.MessageRequest(message_id='1', payload=b'example_payload'))
    print(f"Response: {response.success}, {response.error_message}")

if __name__ == '__main__':
    run()
```

By following these steps, you can create a gRPC adapter that handles requests asynchronously from various languages, interfacing with your proprietary producer-consumer framework. For asynchronous handling, ensure to leverage the specific async features available in the gRPC library for your server's language.


gRPC supports both synchronous and asynchronous APIs. The example I provided uses the synchronous API for simplicity. To handle requests asynchronously, you need to specifically use the asynchronous API provided by gRPC. Here's an overview of how you can implement an asynchronous gRPC server in C++.

### Asynchronous gRPC Server in C++

1. **Define the Service**:
   Your `.proto` file remains the same.
2. **Generate gRPC Code**:
   This step remains the same as well.
3. **Implement the Asynchronous Server**:

```cpp
#include <grpcpp/grpcpp.h>
#include <grpcpp/server_builder.h>
#include <grpcpp/server_context.h>
#include <grpcpp/alarm.h>
#include "adapter.grpc.pb.h"
#include <iostream>
#include <memory>
#include <thread>
#include <chrono>

class AdapterServiceImpl final {
public:
    AdapterServiceImpl() : service_(), cq_() {}

    void RunServer() {
        std::string server_address("0.0.0.0:50051");

        grpc::ServerBuilder builder;
        builder.AddListeningPort(server_address, grpc::InsecureServerCredentials());
        builder.RegisterService(&service_);
        cq_ = builder.AddCompletionQueue();

        server_ = builder.BuildAndStart();
        std::cout << "Server listening on " << server_address << std::endl;

        HandleRpcs();
    }

private:
    class CallData {
    public:
        CallData(AdapterService::AsyncService* service, grpc::ServerCompletionQueue* cq)
            : service_(service), cq_(cq), responder_(&ctx_), status_(CREATE) {
            Proceed();
        }

        void Proceed() {
            if (status_ == CREATE) {
                status_ = PROCESS;
                service_->RequestSendMessage(&ctx_, &request_, &responder_, cq_, cq_, this);
            } else if (status_ == PROCESS) {
                new CallData(service_, cq_);

                // Implement your proprietary message processing logic here
                bool success = true;  // Replace this with actual processing logic
                response_.set_success(success);
                if (!success) {
                    response_.set_error_message("Processing failed");
                }

                status_ = FINISH;
                responder_.Finish(response_, grpc::Status::OK, this);
            } else {
                GPR_ASSERT(status_ == FINISH);
                delete this;
            }
        }

    private:
        AdapterService::AsyncService* service_;
        grpc::ServerCompletionQueue* cq_;
        grpc::ServerContext ctx_;

        MessageRequest request_;
        MessageResponse response_;

        grpc::ServerAsyncResponseWriter<MessageResponse> responder_;

        enum CallStatus { CREATE, PROCESS, FINISH };
        CallStatus status_;
    };

    void HandleRpcs() {
        new CallData(&service_, cq_.get());
        void* tag;
        bool ok;
        while (true) {
            GPR_ASSERT(cq_->Next(&tag, &ok));
            static_cast<CallData*>(tag)->Proceed();
        }
    }

    std::unique_ptr<grpc::Server> server_;
    AdapterService::AsyncService service_;
    std::unique_ptr<grpc::ServerCompletionQueue> cq_;
};

int main(int argc, char** argv) {
    AdapterServiceImpl server;
    server.RunServer();

    return 0;
}
```

### Explanation

- **CallData Class**: This class manages the lifecycle of an RPC. It handles the creation, processing, and completion of an RPC call.
- **Proceed Method**: This method progresses the state of the RPC from creation to processing to finish.
- **HandleRpcs Method**: This method starts the handling of RPCs by creating a new `CallData` instance and continuously polling for new events.

### Summary

In the asynchronous server implementation:

- The server uses a `CompletionQueue` to handle RPCs asynchronously.
- The `CallData` class manages individual RPC calls and progresses them through their lifecycle.
- The `Proceed` method is called to transition the RPC through different states (CREATE, PROCESS, FINISH).

Using this setup, your gRPC server can handle requests asynchronously, allowing for better scalability and performance.


With the asynchronous gRPC server setup described, the 100 concurrent requests will not be handled sequentially. Instead, they will be handled concurrently, which allows the server to process multiple requests simultaneously, leading to better performance and scalability.

Here’s a more detailed explanation of what happens when 100 concurrent users send requests to the asynchronous gRPC server:

### Handling Concurrent Requests

1. **Server Initialization**:

   - The server starts and listens on the specified address.
   - A `CompletionQueue` is created to manage asynchronous events.
2. **CallData Instances**:

   - When a new request arrives, a `CallData` instance is created to handle it.
   - The `CallData` class manages the lifecycle of an RPC call, transitioning through various states (CREATE, PROCESS, FINISH).
3. **Asynchronous Processing**:

   - Each `CallData` instance uses the `CompletionQueue` to wait for and respond to events.
   - The `CompletionQueue` allows multiple `CallData` instances to be active and processing concurrently.

### Concurrent Execution

- **Multiple CallData Instances**: Each incoming request is handled by a separate `CallData` instance. Since these instances operate independently and use the `CompletionQueue` for coordination, multiple requests can be processed in parallel.
- **Non-Blocking Operations**: The asynchronous nature of the `CompletionQueue` means that the server is not blocked while waiting for any single request to complete. Instead, it can continue to accept and process new requests.

### Practical Considerations

- **Concurrency**: The actual level of concurrency will depend on the number of threads handling the events from the `CompletionQueue`. By default, the `HandleRpcs` method runs in the main thread, but you can spawn multiple threads to handle events concurrently.
- **Thread Pool**: To handle high concurrency effectively, you can use a thread pool. Each thread can poll the `CompletionQueue` and process events, allowing the server to scale with the number of available threads.

### Example with Thread Pool

Here’s an updated example that uses a thread pool to handle concurrent requests more effectively:

```cpp
#include <grpcpp/grpcpp.h>
#include <grpcpp/server_builder.h>
#include <grpcpp/server_context.h>
#include <grpcpp/alarm.h>
#include "adapter.grpc.pb.h"
#include <iostream>
#include <memory>
#include <thread>
#include <vector>

class AdapterServiceImpl final {
public:
    AdapterServiceImpl() : service_(), cq_() {}

    void RunServer() {
        std::string server_address("0.0.0.0:50051");

        grpc::ServerBuilder builder;
        builder.AddListeningPort(server_address, grpc::InsecureServerCredentials());
        builder.RegisterService(&service_);
        cq_ = builder.AddCompletionQueue();

        server_ = builder.BuildAndStart();
        std::cout << "Server listening on " << server_address << std::endl;

        // Create a thread pool to handle events
        int num_threads = std::thread::hardware_concurrency(); // Or any number you see fit
        std::vector<std::thread> thread_pool;
        for (int i = 0; i < num_threads; ++i) {
            thread_pool.emplace_back(&AdapterServiceImpl::HandleRpcs, this);
        }

        for (auto& thread : thread_pool) {
            thread.join();
        }
    }

private:
    class CallData {
    public:
        CallData(AdapterService::AsyncService* service, grpc::ServerCompletionQueue* cq)
            : service_(service), cq_(cq), responder_(&ctx_), status_(CREATE) {
            Proceed();
        }

        void Proceed() {
            if (status_ == CREATE) {
                status_ = PROCESS;
                service_->RequestSendMessage(&ctx_, &request_, &responder_, cq_, cq_, this);
            } else if (status_ == PROCESS) {
                new CallData(service_, cq_);

                // Implement your proprietary message processing logic here
                bool success = true;  // Replace this with actual processing logic
                response_.set_success(success);
                if (!success) {
                    response_.set_error_message("Processing failed");
                }

                status_ = FINISH;
                responder_.Finish(response_, grpc::Status::OK, this);
            } else {
                GPR_ASSERT(status_ == FINISH);
                delete this;
            }
        }

    private:
        AdapterService::AsyncService* service_;
        grpc::ServerCompletionQueue* cq_;
        grpc::ServerContext ctx_;

        MessageRequest request_;
        MessageResponse response_;

        grpc::ServerAsyncResponseWriter<MessageResponse> responder_;

        enum CallStatus { CREATE, PROCESS, FINISH };
        CallStatus status_;
    };

    void HandleRpcs() {
        new CallData(&service_, cq_.get());
        void* tag;
        bool ok;
        while (true) {
            GPR_ASSERT(cq_->Next(&tag, &ok));
            static_cast<CallData*>(tag)->Proceed();
        }
    }

    std::unique_ptr<grpc::Server> server_;
    AdapterService::AsyncService service_;
    std::unique_ptr<grpc::ServerCompletionQueue> cq_;
};

int main(int argc, char** argv) {
    AdapterServiceImpl server;
    server.RunServer();

    return 0;
}
```

### Summary

With this setup, the server can handle 100 concurrent requests efficiently:

- **Thread Pool**: The thread pool allows multiple threads to process events from the `CompletionQueue`, enabling concurrent handling of requests.
- **Scalability**: By adjusting the number of threads, you can scale the server to handle more concurrent requests based on the available hardware resources.


Certainly! Here’s a `CMakeLists.txt` file that assumes you have gRPC installed in `~/.local`. This file configures a C++ project to use gRPC and includes the necessary settings to find and link the gRPC and protobuf libraries.

```cmake
cmake_minimum_required(VERSION 3.15)

project(AdapterService)

# Set the C++ standard
set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# Set the path to your local gRPC installation
set(GRPC_INSTALL_PATH "$ENV{HOME}/.local")

# Add gRPC and protobuf cmake modules
list(APPEND CMAKE_PREFIX_PATH "${GRPC_INSTALL_PATH}")

find_package(Protobuf REQUIRED)
find_package(gRPC REQUIRED)

# Include directories
include_directories(${PROTOBUF_INCLUDE_DIRS})
include_directories(${GRPC_INCLUDE_DIRS})
include_directories(${CMAKE_CURRENT_BINARY_DIR})

# Proto files
set(PROTO_FILES adapter.proto)

# Generate C++ source files from proto files
PROTOBUF_GENERATE_CPP(PROTO_SRCS PROTO_HDRS ${PROTO_FILES})
GRPC_GENERATE_CPP(GRPC_SRCS GRPC_HDRS ${PROTO_FILES})

# Executable
add_executable(AdapterServer server.cpp ${PROTO_SRCS} ${GRPC_SRCS})

# Link libraries
target_link_libraries(AdapterServer ${PROTOBUF_LIBRARIES} ${GRPC_LIBRARIES} ${GRPC++_LIBRARIES})

# Ensure gRPC and protobuf libraries are found
find_library(PROTOBUF_LIBRARIES protobuf HINTS "${GRPC_INSTALL_PATH}/lib")
find_library(GRPC_LIBRARIES grpc HINTS "${GRPC_INSTALL_PATH}/lib")
find_library(GRPC++_LIBRARIES grpc++ HINTS "${GRPC_INSTALL_PATH}/lib")
```

### Explanation

- **C++ Standard**: Sets the C++ standard to C++14.
- **GRPC_INSTALL_PATH**: Sets the path to your local gRPC installation (`~/.local`).
- **CMake Prefix Path**: Adds the gRPC install path to the CMake prefix path so that `find_package` can locate gRPC and protobuf.
- **Proto Files**: Specifies the proto files to be processed.
- **Protobuf and gRPC Code Generation**: Uses `PROTOBUF_GENERATE_CPP` and `GRPC_GENERATE_CPP` to generate C++ source files from the proto files.
- **Executable**: Adds an executable target for the server (`AdapterServer`).
- **Link Libraries**: Links the executable with the necessary protobuf and gRPC libraries.
- **Find Libraries**: Ensures that the protobuf and gRPC libraries are found correctly.

### Usage

1. **Create Project Structure**:

   ```sh
   mkdir -p AdapterService/build
   cd AdapterService
   # Place CMakeLists.txt in the AdapterService directory
   # Place adapter.proto and server.cpp in the AdapterService directory
   ```
2. **Build the Project**:

   ```sh
   cd build
   cmake ..
   make
   ```
3. **Run the Server**:

   ```sh
   ./AdapterServer
   ```

Make sure you have your `server.cpp` and `adapter.proto` files in the `AdapterService` directory. This setup should allow you to build and run your gRPC server using your locally installed gRPC and protobuf libraries.



Certainly! You can integrate the `protoc` command directly into the `CMakeLists.txt` file to handle the generation of C++ source files from the `.proto` files. Here’s an updated version of the `CMakeLists.txt` file that includes these commands:

```cmake
cmake_minimum_required(VERSION 3.15)

project(AdapterService)

# Set the C++ standard
set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# Set the path to your local gRPC installation
set(GRPC_INSTALL_PATH "$ENV{HOME}/.local")

# Add gRPC and protobuf cmake modules
list(APPEND CMAKE_PREFIX_PATH "${GRPC_INSTALL_PATH}")

# Find protobuf and gRPC packages
find_package(Protobuf REQUIRED)
find_package(gRPC REQUIRED)

# Include directories
include_directories(${PROTOBUF_INCLUDE_DIRS})
include_directories(${GRPC_INCLUDE_DIRS})
include_directories(${CMAKE_CURRENT_BINARY_DIR})

# Proto files
set(PROTO_FILES adapter.proto)

# Generate C++ source files from proto files using protoc
foreach(PROTO_FILE ${PROTO_FILES})
    get_filename_component(PROTO_FILENAME ${PROTO_FILE} NAME_WE)
    set(GENERATED_PROTO_SRC "${CMAKE_CURRENT_BINARY_DIR}/${PROTO_FILENAME}.pb.cc")
    set(GENERATED_PROTO_HDR "${CMAKE_CURRENT_BINARY_DIR}/${PROTO_FILENAME}.pb.h")
    set(GENERATED_GRPC_SRC "${CMAKE_CURRENT_BINARY_DIR}/${PROTO_FILENAME}.grpc.pb.cc")
    set(GENERATED_GRPC_HDR "${CMAKE_CURRENT_BINARY_DIR}/${PROTO_FILENAME}.grpc.pb.h")

    add_custom_command(
        OUTPUT ${GENERATED_PROTO_SRC} ${GENERATED_PROTO_HDR} ${GENERATED_GRPC_SRC} ${GENERATED_GRPC_HDR}
        COMMAND ${Protobuf_PROTOC_EXECUTABLE}
        ARGS --proto_path=${CMAKE_CURRENT_SOURCE_DIR} --cpp_out=${CMAKE_CURRENT_BINARY_DIR} ${PROTO_FILE}
        COMMAND ${Protobuf_PROTOC_EXECUTABLE}
        ARGS --proto_path=${CMAKE_CURRENT_SOURCE_DIR} --grpc_out=${CMAKE_CURRENT_BINARY_DIR} --plugin=protoc-gen-grpc=${GRPC_INSTALL_PATH}/bin/grpc_cpp_plugin ${PROTO_FILE}
        DEPENDS ${PROTO_FILE}
        COMMENT "Running protoc on ${PROTO_FILE}"
        VERBATIM
    )

    list(APPEND PROTO_SRCS ${GENERATED_PROTO_SRC})
    list(APPEND PROTO_HDRS ${GENERATED_PROTO_HDR})
    list(APPEND GRPC_SRCS ${GENERATED_GRPC_SRC})
    list(APPEND GRPC_HDRS ${GENERATED_GRPC_HDR})
endforeach()

# Executable
add_executable(AdapterServer server.cpp ${PROTO_SRCS} ${GRPC_SRCS})

# Link libraries
target_link_libraries(AdapterServer ${PROTOBUF_LIBRARIES} ${GRPC_LIBRARIES} ${GRPC++_LIBRARIES})

# Ensure gRPC and protobuf libraries are found
find_library(PROTOBUF_LIBRARIES protobuf HINTS "${GRPC_INSTALL_PATH}/lib")
find_library(GRPC_LIBRARIES grpc HINTS "${GRPC_INSTALL_PATH}/lib")
find_library(GRPC++_LIBRARIES grpc++ HINTS "${GRPC_INSTALL_PATH}/lib")
```

### Explanation

- **add_custom_command**: This command invokes `protoc` to generate the C++ source and header files for both protobuf messages and gRPC services from the `.proto` files.
  - The `--proto_path` argument specifies the directory containing the `.proto` files.
  - The `--cpp_out` argument specifies the output directory for the generated protobuf C++ files.
  - The `--grpc_out` argument specifies the output directory for the generated gRPC C++ files and uses the `grpc_cpp_plugin` to generate the necessary code.
- **add_executable**: This command creates an executable target named `AdapterServer` and includes the generated source files in the build.
- **target_link_libraries**: This command links the necessary protobuf and gRPC libraries to the executable.

### Usage

1. **Create Project Structure**:

   ```sh
   mkdir -p AdapterService/build
   cd AdapterService
   # Place CMakeLists.txt in the AdapterService directory
   # Place adapter.proto and server.cpp in the AdapterService directory
   ```
2. **Build the Project**:

   ```sh
   cd build
   cmake ..
   make
   ```
3. **Run the Server**:

   ```sh
   ./AdapterServer
   ```

Make sure your `server.cpp` and `adapter.proto` files are in the `AdapterService` directory. This setup should allow you to build and run your gRPC server using your locally installed gRPC and protobuf libraries, with `protoc` being invoked as part of the build process.


The error you're encountering indicates a version mismatch between the `protoc` compiler and the Protobuf library. Specifically, `protoc` is at version `25.1`, while the Protobuf library is at version `4.25.1`.

This mismatch can happen if you have multiple versions of Protobuf installed on your system or if the `protoc` binary is not correctly aligned with the Protobuf library version used by gRPC.

### Steps to Resolve

1. **Ensure Consistent Installation**: Make sure that both the Protobuf compiler and library are installed from the same source and version.
2. **Update Environment Variables**: Make sure that your environment variables (`PATH` and `LD_LIBRARY_PATH`) are correctly set to point to the versions you intend to use.
3. **Check Versions**: Verify the versions of `protoc` and the Protobuf library you have installed.
4. **Rebuild gRPC and Protobuf**: Ensure you build and install gRPC and Protobuf from the same source to maintain version consistency.

### Detailed Steps

#### 1. Ensure Consistent Installation

Make sure you are using the Protobuf library and `protoc` binary from the same installation source.

```sh
# Remove any existing protobuf installations
sudo apt-get remove -y libprotobuf-dev protobuf-compiler

# Install Protobuf from source (example)
git clone https://github.com/protocolbuffers/protobuf.git
cd protobuf
git checkout v4.25.1  # Use the same version for both library and compiler
mkdir build && cd build
cmake ..
make -j$(nproc)
sudo make install
sudo ldconfig
```

#### 2. Update Environment Variables

Add the installed paths to your `~/.bashrc` or `~/.zshrc`:

```sh
export PATH=$HOME/.local/bin:$PATH
export LD_LIBRARY_PATH=$HOME/.local/lib:$LD_LIBRARY_PATH
```

Reload your shell:

```sh
source ~/.bashrc
# or
source ~/.zshrc
```

#### 3. Check Versions

Verify the versions to ensure they match:

```sh
protoc --version
# Should print: libprotoc 4.25.1
```

#### 4. Rebuild gRPC and Protobuf

If you built gRPC and Protobuf from source, ensure they are aligned:

```sh
# Remove any existing gRPC installation
sudo rm -rf /usr/local/include/grpc /usr/local/lib/libgrpc*

# Clone and build gRPC from source
git clone --recurse-submodules -b v1.56.0 https://github.com/grpc/grpc
cd grpc
mkdir -p cmake/build
cd cmake/build
cmake -DgRPC_INSTALL=ON \
      -DgRPC_BUILD_TESTS=OFF \
      -DCMAKE_INSTALL_PREFIX=$HOME/.local \
      -Dprotobuf_DIR=$HOME/.local/lib/cmake/protobuf ../..
make -j$(nproc)
make install
```

### Updated `CMakeLists.txt`

Here’s an updated `CMakeLists.txt` to ensure it uses the correct paths:

```cmake
cmake_minimum_required(VERSION 3.15)

project(AdapterService)

# Set the C++ standard
set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# Set the path to your local gRPC installation
set(GRPC_INSTALL_PATH "$ENV{HOME}/.local")

# Add gRPC and protobuf cmake modules
list(APPEND CMAKE_PREFIX_PATH "${GRPC_INSTALL_PATH}")

# Find protobuf and gRPC packages
find_package(Protobuf REQUIRED)
find_package(gRPC REQUIRED)

# Include directories
include_directories(${PROTOBUF_INCLUDE_DIRS})
include_directories(${GRPC_INCLUDE_DIRS})
include_directories(${CMAKE_CURRENT_BINARY_DIR})

# Proto files
set(PROTO_FILES adapter.proto)

# Generate C++ source files from proto files using protoc
foreach(PROTO_FILE ${PROTO_FILES})
    get_filename_component(PROTO_FILENAME ${PROTO_FILE} NAME_WE)
    set(GENERATED_PROTO_SRC "${CMAKE_CURRENT_BINARY_DIR}/${PROTO_FILENAME}.pb.cc")
    set(GENERATED_PROTO_HDR "${CMAKE_CURRENT_BINARY_DIR}/${PROTO_FILENAME}.pb.h")
    set(GENERATED_GRPC_SRC "${CMAKE_CURRENT_BINARY_DIR}/${PROTO_FILENAME}.grpc.pb.cc")
    set(GENERATED_GRPC_HDR "${CMAKE_CURRENT_BINARY_DIR}/${PROTO_FILENAME}.grpc.pb.h")

    add_custom_command(
        OUTPUT ${GENERATED_PROTO_SRC} ${GENERATED_PROTO_HDR} ${GENERATED_GRPC_SRC} ${GENERATED_GRPC_HDR}
        COMMAND ${Protobuf_PROTOC_EXECUTABLE}
        ARGS --proto_path=${CMAKE_CURRENT_SOURCE_DIR} --cpp_out=${CMAKE_CURRENT_BINARY_DIR} ${PROTO_FILE}
        COMMAND ${Protobuf_PROTOC_EXECUTABLE}
        ARGS --proto_path=${CMAKE_CURRENT_SOURCE_DIR} --grpc_out=${CMAKE_CURRENT_BINARY_DIR} --plugin=protoc-gen-grpc=${GRPC_INSTALL_PATH}/bin/grpc_cpp_plugin ${PROTO_FILE}
        DEPENDS ${PROTO_FILE}
        COMMENT "Running protoc on ${PROTO_FILE}"
        VERBATIM
    )

    list(APPEND PROTO_SRCS ${GENERATED_PROTO_SRC})
    list(APPEND PROTO_HDRS ${GENERATED_PROTO_HDR})
    list(APPEND GRPC_SRCS ${GENERATED_GRPC_SRC})
    list(APPEND GRPC_HDRS ${GENERATED_GRPC_HDR})
endforeach()

# Executable
add_executable(AdapterServer server.cpp ${PROTO_SRCS} ${GRPC_SRCS})

# Link libraries
target_link_libraries(AdapterServer ${PROTOBUF_LIBRARIES} ${GRPC_LIBRARIES} ${GRPC++_LIBRARIES})

# Ensure gRPC and protobuf libraries are found
find_library(PROTOBUF_LIBRARIES protobuf HINTS "${GRPC_INSTALL_PATH}/lib")
find_library(GRPC_LIBRARIES grpc HINTS "${GRPC_INSTALL_PATH}/lib")
find_library(GRPC++_LIBRARIES grpc++ HINTS "${GRPC_INSTALL_PATH}/lib")
```

This approach ensures that `protoc` and the Protobuf library are from the same version, preventing version mismatch errors.


It looks like you are on the right track to install Protobuf from source. Here are the detailed steps to ensure everything is installed correctly and to verify the versions:

### Step-by-Step Instructions to Install Protobuf from Source

1. **Remove any existing protobuf installations**:

   ```sh
   sudo apt-get remove -y libprotobuf-dev protobuf-compiler
   ```
2. **Clone the Protobuf repository and check out the specific version**:

   ```sh
   git clone https://github.com/protocolbuffers/protobuf.git
   cd protobuf
   git checkout v4.25.1  # Ensure this matches the version you need
   ```
3. **Build and install Protobuf**:

   ```sh
   mkdir build && cd build
   cmake ..
   make -j$(nproc)
   sudo make install
   sudo ldconfig
   ```
4. **Verify the installation**:

   Ensure that the installed `protoc` version matches the Protobuf library version:

   ```sh
   protoc --version  # Should output: libprotoc 4.25.1
   ```

### Step-by-Step Instructions to Install gRPC from Source

1. **Clone the gRPC repository**:

   ```sh
   git clone --recurse-submodules -b v1.56.0 https://github.com/grpc/grpc
   cd grpc
   ```
2. **Build and install gRPC**:

   ```sh
   mkdir -p cmake/build
   cd cmake/build
   cmake -DgRPC_INSTALL=ON \
         -DgRPC_BUILD_TESTS=OFF \
         -DCMAKE_INSTALL_PREFIX=$HOME/.local \
         -Dprotobuf_DIR=$HOME/.local/lib/cmake/protobuf ../..
   make -j$(nproc)
   sudo make install
   sudo ldconfig
   ```

### Updated `CMakeLists.txt`

Here's the updated `CMakeLists.txt` file with the correct paths and `protoc` commands:

```cmake
cmake_minimum_required(VERSION 3.15)

project(AdapterService)

# Set the C++ standard
set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# Set the path to your local gRPC installation
set(GRPC_INSTALL_PATH "$ENV{HOME}/.local")

# Add gRPC and protobuf cmake modules
list(APPEND CMAKE_PREFIX_PATH "${GRPC_INSTALL_PATH}")

# Find protobuf and gRPC packages
find_package(Protobuf REQUIRED)
find_package(gRPC REQUIRED)

# Include directories
include_directories(${PROTOBUF_INCLUDE_DIRS})
include_directories(${GRPC_INCLUDE_DIRS})
include_directories(${CMAKE_CURRENT_BINARY_DIR})

# Proto files
set(PROTO_FILES adapter.proto)

# Generate C++ source files from proto files using protoc
foreach(PROTO_FILE ${PROTO_FILES})
    get_filename_component(PROTO_FILENAME ${PROTO_FILE} NAME_WE)
    set(GENERATED_PROTO_SRC "${CMAKE_CURRENT_BINARY_DIR}/${PROTO_FILENAME}.pb.cc")
    set(GENERATED_PROTO_HDR "${CMAKE_CURRENT_BINARY_DIR}/${PROTO_FILENAME}.pb.h")
    set(GENERATED_GRPC_SRC "${CMAKE_CURRENT_BINARY_DIR}/${PROTO_FILENAME}.grpc.pb.cc")
    set(GENERATED_GRPC_HDR "${CMAKE_CURRENT_BINARY_DIR}/${PROTO_FILENAME}.grpc.pb.h")

    add_custom_command(
        OUTPUT ${GENERATED_PROTO_SRC} ${GENERATED_PROTO_HDR} ${GENERATED_GRPC_SRC} ${GENERATED_GRPC_HDR}
        COMMAND ${Protobuf_PROTOC_EXECUTABLE}
        ARGS --proto_path=${CMAKE_CURRENT_SOURCE_DIR} --cpp_out=${CMAKE_CURRENT_BINARY_DIR} ${PROTO_FILE}
        COMMAND ${Protobuf_PROTOC_EXECUTABLE}
        ARGS --proto_path=${CMAKE_CURRENT_SOURCE_DIR} --grpc_out=${CMAKE_CURRENT_BINARY_DIR} --plugin=protoc-gen-grpc=${GRPC_INSTALL_PATH}/bin/grpc_cpp_plugin ${PROTO_FILE}
        DEPENDS ${PROTO_FILE}
        COMMENT "Running protoc on ${PROTO_FILE}"
        VERBATIM
    )

    list(APPEND PROTO_SRCS ${GENERATED_PROTO_SRC})
    list(APPEND PROTO_HDRS ${GENERATED_PROTO_HDR})
    list(APPEND GRPC_SRCS ${GENERATED_GRPC_SRC})
    list(APPEND GRPC_HDRS ${GENERATED_GRPC_HDR})
endforeach()

# Executable
add_executable(AdapterServer server.cpp ${PROTO_SRCS} ${GRPC_SRCS})

# Link libraries
target_link_libraries(AdapterServer ${PROTOBUF_LIBRARIES} ${GRPC_LIBRARIES} ${GRPC++_LIBRARIES})

# Ensure gRPC and protobuf libraries are found
find_library(PROTOBUF_LIBRARIES protobuf HINTS "${GRPC_INSTALL_PATH}/lib")
find_library(GRPC_LIBRARIES grpc HINTS "${GRPC_INSTALL_PATH}/lib")
find_library(GRPC++_LIBRARIES grpc++ HINTS "${GRPC_INSTALL_PATH}/lib")
```

### Build and Run the Project

1. **Create Project Structure**:

   ```sh
   mkdir -p AdapterService/build
   cd AdapterService
   # Place CMakeLists.txt in the AdapterService directory
   # Place adapter.proto and server.cpp in the AdapterService directory
   ```
2. **Build the Project**:

   ```sh
   cd build
   cmake ..
   make
   ```
3. **Run the Server**:

   ```sh
   ./AdapterServer
   ```

This setup ensures that `protoc` and the Protobuf library are from the same version, preventing version mismatch errors.


It looks like you're trying to build gRPC and it's complaining about the missing `third_party/googletest` directory. This can happen if the submodules were not properly initialized when you cloned the repository.

### Ensure Submodules are Properly Initialized

When cloning the gRPC repository, you need to ensure that all submodules are also cloned. Here are the steps to do this:

1. **Clone the gRPC repository with submodules**:

   ```sh
   git clone --recurse-submodules -b v1.56.0 https://github.com/grpc/grpc
   cd grpc
   ```

   If you've already cloned the repository without submodules, you can initialize and update them with the following commands:

   ```sh
   git submodule update --init --recursive
   ```
2. **Build and install gRPC**:

   ```sh
   mkdir -p cmake/build
   cd cmake/build
   cmake -DgRPC_INSTALL=ON \
         -DgRPC_BUILD_TESTS=OFF \
         -DCMAKE_INSTALL_PREFIX=$HOME/.local \
         -Dprotobuf_DIR=$HOME/.local/lib/cmake/protobuf ../..
   make -j$(nproc)
   sudo make install
   sudo ldconfig
   ```

### Verify Submodule Initialization

Ensure that the `third_party/googletest` directory exists and is populated:

```sh
ls third_party/googletest
```

If it doesn't exist or is empty, the submodules were not properly initialized.

### Correct `CMakeLists.txt`

Here's the `CMakeLists.txt` file again to ensure all settings are correct:

```cmake
cmake_minimum_required(VERSION 3.15)

project(AdapterService)

# Set the C++ standard
set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# Set the path to your local gRPC installation
set(GRPC_INSTALL_PATH "$ENV{HOME}/.local")

# Add gRPC and protobuf cmake modules
list(APPEND CMAKE_PREFIX_PATH "${GRPC_INSTALL_PATH}")

# Find protobuf and gRPC packages
find_package(Protobuf REQUIRED)
find_package(gRPC REQUIRED)

# Include directories
include_directories(${PROTOBUF_INCLUDE_DIRS})
include_directories(${GRPC_INCLUDE_DIRS})
include_directories(${CMAKE_CURRENT_BINARY_DIR})

# Proto files
set(PROTO_FILES adapter.proto)

# Generate C++ source files from proto files using protoc
foreach(PROTO_FILE ${PROTO_FILES})
    get_filename_component(PROTO_FILENAME ${PROTO_FILE} NAME_WE)
    set(GENERATED_PROTO_SRC "${CMAKE_CURRENT_BINARY_DIR}/${PROTO_FILENAME}.pb.cc")
    set(GENERATED_PROTO_HDR "${CMAKE_CURRENT_BINARY_DIR}/${PROTO_FILENAME}.pb.h")
    set(GENERATED_GRPC_SRC "${CMAKE_CURRENT_BINARY_DIR}/${PROTO_FILENAME}.grpc.pb.cc")
    set(GENERATED_GRPC_HDR "${CMAKE_CURRENT_BINARY_DIR}/${PROTO_FILENAME}.grpc.pb.h")

    add_custom_command(
        OUTPUT ${GENERATED_PROTO_SRC} ${GENERATED_PROTO_HDR} ${GENERATED_GRPC_SRC} ${GENERATED_GRPC_HDR}
        COMMAND ${Protobuf_PROTOC_EXECUTABLE}
        ARGS --proto_path=${CMAKE_CURRENT_SOURCE_DIR} --cpp_out=${CMAKE_CURRENT_BINARY_DIR} ${PROTO_FILE}
        COMMAND ${Protobuf_PROTOC_EXECUTABLE}
        ARGS --proto_path=${CMAKE_CURRENT_SOURCE_DIR} --grpc_out=${CMAKE_CURRENT_BINARY_DIR} --plugin=protoc-gen-grpc=${GRPC_INSTALL_PATH}/bin/grpc_cpp_plugin ${PROTO_FILE}
        DEPENDS ${PROTO_FILE}
        COMMENT "Running protoc on ${PROTO_FILE}"
        VERBATIM
    )

    list(APPEND PROTO_SRCS ${GENERATED_PROTO_SRC})
    list(APPEND PROTO_HDRS ${GENERATED_PROTO_HDR})
    list(APPEND GRPC_SRCS ${GENERATED_GRPC_SRC})
    list(APPEND GRPC_HDRS ${GENERATED_GRPC_HDR})
endforeach()

# Executable
add_executable(AdapterServer server.cpp ${PROTO_SRCS} ${GRPC_SRCS})

# Link libraries
target_link_libraries(AdapterServer ${PROTOBUF_LIBRARIES} ${GRPC_LIBRARIES} ${GRPC++_LIBRARIES})

# Ensure gRPC and protobuf libraries are found
find_library(PROTOBUF_LIBRARIES protobuf HINTS "${GRPC_INSTALL_PATH}/lib")
find_library(GRPC_LIBRARIES grpc HINTS "${GRPC_INSTALL_PATH}/lib")
find_library(GRPC++_LIBRARIES grpc++ HINTS "${GRPC_INSTALL_PATH}/lib")
```

### Recap

1. **Ensure submodules are initialized**: Either clone the repository with `--recurse-submodules` or run `git submodule update --init --recursive`.
2. **Build gRPC**: Follow the steps to configure and build gRPC.
3. **Verify submodules**: Ensure that the `third_party/googletest` directory is populated.

This should resolve the issue with missing `googletest` and allow you to proceed with building gRPC.
