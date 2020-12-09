import scala.collection.mutable
import scala.io.Source._

val instructions: List[String] =
  fromFile("./day8_input")
    .getLines
    .toList

val regex = """(\w+)\s([+-]\d+)""".r

def parseCommand(cmd: String): (String, Int) =
  regex
    .findFirstMatchIn(cmd)
    .map { m => (m.group(1), m.group(2).toInt) }
    .getOrElse(throw new Exception(s"failed to parse $cmd"))

parseCommand("jmp +321")
parseCommand("jmp -32")

class Interpreter(instructions: List[String]) {
  var acc = 0
  var pos = 0 // current position

  val executedPos: mutable.Set[Int] = mutable.Set()

  def run() {
    println("starting execution")
    while (!executedPos.contains(pos)) {
      executedPos.add(pos)
      execute(instructions(pos))
    }
    println(s"about to execute the same pos twice: pos $pos, acc $acc")
  }

  def execute(cmd: String) = {
    println(cmd)
    parseCommand(cmd) match {
      case ("jmp", n) => pos += n
      case ("acc", n) => acc += n; pos += 1
      case ("nop", _) => pos += 1 // noop
      case c => throw new Exception(s"unknown command $c")
    }
  }
}

// test run
new Interpreter("nop +123" :: "acc +10" :: "jmp -2" :: Nil).run()

new Interpreter(instructions).run()

