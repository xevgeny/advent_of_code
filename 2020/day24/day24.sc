import scala.annotation.tailrec
import scala.collection.mutable
import scala.io.Source.fromFile

abstract class Color
case object White extends Color
case object Black extends Color

case class AxialCoordinate(q: Int, r: Int)

val RootAxialCoordinate = AxialCoordinate(0, 0)

abstract class Cardinal
case object East extends Cardinal
case object SouthEast extends Cardinal
case object SouthWest extends Cardinal
case object West extends Cardinal
case object NorthWest extends Cardinal
case object NorthEast extends Cardinal

// These directions are given in your list, respectively, as e, se, sw, w, nw, and ne
// TODO @tailrec
def stringToCardinal(xs: List[Char]): List[Cardinal] =
  xs match {
    case Nil => Nil
    case 'e' :: tail => East +: stringToCardinal(tail)
    case 's' :: 'e' :: tail => SouthEast +: stringToCardinal(tail)
    case 's' :: 'w' :: tail => SouthWest +: stringToCardinal(tail)
    case 'w' :: tail => West +: stringToCardinal(tail)
    case 'n' :: 'w' :: tail => NorthWest +: stringToCardinal(tail)
    case 'n' :: 'e' :: tail => NorthEast +: stringToCardinal(tail)
    case _ => throw new IllegalArgumentException
  }



class Lobby {
  val hexStore = mutable.HashMap[AxialCoordinate, Color]()

  def nextTile(curr: AxialCoordinate, c: Cardinal): AxialCoordinate = {
    (curr, c) match {
      case (AxialCoordinate(q, r), East) => AxialCoordinate(q + 1, r)
      case (AxialCoordinate(q, r), SouthEast) => AxialCoordinate(q, r + 1)
      case (AxialCoordinate(q, r), SouthWest) => AxialCoordinate(q - 1, r + 1)
      case (AxialCoordinate(q, r), West) => AxialCoordinate(q - 1, r)
      case (AxialCoordinate(q, r), NorthWest) => AxialCoordinate(q , r - 1)
      case (AxialCoordinate(q, r), NorthEast) => AxialCoordinate(q + 1, r - 1)
      case _ => throw new IllegalArgumentException
    }
  }

  def flipTile(s: String): Unit = {
    val xs = stringToCardinal(s.toList)
    var tile = RootAxialCoordinate
    xs.foreach(c => tile = nextTile(tile, c))
    hexStore.get(tile).fold(hexStore += tile -> Black) {
      case White => hexStore += tile -> Black
      case Black => hexStore += tile -> White
    }
  }

  def flipTiles(xs: List[String]): Unit = xs.foreach(flipTile)
}


val basicFlip = "sesenwnenenewseeswwswswwnenewsewsw"
val basicLobby = new Lobby

basicLobby.flipTile(basicFlip)
basicLobby.hexStore


val testInput: List[String] = fromFile("./test_input").getLines.toList

val testLobby = new Lobby
testLobby.flipTiles(testInput)
println(testLobby.hexStore.values.count(_ == Black))

val input: List[String] = fromFile("./input").getLines.toList

val lobby = new Lobby
lobby.flipTiles(input)
println(lobby.hexStore.values.count(_ == Black))

