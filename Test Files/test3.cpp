#include <iostream>
using namespace std;

// This is a single-line comment
/* This is a 
   multi-line comment */

class TestClass {
private:
    int x;
    float y;
    
public:
    TestClass(int a, float b) : x(a), y(b) {}
    
    void printValues() {
        cout << "x = " << x << ", y = " << y << endl;
    }
    
    bool isPositive() {
        return (x > 0) && (y > 0.0);
    }
};

int main() {
    int num1 = 42;
    float num2 = 3.14;
    char c = 'A';
    string message = "Hello, World!";
    
    TestClass test(10, 20.5);
    test.printValues();
    
    if (test.isPositive()) {
        cout << "Both values are positive!" << endl;
    } else {
        cout << "At least one value is not positive!" << endl;
    }
    
    for (int i = 0; i < 5; ++i) {
        num1 += i;
        num2 *= 1.1;
    }
    
    while (num1 > 45) {
        num1--;
    }
    
    switch (num1) {
        case 42:
            cout << "The answer to everything!" << endl;
            break;
        default:
            cout << "Just a number: " << num1 << endl;
    }
    
    // Bitwise operations
    int a = 5 & 3;  // Bitwise AND
    int b = 5 | 3;  // Bitwise OR
    int c = 5 ^ 3;  // Bitwise XOR
    int d = ~5;     // Bitwise NOT
    int e = 5 << 1; // Left shift
    int f = 5 >> 1; // Right shift
    
    return 0;
}