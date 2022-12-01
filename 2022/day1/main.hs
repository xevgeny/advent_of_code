import Data.List (sort)
import Data.List.Split (splitOn)

totalCalories :: String -> [Int]
totalCalories s = map (sum . map read . splitOn "\n") (splitOn "\n\n" s)

main = do
  input <- readFile "input"
  let xs = totalCalories input
  putStrLn $ "Part 1: " ++ show (maximum xs)
  putStrLn $ "Part 2: " ++ show (sum . take 3 . reverse . sort $ xs)
