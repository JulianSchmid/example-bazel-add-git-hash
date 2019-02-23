#include <iostream>
#include "b.h"

#define ARRAY_SIZE(_NAME) (sizeof(_NAME)/sizeof(_NAME[0])) 

int main(int argc, const char** argv) {
    std::cout << "Git Hash: ";
    for (size_t i = 0; i < ARRAY_SIZE(VersionInfo::git_hash); ++i) {
        std::cout << VersionInfo::git_hash[i];
    }
    std::cout << std::endl;
    if (VersionInfo::git_is_workspace_dirty) {
        std::cout << "git workspace is dirty:" << std::endl;
    } else {
        std::cout << "git workspace is clean:" << std::endl;
    }
    
}