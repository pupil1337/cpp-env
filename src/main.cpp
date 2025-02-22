#include <iostream>

#include "ref.hpp"

void test_ref() {
	Ref<int> a(new int(55)); // = Ref<int>(new int(55));
	std::cout << **a << std::endl;

	// Ref<int> b = Ref<int>(*a); 错误 别这样写
	Ref<int> b = a;
	std::cout << **b << std::endl;
}

int main() {
	test_ref();

	return 0;
}
