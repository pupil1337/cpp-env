#ifndef REF_HPP
#define REF_HPP

template <typename T>
class Ref {
	void ref(const Ref& p_from) {
		if (ptr == p_from.ptr) {
			return;
		}

		unref();

		ptr = p_from.ptr;
		count = p_from.count;
		if (count) {
			++(*count);
		}
	}

	void unref() {
		if (count && --(*count) == 0) {
			delete ptr;
			delete count;
		}

		ptr = nullptr;
		count = nullptr;
	}

public:
	inline T* operator*() const {
		return ptr;
	}
	void operator=(const Ref& p_from) {
		ref(p_from);
	}

public:
	Ref(T* p_ptr) :
			ptr(p_ptr), count(new int(1)) {}

	Ref(const Ref& p_from) {
		ref(p_from);
	}

	~Ref() {
		unref();
	}

private:
	T* ptr = nullptr;
	int* count = nullptr;
};

#endif // REF_HPP
