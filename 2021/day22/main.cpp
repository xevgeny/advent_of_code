#include <iostream>
#include <fstream>
#include <sstream>
#include <regex>
#include <string>

struct cuboid_t
{
    int x0, x1, y0, y1, z0, z1;

    cuboid_t intersect(const cuboid_t &other) const
    {
        return cuboid_t{
            std::max(x0, other.x0),
            std::min(x1, other.x1),
            std::max(y0, other.y0),
            std::min(y1, other.y1),
            std::max(z0, other.z0),
            std::min(z1, other.z1),
        };
    }

    bool is_intersection() const
    {
        return (x1 - x0 >= 0 && y1 - y0 >= 0 && z1 - z0 >= 0);
    }

    long vol() const
    {
        return (long) (x1 - x0 + 1) * (y1 - y0 + 1) * (z1 - z0 + 1);
    }
};

struct signed_cuboid_t : cuboid_t
{
    bool sign;

    std::string str() const
    {
        std::stringstream buf;
        buf << (sign ? "on" : "off")
            << " x=" << x0 << ".." << x1
            << ",y=" << y0 << ".." << y1
            << ",z=" << z0 << ".." << z1;
        return buf.str();
    }
};

signed_cuboid_t parsecub(const std::string &input)
{
    std::smatch sm;
    std::regex r("-?\\d+");
    std::vector<int> vec;
    auto iter = input.cbegin();
    while (std::regex_search(iter, input.cend(), sm, r))
    {
        vec.push_back(std::stoi(sm[0]));
        iter += sm.position() + sm.length();
    }
    return {vec[0], vec[1], vec[2], vec[3], vec[4], vec[5], input.rfind("on", 0) == 0};
}

void readinput(const std::string &fname, const bool filter, std::vector<signed_cuboid_t> &vec)
{
    std::ifstream file(fname);
    std::stringstream buf;
    std::string line;
    buf << file.rdbuf();
    while (std::getline(buf, line))
    {
        auto cub = parsecub(line);
        if (!filter || filter && cub.x0 >= -50 && cub.x0 <= 50) 
            vec.push_back(cub);
    }
}

/*
          +-------+
          |C      |
  +-------+---+   |
  |A      |   |   |
  |   +---+---+   |
  |   |   |   |   |
  +---+---+---+   |
      |B  |   |   |
      +---+---+---+

  Total volume of A          : A
  Total volume of A and B    : A, B, -A∩B
  Total volume of A, B, and C: A, B, -A∩B, C, -A∩C, -B∩C, A∩B∩C
*/
long long totalvol(const std::vector<signed_cuboid_t> &vec)
{
    std::vector<signed_cuboid_t> res;
    for (const auto &cub : vec)
    {
        size_t size = res.size();
        for (int i = 0; i < size; ++i)
        {
            cuboid_t inter = cub.intersect(res[i]);
            if (inter.is_intersection())
                res.push_back({inter.x0, inter.x1, inter.y0, inter.y1, inter.z0, inter.z1, !res[i].sign});
        }
        if (cub.sign)
            res.push_back(cub);
    }
    long long total = 0;
    for (const auto &cub : res)
        total += (cub.sign ? 1 : -1) * cub.vol();
    return total;
}

int main()
{
    signed_cuboid_t c1 = parsecub("on x=10..12,y=10..12,z=10..12");
    signed_cuboid_t c2 = parsecub("on x=11..13,y=11..13,z=11..13");
    signed_cuboid_t c3 = parsecub("off x=9..11,y=9..11,z=9..11");
    signed_cuboid_t c4 = parsecub("on x=10..10,y=10..10,z=10..10");
    std::vector<signed_cuboid_t> test_vec = {c1, c2, c3, c4};
    assert(totalvol(test_vec) == 39);

    std::vector<signed_cuboid_t> vec1;
    readinput("./input", true, vec1);
    std::cout << "Answer 1: " << totalvol(vec1) << std::endl;

    std::vector<signed_cuboid_t> vec2;
    readinput("./input", false, vec2);
    std::cout << "Answer 2: " << totalvol(vec2) << std::endl;
}