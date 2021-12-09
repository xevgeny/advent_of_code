import scala.annotation.tailrec
import scala.collection.mutable
import scala.io.Source.fromFile

case class AxialCoordinate(q: Int, r: Int)

abstract class Color
case object Black
case object White

abstract class Cardinal
case object East extends Cardinal
case object SouthEast extends Cardinal
case object SouthWest extends Cardinal
case object West extends Cardinal
case object NorthWest extends Cardinal
case object NorthEast extends Cardinal

object Cardinal {
  val all = List(
    East,
    SouthEast,
    SouthWest,
    West,
    NorthWest,
    NorthEast,
  )
}

def stringToCardinal(xs: List[Char]): List[Cardinal] =
  xs match {
    case Nil => Nil
    case 'e' :: tail => East +: stringToCardinal(tail)
    case 's' :: 'e' :: tail => SouthEast +: stringToCardinal(tail)
    case 's' :: 'w' :: tail => SouthWest +: stringToCardinal(tail)
    case 'w' :: tail => West +: stringToCardinal(tail)
    case 'n' :: 'w' :: tail => NorthWest +: stringToCardinal(tail)
    case 'n' :: 'e' :: tail => NorthEast +: stringToCardinal(tail)
    case _ => throw new Exception
  }

class Lobby {
  val blackTiles = new mutable.HashSet[AxialCoordinate]

  def nextTile(curr: AxialCoordinate, c: Cardinal): AxialCoordinate = {
    (curr, c) match {
      case (AxialCoordinate(q, r), East) => AxialCoordinate(q + 1, r)
      case (AxialCoordinate(q, r), SouthEast) => AxialCoordinate(q, r + 1)
      case (AxialCoordinate(q, r), SouthWest) => AxialCoordinate(q - 1, r + 1)
      case (AxialCoordinate(q, r), West) => AxialCoordinate(q - 1, r)
      case (AxialCoordinate(q, r), NorthWest) => AxialCoordinate(q , r - 1)
      case (AxialCoordinate(q, r), NorthEast) => AxialCoordinate(q + 1, r - 1)
      case _ => throw new Exception
    }
  }

  def flipTile(s: String): Unit = {
    var tile = AxialCoordinate(0, 0)
    val xs = stringToCardinal(s.toList)
    xs.foreach(c => tile = nextTile(tile, c))
    if (blackTiles.contains(tile)) blackTiles.remove(tile)
    else blackTiles.add(tile)
  }

  def getAdjacentTiles(curr: AxialCoordinate): List[AxialCoordinate] = 
    Cardinal.all.map(c => nextTile(curr, c))

  def flipForDay(): Unit = {
    val toFlip = new mutable.HashSet[AxialCoordinate]

    blackTiles.foreach { tile =>
      // check flip condition for black tile
      val count = getAdjacentTiles(tile).count(blackTiles.contains)
      if (count == 0 || count > 2) toFlip.add(tile)
      // check flip condition for all adjacent white tiles
      getAdjacentTiles(tile).foreach { adj =>
        if (!blackTiles.contains(adj)) {
          val count = getAdjacentTiles(adj).count(blackTiles.contains)
          if (count == 2) toFlip.add(adj)
        }
      }
    }

    toFlip.foreach { tile =>
      if (blackTiles.contains(tile)) blackTiles.remove(tile)
      else blackTiles.add(tile)
    }
  }
}


object Main {
    def main(args: Array[String]): Unit = {
      val input: List[String] = fromFile("./input").getLines.toList

      val lobby = new Lobby
      input.foreach(lobby.flipTile)
      println(s"Answer 1: ${lobby.blackTiles.size}")

      for (day <- 1 to 100) {
        lobby.flipForDay()
        println(s"Day $day: ${lobby.blackTiles.size}")
      }
    }
}