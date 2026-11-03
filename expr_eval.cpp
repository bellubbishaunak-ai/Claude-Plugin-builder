#include <iostream>
#include <string>
#include <cctype>
using namespace std;
using ll = long long;

const char* p;
void err() { throw 0; }
void skip() { while (*p == ' ' || *p == '\t' || *p == '\r') p++; }
ll expr();

ll atom() {
    skip();
    if (*p == '(') {
        p++;
        ll v = expr();
        skip();
        if (*p != ')') err();
        p++;
        return v;
    }
    if (!isdigit((unsigned char)*p)) err();
    ll v = 0;
    while (isdigit((unsigned char)*p)) v = v * 10 + (*p++ - '0');
    return v;
}

ll unary() {
    skip();
    if (*p == '-') return -unary();
    return atom();
}

ll power() {
    ll v = unary();

    skip();
    if (*p != '^') return v;
    p++;
    ll e = power();  // ^ is right-associative: a^b^c = a^(b^c)
    if (e < 0) err();
    ll r = 1;
    while (e--) r *= v;
    return r;
}

ll term() {
    ll v = power();
    for (;;) {
        skip();
        if (*p == '*') { p++; v *= power(); }
        else if (*p == '/') { p++; ll d = power(); if (!d) err(); v /= d; }
        else return v;
    }
}

ll expr() {
    ll v = term();
    for (;;) {
        skip();
        if (*p == '+') { p++; v += term(); }
        else if (*p == '-') { p++; v -= term(); }
        else return v;
    }
}

int main() {
    string line;
    while (getline(cin, line)) {
        p = line.c_str();
        try {
            ll v = expr();
            skip();
            if (*p) err();
            cout << v << "\n";
        } catch (...) { cout << "error\n"; }
    }
}
