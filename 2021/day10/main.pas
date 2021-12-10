program Main;

{$mode objfpc}

uses
  Classes, SysUtils, generics.collections;

type
  TCharStack = specialize TStack<Char>;
  TInt64List = specialize TList<Int64>;

var
  Lines: TStringList;

function IllegalCharScore(const c: Char): Integer;
begin
  IllegalCharScore := 0;
  case c of
    ')': IllegalCharScore := 3;
    ']': IllegalCharScore := 57;
    '}': IllegalCharScore := 1197;
    '>': IllegalCharScore := 25137;
  end;
end;

function AutocompleteCharScore(const c: Char): Integer;
begin
  AutocompleteCharScore := 0;
  case c of
    '(': AutocompleteCharScore := 1;
    '[': AutocompleteCharScore := 2;
    '{': AutocompleteCharScore := 3;
    '<': AutocompleteCharScore := 4;
  end;
end;

function ScoreLine(const line: String): Integer;
var
  stack: TCharStack;
  c: Char;
  i: Integer;
begin
  ScoreLine := 0;
  i := 0;
  stack := TCharStack.Create;
  for c in line do begin
    if pos(c, '([{<') > 0 then
      stack.Push(c)
    else
      if ((c = ')') and (stack.Peek <> '(') or
          (c = ']') and (stack.Peek <> '[') or
          (c = '}') and (stack.Peek <> '{') or
          (c = '>') and (stack.Peek <> '<')) then
        exit(IllegalCharScore(c))
      else
        Stack.Pop;
    inc(i);
  end;
end;

function ScoreLines(): LongInt;
var
  line: String;
  sum: LongInt;
begin
  sum := 0;
  for line in Lines do
    sum += ScoreLine(line);
  ScoreLines := sum;
end;

function RepairLine(const line: String): Int64;
var
  stack: TCharStack;
  score: Int64;
  c: Char;
begin
  stack := TCharStack.Create;
  score := 0;

  for c in line do
    if pos(c, '([{<') > 0 then stack.Push(c)
    else stack.Pop;
  
  while (stack.Count > 0) do begin
    score := 5*score  + AutocompleteCharScore(stack.Peek);
    stack.Pop;
  end;

  RepairLine := score;
end;

function RepairLines(): Int64;
var
  scores: TInt64List;
  line: String;
begin
  scores := TInt64List.Create;
  for line in Lines do
    if ScoreLine(line) = 0 then
      scores.Add(RepairLine(line));
  scores.Sort();
  RepairLines := scores.Items[round(scores.Count / 2)];
end;

begin
  Lines := TStringList.Create;
  Lines.LoadFromFile('./input');
  writeln('Answer 1: ' + IntToStr(ScoreLines()));
  writeln('Answer 2: ' + IntToStr(RepairLines()));
  Lines.Free;
end.
