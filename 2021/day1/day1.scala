import scala.io.Source._

@main def main = 
  val input: List[String] = fromFile("./input").getLines.toList
  val res = input.map(_.toLong).foldLeft((0, Long.MaxValue)) {
    case ((acc, prev), i) =>
      if i > prev then (acc + 1, i) else (acc, i)
  }
  println(res._1)
