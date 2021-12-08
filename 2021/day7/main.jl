using DelimitedFiles
using Statistics
using Printf
using Optim

N = readdlm("./input", ',', Int)

function fuel_cost_1(pos)
    fuel_cost = 0
    for i in 1:length(N)
        fuel_cost += abs(N[i] - pos)
    end
    return fuel_cost
end

function fuel_cost_2(pos)
    fuel_cost = 0
    for i in 1:length(N)
        n = abs(N[i] - pos)
        sum = n * (n + 1) / 2
        fuel_cost += sum
    end
    return fuel_cost
end

@printf "Answer 1: %d\n" fuel_cost_1(median(N))
@printf "Answer 2: %d\n" fuel_cost_2(minimum([floor(mean(N)), ceil(mean(N))]))