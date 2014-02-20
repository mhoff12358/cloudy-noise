#include <string>
#include <sstream>
#include <iostream>
#include <fstream>
#include <list>
#include <vector>
#include <array>
#include <math.h>

#define hvt uint32_t

using std::string;
using std::hash;
using std::list;
using std::vector;
using std::array;

class CloudGrid {
private:
	std::string seed;

	float max_hash;
	size_t cloud_hashcap;
	float max_radius;
	int over_scan;

	array<int, 4> cloud_size = {{0, 0, 0, 0}}; //Size is minx, miny, maxx, maxy
	vector<vector<float>> cloud;

public:
	CloudGrid(string, float, float);
	CloudGrid(float, float);

	hvt pointhash(int x, int y, string mod);
	hvt pointhash(int x, int y);
	bool check_point(int x, int y);
	bool check_point(hvt hashval);
	float point_height(int x, int y);
	float point_height(hvt hashval);
	float point_radius(int x, int y);
	float point_radius(hvt hashval);

	float height_finalize_fn(int, int, float);
	float height_add_fn(float, float);
	float distance_fn(float, float, float);

	void write_cloud(string);
	void resize_cloud(array<int, 4>);
	void generate_cloud();
	void generate_cloud(array<int, 4>);
	void add_cloud(int, int, array<int, 4>);

	float get_point(int, int);
	void set_point(int, int, float);
	array<int, 4> get_size();
	void set_size(array<int, 4>);
	// void compute_cloud();
};
