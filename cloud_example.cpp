#include "cloud.h"

int main() {
	CloudGrid cg("hello", 0.5, 24.0);
	cg.resize_cloud({{-1, -2, 50, 50}});
	cg.write_cloud("cloud.txt");
	return 0;
}
