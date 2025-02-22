#ifndef REF_HPP
#define REF_HPP

template <typename T>
class Ref {
private:
	T* reference;
	int* ref_count;

public:
	int geta() {
	}
};

#endif // REF_HPP
