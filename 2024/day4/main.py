def count_xmas(xs, i, j):
  xmas, count = list("XMAS"), 0
  q = [(0,i,j,1,0), (0,i,j,-1,0), (0,i,j,0,1), (0,i,j,0,-1), (0,i,j,1,1), (0,i,j,-1,-1), (0,i,j,1,-1), (0,i,j,-1,1)]
  while q:
    s,i,j,ii,jj = q.pop(0)
    if 0 <= i < len(xs) and 0 <= j < len(xs[0]):
      if xs[i][j] == xmas[s]:
        if s == len(xmas)-1:
          count += 1
        else:
          q.append((s+1,i+ii,j+jj,ii,jj))
  return count

def count_x_mas(xs, i, j):
  if xs[i][j] == "A": 
    xmas = "".join([xs[i-1][j-1], xs[i-1][j+1], xs[i+1][j-1], xs[i+1][j+1]])
    return int(xmas in ["MMSS", "SSMM", "MSMS", "SMSM"])
  return 0

with open("input") as f:
  xs = [list(line.strip()) for line in f.readlines()]
  print(f"Part 1: {sum(count_xmas(xs, i, j) for i in range(len(xs)) for j in range(len(xs[0])))}")
  print(f"Part 2: {sum(count_x_mas(xs, i, j) for i in range(1, len(xs)-1) for j in range(1, len(xs[0])-1))}")
