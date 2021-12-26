import scala.io.Source._
import scala.collection.mutable
import java.lang.Exception


class ALU: // this is optional
  var state = mutable.HashMap[String, Long]("w" -> 0L, "x" -> 0L, "y" -> 0L, "z" -> 0L)

  var input = 0L
  val names = Set("w", "x", "y", "z")

  def parse(v: String): Long =
    if names.contains(v) then state(v) else v.toLong

  def execute(cmd: String) =
    cmd.split(" ").toList match
      case "inp" :: reg :: Nil => state(reg) = input
      case "add" :: reg :: v :: Nil => state(reg) += parse(v)
      case "mul" :: reg :: v :: Nil => state(reg) *= parse(v)
      case "div" :: reg :: v :: Nil => state(reg) /= parse(v)
      case "mod" :: reg :: v :: Nil => state(reg) %= parse(v)
      case "eql" :: reg :: v :: Nil => state(reg) = if state(reg) == parse(v) then 1 else 0
      case _ => throw new Exception(s"unknown command '$cmd'")

end ALU


object Sim: // simulates ALU, see sim.png
  val alpha = List(13, 11, 12, 10, 14, -1, 14, -16, -8, 12, -16, -13, -6, -6)
  val beta = List(6, 11, 5, 6, 8, 14, 9, 4, 7, 13, 11, 11, 6, 1)
  val divz1 = Set(0, 1, 2, 3, 4, 6, 9)

  def cond(z: Long, index: Int, input: Int): Boolean = 
    z % 26 + alpha(index) == input

  def execute(z: Long, index: Int, input: Int): (Int, Long) =
    if cond(z, index, input) then
      if divz1.contains(index) then
        (input, z)
      else
        (input, z/26)
    else
      if divz1.contains(index) then
        (input, 26*z + input + beta(index))
      else
        (input, 26*(z/26) + input + beta(index))

end Sim


def backtrackMax(zstate: mutable.Stack[(Int, Long)]): Unit =
  val (digit, _) = zstate.pop
  val z = if zstate.isEmpty then 0L else zstate.head._2
  val idx = zstate.length
  if Sim.divz1.contains(idx) then
    if digit > 1 then
      zstate.push(Sim.execute(z, idx, digit-1))
      return
  else
    var d = digit-1
    while (!Sim.cond(z, idx, d) && d >= 1) do d -= 1 
    if d >= 1 then
      zstate.push(Sim.execute(z, idx, d))
      return
  backtrackMax(zstate)


def backtrackMin(zstate: mutable.Stack[(Int, Long)]): Unit =
  val (digit, _) = zstate.pop
  val z = if zstate.isEmpty then 0L else zstate.head._2
  val idx = zstate.length
  if Sim.divz1.contains(idx) then
    if digit < 9 then
      zstate.push(Sim.execute(z, idx, digit+1))
      return
  else
    var d = digit+1
    while (!Sim.cond(z, idx, d) && d <= 9) do d += 1 
    if d <= 9 then
      zstate.push(Sim.execute(z, idx, d))
      return
  backtrackMin(zstate)


def findNumber(digit: Int, backtrackFn: mutable.Stack[(Int, Long)] => Unit): Option[String] =
  val zstate = mutable.Stack[(Int, Long)]()

  while true do // DFS
    if zstate.length < 14 then
      val z = if zstate.isEmpty then 0L else zstate.head._2
      val idx = zstate.length
      zstate.push(Sim.execute(z, idx, digit))
      if !Sim.divz1.contains(idx) && !Sim.cond(z, idx, digit) then
        backtrackFn(zstate)
    else
      if zstate.head._2 == 0L then
        return Some(zstate.toList.reverse.map(_._1).mkString)
      else
        backtrackFn(zstate)

  None
end findNumber


// verify number in real ALU
def runInALU(commands: List[String], num: String): Long =
  val blocks = commands.grouped(18).toList
  val digits  = mutable.Queue(num.map(_.asDigit): _*)

  val alu = new ALU
  for block <- blocks do
    alu.input = digits.dequeue
    block.foreach(alu.execute)

  alu.state("z")
end runInALU


@main def main =
  val commands = fromFile("./input").getLines.toList

  val max = findNumber(9, backtrackMax).get
  assert(runInALU(commands, max) == 0L)
  println(s"Answer 1: $max")

  val min = findNumber(1, backtrackMin).get
  assert(runInALU(commands, min) == 0L)
  println(s"Answer 2: $min")
