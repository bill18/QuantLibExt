The provided solution should work well, but there are a few other approaches to consider for managing memory and ensuring safety and convenience when dealing with strings returned from a dynamic library.

### Approach 1: Use `std::string` in the C++ Library

If you are working exclusively with C++ and your main program is also C++, you can return `std::string` objects from the library instead of raw pointers. This approach leverages C++'s automatic memory management.

**mylib.h**:

```cpp
#ifndef MYLIB_H
#define MYLIB_H

#include <string>

#ifdef __cplusplus
extern "C" {
#endif

std::string greet(const std::string& name);

#ifdef __cplusplus
}
#endif

#endif // MYLIB_H
```

**mylib.cpp**:

```cpp
#include "mylib.h"

std::string greet(const std::string& name) {
    return "Hello, " + name + "!";
}
```

**main.cpp**:

```cpp
#include <iostream>
#include <dlfcn.h>
#include <string>

typedef std::string (*greet_func)(const std::string&);

int main() {
    void* handle = dlopen("./libmylib.so", RTLD_LAZY);
    if (!handle) {
        std::cerr << "Cannot open library: " << dlerror() << std::endl;
        return 1;
    }

    // Reset errors
    dlerror();

    // Load the symbols
    greet_func greet = (greet_func) dlsym(handle, "greet");
    const char* dlsym_error = dlerror();
    if (dlsym_error) {
        std::cerr << "Cannot load symbol 'greet': " << dlsym_error << std::endl;
        dlclose(handle);
        return 1;
    }

    // Use the function
    std::string result = greet("World");
    std::cout << result << std::endl;

    // Clean up
    dlclose(handle);
    return 0;
}
```

### Approach 2: Use `std::unique_ptr` for Automatic Memory Management

Another approach is to use `std::unique_ptr` to automatically manage memory and ensure it gets freed when no longer needed. This requires a custom deleter to call the library's free function.

**mylib.h** and **mylib.cpp** remain the same as the original approach.

**main.cpp**:

```cpp
#include <iostream>
#include <dlfcn.h>
#include <memory>
#include <string>

typedef const char* (*greet_func)(const char*);
typedef void (*free_func)(const char*);

int main() {
    void* handle = dlopen("./libmylib.so", RTLD_LAZY);
    if (!handle) {
        std::cerr << "Cannot open library: " << dlerror() << std::endl;
        return 1;
    }

    // Reset errors
    dlerror();

    // Load the symbols
    greet_func greet = (greet_func) dlsym(handle, "greet");
    const char* dlsym_error = dlerror();
    if (dlsym_error) {
        std::cerr << "Cannot load symbol 'greet': " << dlsym_error << std::endl;
        dlclose(handle);
        return 1;
    }

    free_func free_string = (free_func) dlsym(handle, "free_string");
    dlsym_error = dlerror();
    if (dlsym_error) {
        std::cerr << "Cannot load symbol 'free_string': " << dlsym_error << std::endl;
        dlclose(handle);
        return 1;
    }

    // Use the functions with std::unique_ptr
    std::unique_ptr<const char, decltype(free_string)> result(greet("World"), free_string);
    std::cout << result.get() << std::endl;

    // Clean up
    dlclose(handle);
    return 0;
}
```

### Approach 3: Use `std::shared_ptr` for Shared Ownership

If you need shared ownership of the returned string, `std::shared_ptr` can be used with a custom deleter.

**mylib.h** and **mylib.cpp** remain the same as the original approach.

**main.cpp**:

```cpp
#include <iostream>
#include <dlfcn.h>
#include <memory>
#include <string>

typedef const char* (*greet_func)(const char*);
typedef void (*free_func)(const char*);

int main() {
    void* handle = dlopen("./libmylib.so", RTLD_LAZY);
    if (!handle) {
        std::cerr << "Cannot open library: " << dlerror() << std::endl;
        return 1;
    }

    // Reset errors
    dlerror();

    // Load the symbols
    greet_func greet = (greet_func) dlsym(handle, "greet");
    const char* dlsym_error = dlerror();
    if (dlsym_error) {
        std::cerr << "Cannot load symbol 'greet': " << dlsym_error << std::endl;
        dlclose(handle);
        return 1;
    }

    free_func free_string = (free_func) dlsym(handle, "free_string");
    dlsym_error = dlerror();
    if (dlsym_error) {
        std::cerr << "Cannot load symbol 'free_string': " << dlsym_error << std::endl;
        dlclose(handle);
        return 1;
    }

    // Use the functions with std::shared_ptr
    std::shared_ptr<const char> result(greet("World"), free_string);
    std::cout << result.get() << std::endl;

    // Clean up
    dlclose(handle);
    return 0;
}
```

### Conclusion

Using `std::string` is the most C++-idiomatic way when both the library and the client code are in C++. It automatically manages memory and avoids manual memory management. When working with C-style strings and requiring interoperability with C, using smart pointers (`std::unique_ptr` or `std::shared_ptr`) with custom deleters is a robust solution to prevent memory leaks.
