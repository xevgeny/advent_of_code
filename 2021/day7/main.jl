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

res = optimize(fuel_cost_2, minimum(N), maximum(N), Brent())
println(res) # print optimizer summary
@printf "Answer 2: %d" fuel_cost_2(Int(round(res.minimizer)))

#= sample output
Answer 1: 342534
Results of Optimization Algorithm
 * Algorithm: Brent's Method
 * Search Interval: [0.000000, 1936.000000]
 * Minimizer: 4.744910e+02
 * Minimum: 9.400409e+07
 * Iterations: 7
 * Convergence: max(|x - x_upper|, |x - x_lower|) <= 2*(1.5e-08*|x|+2.2e-16): true
 * Objective Function Calls: 8
Answer 2: 94004208
=#
