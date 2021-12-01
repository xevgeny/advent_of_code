import scala.collection.mutable
import scala.collection.mutable.ListBuffer
import scala.io.Source._

val instructions: List[String] =
  fromFile("./input")
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
  var pos = 0 // current line

  val executionLog: mutable.ListBuffer[(Int, String)] = new ListBuffer()

  def posAlreadyExecuted(): Boolean = executionLog.map(_._1).contains(pos)

  // returns execution status
  // status 0 - success
  // status 1 - duplicated pos
  def run(): (Int, List[(Int, String)]) = {
    // println("start")
    while (!posAlreadyExecuted() && pos != instructions.size) {
      execute(instructions(pos))
    }
    if (posAlreadyExecuted()) {
      // println(s"about to execute the same line twice: pos $pos, acc $acc")
      return (1, executionLog.toList)
    }
    println(s"end: acc $acc")
    (0, executionLog.toList)
  }

  def execute(cmd: String) = {
    executionLog.addOne((pos, cmd))
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

// part 1

val executionLog = new Interpreter(instructions).run()

// part 2

// Let's find executed instructions that are close to the end of instruction file
executionLog._2.takeRight(10)

// List((600,acc -2), (601,acc +50), (602,nop -337), (603,jmp -252), (611,jmp -45),
//      (621,acc -11), (622,acc +30), (623,nop -572), (624,acc +21), (625,jmp -235))

// modify last jmp -235 to nop -235 at line 625+1=626, doesn't work x_x
// ok we can still brute force the solution

import scala.util.control.Breaks._

for (i <- 0 until instructions.length) {
  parseCommand(instructions(i)) match {
    case ("jmp", n) =>
      val s = if (n >= 0) s"+$n" else s"$n"
      val res = new Interpreter(instructions.updated(i, s"nop $s")).run()
      if (res._1 == 0) {
        println(s"You need to replace pos ${i+1} to nop $s")
        break
      }
    case _ =>
  }
}

// end: acc 631
// You need to replace pos 430 to nop +93