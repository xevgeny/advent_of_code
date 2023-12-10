import scala.io.Source._
import scala.util.boundary, boundary.break
import scala.collection.mutable._

type Pos = (Int, Int)

val connections: Map[Char, List[(Int, Int)]] = Map(
  'S' -> ((-1, 0) :: (0, 1) :: (1, 0) :: (0, -1) :: Nil),
  '|' -> ((-1, 0) :: (1, 0) :: Nil),
  '-' -> ((0, -1) :: (0, 1) :: Nil),
  'L' -> ((-1, 0) :: (0, 1) :: Nil),
  'J' -> ((-1, 0) :: (0, -1) :: Nil),
  '7' -> ((0, -1) :: (1, 0) :: Nil),
  'F' -> ((0, 1) :: (1, 0) :: Nil),
  '.' -> Nil
)

def getNeighbors(pos: Pos, input: List[String]): List[Pos] =
  val res = ListBuffer[Pos]()
  for (i, j) <- connections(input(pos._1)(pos._2)) do
    for (ii, jj) <- connections(input(pos._1+i)(pos._2+j)) do
      if i+ii == 0 && j+jj == 0 then res += ((pos._1+i, pos._2+j))
  res.toList

def findStartPos(input: List[String]): Pos =
  boundary:
    for (line, i) <- input.zipWithIndex do
      val j = line.indexOf("S")
      if j != -1 then break((i, j))
    (0, 0)

def replaceStartPos(pos: Pos, input: List[String]): List[String] =
  var xs = List[Pos]()
  for (i, j) <- connections(input(pos._1)(pos._2)) do
    for (ii, jj) <- connections(input(pos._1+i)(pos._2+j)) do
      if i+ii == 0 && j+jj == 0 then xs ::= ((i, j))
  xs match
    case a :: b :: Nil => 
      boundary:
        for (k, v) <- connections do
          if v == a :: b :: Nil || v == b :: a :: Nil then
            break(input.updated(pos._1, input(pos._1).replace('S', k)))
        input
    case _ => input

@main def main =
  var input = fromFile("input").getLines.toList
  val startPos = findStartPos(input)
  input = replaceStartPos(startPos, input)

  // Part 1: Dijkstra variation
  val q = PriorityQueue((0, startPos)).reverse
  val dists = Map(startPos -> 0)
  while q.nonEmpty do
    val (dist, pos) = q.dequeue()
    for newPos <- getNeighbors(pos, input) do
      val newDist = dist + 1
      if newDist < dists.getOrElse(newPos, Int.MaxValue) then
        dists(newPos) = newDist
        q.enqueue((newDist, newPos))
  println(s"Part 1: ${dists.maxBy(_._2)._2}")

  // Part 2:
  // cross horizontal slice of the pipe from left to right
  // count number of vertical pipes along the way: L-7, F-J, |
  // odd - inside, even - outside
  val pipePos = dists.keySet
  var inside = 0
  for i <- (pipePos.map(_._1).min to pipePos.map(_._1).max) do
    val posSlice = pipePos.filter(_._1 == i)
    var cnt = 0
    var prev: Option[Char] = None
    for j <- (posSlice.map(_._2).min to posSlice.map(_._2).max) do
      if pipePos.contains((i, j)) then
        (prev, input(i)(j)) match
          case (_, '|') | (Some('L'), '7') | (Some('F'), 'J') =>
            cnt += 1
          case _ => // noop
        if input(i)(j) != '-' then prev = Some(input(i)(j))
      else if cnt % 2 == 1 then inside += 1
  println(s"Part 2: ${inside}")
