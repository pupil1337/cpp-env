#include <chrono>
#include <cstdio>
#include <ratio>
#include <thread>

#include "ref.hpp"

constexpr int FPS = 60;
constexpr std::chrono::nanoseconds FRAME_TIME(1000000000 / FPS);

void test_ref() {
	Ref<int> a(new int(55)); // = Ref<int>(new int(55));
	printf("Ref<int> a.ptr = %d\n", **a);

	// Ref<int> b = Ref<int>(*a); 错误 别这样写
	Ref<int> b = a;
	printf("Ref<int> b.ptr = %d\n", **b);
}

int main() {
	test_ref();

	int frame = 0;
	auto last_time = std::chrono::high_resolution_clock::now();
	while (1) {
		// 游戏逻辑
		// TODO

		auto curr_time = std::chrono::high_resolution_clock::now();
		auto elapsed = curr_time - last_time;
		last_time = curr_time;
		printf("Frame: %d, Time: %f\n", ++frame, std::chrono::duration_cast<std::chrono::duration<float, std::milli>>(elapsed).count());
		if (elapsed < FRAME_TIME) {
			auto sleep_time = FRAME_TIME - elapsed;
			printf("Sleep Time: %f\n", std::chrono::duration_cast<std::chrono::duration<float, std::milli>>(sleep_time).count());
			std::this_thread::sleep_for(sleep_time);
			last_time += sleep_time;
		}
	}
	return 0;
}
