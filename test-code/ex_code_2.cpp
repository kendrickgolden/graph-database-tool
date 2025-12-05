#include <string>

int countA(const std::string& str) {
    int count = 0;
    for (char c : str) {
        if (c == 'a') {
            count++;
        }
    }
    return count;
}

int countZ(const std::string& str) {
    int count = 0;
    for (char c : str) {
        if (c == 'z') {
            count++;
        }
    }
    return count;
}

std::string repeatThreeTimes(const std::string& str) {
    return str + str + str;
}

int countAZ(const std::string& str) {
    int count = 0;
    count += countA(str);
    count += countZ(str);
    return count;
}
