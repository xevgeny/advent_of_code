#include <map>
#include <unordered_map>
#include <iostream>
#include <sstream>

int playgame1(const int players[2])
{
    int p = 0, n = 0;
    int pp[2] = {players[0], players[1]};
    long ss[2] = {0, 0};
    while (true)
    {
        n += 3;
        p = n % 2 == 0 ? 1 : 0;
        pp[p] = (pp[p] + 3 * n - 4) % 10 + 1;
        ss[p] += pp[p];
        if (ss[p] >= 1000)
            break;
    }
    return std::min(ss[0], ss[1]) * n;
}

struct game_state_t
{
    int player1;
    int player2;
    int score1;
    int score2;
    int next;

    bool operator==(const game_state_t &other) const
    {
        return (player1 == other.player1 && player2 == other.player2 &&
                score1 == other.score1 && score2 == other.score2 && next == other.next);
    }
};

struct game_state_hash
{
    std::size_t operator()(const game_state_t &gs) const
    {
        std::stringstream buf;
        buf << gs.player1 << "#" << gs.player2 << "#";
        buf << gs.score1 << "#" << gs.score2 << "#" << gs.next;
        return std::hash<std::string>{}(buf.str());
    }
};

using game_cache_t = std::unordered_map<game_state_t, std::pair<long, long>, game_state_hash>;

std::pair<long, long> playgame2(game_state_t &gs, game_cache_t &cache, const std::map<int, int> &rf)
{
    std::pair<long, long> wins = {0, 0};
    for (auto const &[sum, freq] : rf)
    {
        int pp[2] = {gs.player1, gs.player2};
        int ss[2] = {gs.score1, gs.score2};
        pp[gs.next] = (pp[gs.next] + sum - 1) % 10 + 1;
        ss[gs.next] += pp[gs.next];
        if (ss[gs.next] < 21)
        {
            std::pair<long, long> res;
            game_state_t next = {pp[0], pp[1], ss[0], ss[1], gs.next == 0 ? 1 : 0};

            auto cache_res = cache.find(next);
            if (cache_res == cache.end())
            {
                res = playgame2(next, cache, rf);
                cache[next] = res;
            }
            else
                res = cache_res->second;

            wins.first += freq * res.first;
            wins.second += freq * res.second;
        }
        else
            gs.next == 0 ? wins.first += freq : wins.second += freq;
    }
    return wins;
}

int main()
{
    int players[] = {4, 9};
    std::cout << "Answer 1: " << playgame1(players) << std::endl;

    // Initialize roll frequences (optional step)
    std::map<int, int> rf;
    auto rolls = {1, 2, 3};
    for (int i : rolls)
        for (int j : rolls)
            for (int k : rolls)
                if (rf.find(i + j + k) != rf.end())
                    rf[i + j + k] += 1;
                else
                    rf[i + j + k] = 1;

    game_cache_t game_cache;
    game_state_t game_state = {4, 9, 0, 0, 0};
    auto res = playgame2(game_state, game_cache, rf);
    std::cout << "Answer 2: " << std::max(res.first, res.second) << std::endl;

    return 0;
}
