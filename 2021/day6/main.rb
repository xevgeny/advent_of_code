days = 256
input = File.read('./input').split(',').map(&:to_i)
state = Array.new(9, 0)
input.each { |n| state[n] += 1 }
for i in (1..days) do
    tmp = state.shift
    state[6] += tmp
    state[8] = tmp
end
puts state.inject(0, :+)
