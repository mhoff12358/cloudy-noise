#include "cloud.h"

// using namespace std;

CloudGrid::CloudGrid(string seed_val, float cloud_prob, float max_rad) {
	seed = seed_val;
	cloud_hashcap = (size_t)(((size_t)-1)*cloud_prob+.5);
	max_radius = max_rad;
	over_scan = (int)max_rad;
}

float CloudGrid::pointhash(int x, int y) {
	string newmod;
	return pointhash(x, y, newmod);
}

float CloudGrid::pointhash(int x, int y, string mod) {
	std::stringstream hashstr;
	hashstr << x << y << mod << seed;
	hash<string> hashfn;
	return hashfn(hashstr.str());
}

bool CloudGrid::check_point(int x, int y) {
	return check_point(pointhash(x, y));
}

bool CloudGrid::check_point(size_t hashval) {
	return (hashval < cloud_hashcap);
}

float CloudGrid::point_height(int x, int y) {
	return point_height(pointhash(x, y));
}

float CloudGrid::point_height(size_t hashval) {
	return log((float)hashval/(float)cloud_hashcap*(1-exp(-1))+exp(-1))+1;
}

float CloudGrid::point_radius(int x, int y) {
	return point_radius(pointhash(x, y));
}

float CloudGrid::point_radius(size_t hashval) {
	return max_radius*(float)hashval/(float)((size_t)-1);
}

float CloudGrid::height_finalize_fn(int x, int y, float height) {
	return 1.0-height;
}

float CloudGrid::height_add_fn(float h1, float h2) {
	return h1 * h2;
}

float CloudGrid::distance_fn(float base_height, float dist, float rad) {
	return 1-(1-base_height)*pow((rad-dist)/rad, 2);
}

void CloudGrid::set_point(int x, int y, float newval) {
	if (x >= cloud_size[0] && x < cloud_size[2] &&
		y >= cloud_size[1] && y < cloud_size[3]) {
		cloud[x-cloud_size[0]][y-cloud_size[1]] = newval;
	}
}

float CloudGrid::get_point(int x, int y) {
	if (x >= cloud_size[0] && x < cloud_size[2] &&
		y >= cloud_size[1] && y < cloud_size[3]) {
		return cloud[x-cloud_size[0]][y-cloud_size[1]];
	}
	return 0.0;
}

void CloudGrid::resize_cloud(array<int, 4> newsize) {
	//
	if (newsize[1] < cloud_size[1]) {
		for (vector<vector<float>>::iterator extender = cloud.begin(); extender != cloud.end(); ++extender) {
			extender->insert(extender->begin(), cloud_size[1]-newsize[1], 1.0);
		}
	}
	if (newsize[3] > cloud_size[3]) {
		for (vector<vector<float>>::iterator extender = cloud.begin(); extender != cloud.end(); ++extender) {
			extender->insert(extender->end(), newsize[3]-cloud_size[3], 1.0);
		}
	}
	if (newsize[0] < cloud_size[0]) {
		vector<float> newcol(newsize[3]-newsize[1], 1.0);
		cloud.insert(cloud.begin(), cloud_size[0]-newsize[0], newcol);
	std::cout << cloud.size() << std::endl;;
	}
	if (newsize[2] > cloud_size[2]) {
		vector<float> newcol(newsize[3]-newsize[1], 1.0);
		cloud.insert(cloud.end(), newsize[2]-cloud_size[2], newcol);
	std::cout << cloud.size() << std::endl;;
	}

	array<int, 4> preserve_area = cloud_size;
	cloud_size = newsize;

	generate_cloud(preserve_area);
}

void CloudGrid::generate_cloud() {
	generate_cloud({{0, 0, 0, 0}});
}

void CloudGrid::generate_cloud(array<int, 4> preserve_area) {
	/*
	Should add clouds for each point that could add to something outside the preserve_area.
	This means an x and y range from cloudmin-overscan to preservemin+overscan and
	preservemax-overscan to cloudmax+overscan

	These overlap awkwardly, especially since preservemin+overscan and preservemax-overscan can overlap
	*/

	if (preserve_area[1]+over_scan >= cloud_size[3]-over_scan) {
		//The y areas overlap (or at least bump right up against eachother) so this can just
		//iterate over all x and y values.
		for (int x = cloud_size[0]-over_scan; x < cloud_size[2]+over_scan; x++) {
			for (int y = cloud_size[1]-over_scan; y < cloud_size[3]+over_scan; y++) {
				add_cloud(x, y, preserve_area);
			}
		}
	} else {
		//There must be a gap in the y range, so iterate over x and then iterate over y, checking
		//to see if there is a gap that needs to be jumped based on the x range.
		for (int x = cloud_size[0]-over_scan; x < cloud_size[2]+over_scan; x++) {
			if (x <= preserve_area[0]+over_scan || x >= preserve_area[2]-over_scan) {
				//No gap in the y range, because everything will be in the x range
				for (int y = cloud_size[1]-over_scan; y < cloud_size[3]+over_scan; y++) {
					add_cloud(x, y, preserve_area);
				}
			} else {
				for (int y = cloud_size[1]-over_scan; y < preserve_area[1]+over_scan; y++) {
					add_cloud(x, y, preserve_area);
				}
				for (int y = preserve_area[3]-over_scan; y < cloud_size[3]+over_scan; y++) {
					add_cloud(x, y, preserve_area);
				}
			}
		}
	}
}

void CloudGrid::add_cloud(int x, int y, array<int, 4> preserve_area) {
	float pheight = point_height(x, y);
	float pradius = point_radius(x, y);
	int rad = (int)(pradius+1);
	for (int px = x - rad; px <= x + rad; px++) {
		for (int py = y - rad; py <= y + rad; py++) {
			float dist = pow(pow(x-px,2)+pow(y-py,2),.5);
			if (dist < pradius) {
				set_point(px, py, height_add_fn(get_point(px, py), distance_fn(pheight, dist, pradius)));
			}
		}
	}
}

void CloudGrid::write_cloud(string filename) {
	std::ofstream ofile;
	ofile.open(filename);
	for (vector<vector<float>>::iterator col = cloud.begin(); col != cloud.end(); ++col) {
		for (vector<float>::iterator val = col->begin(); val != col->end(); ++val) {
			ofile << *val << '|';
		}
		ofile << std::endl;
	}
	ofile.close();
}

// void CloudGrid::compute_cloud(int minx, int maxx, int miny, int maxy) {

// }

int main() {
	CloudGrid cg("hello", 0.5, 24.0);
	cg.resize_cloud({{-1, -2, 50, 50}});
	// cg.resize_cloud(size);
	cg.write_cloud("cloud.txt");
	return 0;
}
