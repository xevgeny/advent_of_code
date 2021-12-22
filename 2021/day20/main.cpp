#include <iostream>
#include <fstream>
#include <sstream>
#include <set>

using point_t = std::pair<int, int>;

void printset(const std::set<point_t> &points, int size, int it)
{
    for (int i = -it; i < size + it; i++)
    {
        for (int j = -it; j < size + it; j++)
            std::cout << (points.find({i, j}) != points.end() ? '#' : '.');
        std::cout << std::endl;
    }
}

void readinput(const std::string &fname, std::string &algo, std::set<point_t> &points, int &size)
{
    std::ifstream file(fname);
    std::stringstream buf;
    std::string line;

    buf << file.rdbuf();
    std::getline(buf, algo);

    int i = 0;
    while (std::getline(buf, line))
    {
        if (!line.empty())
        {
            int j = 0;
            for (auto c : line)
            {
                if (c == '#')
                    points.insert({i, j});
                ++j;
            }
            ++i;
        }
    }
    size = i;
}

int enhannce(const std::string &algo, const std::set<point_t> &points, int size, int iterations)
{
    std::set<point_t> seta = points;
    std::set<point_t> setb;

    char inf = '.';
    for (int it = 0; it < iterations; it++)
    {
        int next = it + 1;
        for (int n = -next; n < size + next; n++)
        {
            for (int m = -next; m < size + next; m++)
            {
                std::stringstream sbin;
                for (int i = -1; i <= 1; i++)
                {
                    for (int j = -1; j <= 1; j++)
                    {
                        int ii = n + i;
                        int jj = m + j;
                        if (-it <= ii && ii < size + it && -it <= jj && jj < size + it)
                            seta.find({n + i, m + j}) != seta.end() ? sbin << '1' : sbin << '0';
                        else
                            inf == '#' ? sbin << '1' : sbin << '0';
                    }
                }
                int num = std::stoi(sbin.str(), 0, 2);
                if (algo[num] == '#')
                    setb.insert({n, m});
            }
        }
        seta = setb;
        setb.clear();
        if (algo[0] == '#') // turn on/off all pixels
            inf = inf == '.' ? '#' : '.';
    }

    return seta.size();
}

int main()
{
    int size;
    std::string algo;
    std::set<point_t> on_points;

    readinput("./input", algo, on_points, size);
    std::cout << "Answer 1: " << enhannce(algo, on_points, size, 2) << std::endl;
    std::cout << "Answer 2: " << enhannce(algo, on_points, size, 50) << std::endl;

    return 0;
}