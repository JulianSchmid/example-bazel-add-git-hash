#include <iostream>
#include "b.h"

#define ARRAY_SIZE(_NAME) (sizeof(_NAME)/sizeof(_NAME[0])) 

int main(int argc, const char** argv) {
    std::cout << "Git Hash:" << std::endl;
    for (size_t i = 0; i < ARRAY_SIZE(VersionInfo::git_hash); ++i) {
        std::cout << VersionInfo::git_hash[i];
    }
    std::cout << std::endl;
}