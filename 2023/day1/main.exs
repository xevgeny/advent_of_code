defmodule Main do
  def part1(line) do
    xs = for <<x <- line>>, x >= ?0 and x <= ?9, do: <<x>>
    String.to_integer(List.first(xs) <> List.last(xs))
  end

  @reg ~r/(?=(\d|one|two|three|four|five|six|seven|eight|nine))/
  @digits %{
    one: "1",
    two: "2",
    three: "3",
    four: "4",
    five: "5",
    six: "6",
    seven: "7",
    eight: "8",
    nine: "9"
  }

  def part2(line) do
    to_digit = fn
      <<x>> when x >= ?0 and x <= ?9 -> <<x>>
      x -> Map.fetch!(@digits, String.to_atom(x))
    end

    xs =
      Regex.scan(@reg, line, capture: :all_but_first)
      |> List.flatten()
      |> Enum.map(to_digit)

    String.to_integer(List.first(xs) <> List.last(xs))
  end

  def run do
    File.stream!(~c"input")
    |> Stream.map(&part2/1)
    |> Enum.sum()
    |> IO.puts()
  end
end

Main.run()
