#include <iostream>
#include <vector>
#include <algorithm>

int addThree(int a, int b, int c) {
    return a + b + c;
}

int multiplyThree(int x, int y, int z) {
    return x * y * z;
}

int subtractThree(int p, int q, int r) {
    return p - q - r;
}

std::string removeFirstLetter(const std::string& s) {
    if (s.empty()) return s;
    return s.substr(1);
}

std::string removeSecondLetter(const std::string& s) {
    if (s.size() < 2) return s;
    return s.substr(0,1) + s.substr(2);
}

std::string removeFifthLetter(const std::string& s) {
    if (s.size() < 5) return s;
    return s.substr(0,4) + s.substr(5);
}

std::string reverseString(const std::string& s) {
    std::string rev = s;
    std::reverse(rev.begin(), rev.end());
    return rev;
}

std::pair<std::string,std::string> longestAndShortest(const std::vector<std::string>& v) {
    if (v.empty()) return {"", ""};
    std::string longest = v[0];
    std::string shortest = v[0];
    for (const auto& s : v) {
        if (s.length() > longest.length()) longest = s;
        if (s.length() < shortest.length()) shortest = s;
    }
    return {longest, shortest};
}

int countVowels(const std::string& s) {
    int count = 0;
    for (char c : s) {
        char lower = std::tolower(c);
        if (lower == 'a' || lower == 'e' || lower == 'i' || lower == 'o' || lower == 'u') {
            count++;
        }
    }
    return count;
}

// 10. Example function: print numbers up to n and their squares (≥10 lines)
void printSquares(int n) {
    if (n < 1) {
        std::cout << "Number must be >= 1\n";
        return;
    }
    for (int i = 1; i <= n; ++i) {
        int square = i * i;
        std::cout << "Number: " << i << " Square: " << square << "\n";
    }
}

