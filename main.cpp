#include <iostream>
#include "a/c/b.h"

#define ARRAY_SIZE(_NAME) (sizeof(_NAME)/sizeof(_NAME[0])) 

void print_bool(bool value) {
    if (VersionInfo::git_is_workspace_dirty) {
        std::cout << "true" << std::endl;
    } else {
        std::cout << "false" << std::endl;
    }
}

int main(int argc, const char** argv) {

    //commit hash
    std::cout << "git commit hash: ";
    for (size_t i = 0; i < ARRAY_SIZE(VersionInfo::git_hash); ++i) {
        std::cout << VersionInfo::git_hash[i];
    }
    std::cout << std::endl;

    //commit hash reliable
    std::cout << "git commit hash reliable (aka from a STABLE_ variable): ";
    print_bool(VersionInfo::git_hash_reliable);

    //dirty
    std::cout << "git workspace dirty: ";
    print_bool(VersionInfo::git_is_workspace_dirty);

    //dirty reliable
    std::cout << "git workspace dirty reliable: ";
    print_bool(VersionInfo::git_is_workspace_dirty_reliable);
}