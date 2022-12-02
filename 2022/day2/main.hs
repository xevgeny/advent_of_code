import Data.List.Split (splitOn)

-- part 1

score1 :: String -> Int
score1 "A X" = 4
score1 "A Y" = 8
score1 "A Z" = 3
score1 "B X" = 1
score1 "B Y" = 5
score1 "B Z" = 9
score1 "C X" = 7
score1 "C Y" = 2
score1 "C Z" = 6

-- part 2

data Fig = Rock | Paper | Scissors deriving (Show, Eq)

parseFig :: String -> Fig
parseFig "A" = Rock
parseFig "B" = Paper
parseFig "C" = Scissors
parseFig fig = error $ "Invalid figure: " ++ fig

figScore :: Fig -> Int
figScore Rock = 1
figScore Paper = 2
figScore Scissors = 3

data Result = Win | Lose | Draw deriving (Show, Eq)

parseResult :: String -> Result
parseResult "X" = Lose
parseResult "Y" = Draw
parseResult "Z" = Win
parseResult res = error $ "Invalid result: " ++ res

resultScore :: Result -> Int
resultScore Lose = 0
resultScore Draw = 3
resultScore Win = 6

game :: Fig -> Result -> Fig
game Rock Win = Paper
game Rock Lose = Scissors
game Paper Win = Scissors
game Paper Lose = Rock
game Scissors Win = Rock
game Scissors Lose = Paper
game x Draw = x

score2 :: String -> Int
score2 str = do
  let [fig1, res] = splitOn " " str
  let fig2 = game (parseFig fig1) (parseResult res)
  figScore fig2 + resultScore (parseResult res)

main = do
  input <- readFile "input"
  let lines = splitOn "\n" input
  putStrLn $ "Answer 1: " ++ show (sum $ map score1 lines)
  putStrLn $ "Answer 2: " ++ show (sum $ map score2 lines)
