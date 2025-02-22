#include "ref.hpp"
#include <cstdio>
#include <iostream>

void func(int a) {
	printf("func...");
}

int main() {
	Ref<int> t;
	std::cout << t.geta() << std::endl;

	func(1);
	return 0;
	std::cout << "run main... and exit." << std::endl;
	return 0;
}
