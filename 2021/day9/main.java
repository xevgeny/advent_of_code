import java.io.IOException;
import java.lang.System;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;

class Main {

    static class Point {
        int _1;
        int _2;

        public Point(int _1, int _2) {
            this._1 = _1;
            this._2 = _2;
        }

        static Point of(int _1, int _2) {
            return new Point(_1, _2);
        }

        @Override
        public boolean equals(Object obj) { // ugh, Java!
            Point point = (Point) obj;
            return this._1 == point._1 && this._2 == point._2;
        }
    }

    static final Point[] neighbours = new Point[]{Point.of(0, -1), Point.of(-1, 0), Point.of(0, 1), Point.of(1, 0)};

    static int[][] readInput(String input) throws IOException {
        List<String> lines = Files.readAllLines(Paths.get(input));
        int N = lines.size();
        int M = lines.get(0).length();
        int[][] arr = new int[N][M];
        for (int n = 0; n < N; n++) {
            for (int m = 0; m < M; m++) {
                char c = lines.get(n).charAt(m);
                arr[n][m] = Integer.parseInt(String.valueOf(c));
            }
        }
        return arr;
    }

    static List<Point> findAllLowestPoints(int[][] input) {
        int N = input.length;
        int M = input[0].length;
        List<Point> lowestPoints = new ArrayList<Point>();
        for (int n = 0; n < N; n++) {
            for (int m = 0; m < M; m++) {
                boolean lowest = true;
                for (Point shift : neighbours)
                    if (n + shift._1 >= 0 && n + shift._1 < N && m + shift._2 >= 0 && m + shift._2 < M)
                        lowest &= input[n][m] < input[n + shift._1][m + shift._2];
                if (lowest) lowestPoints.add(Point.of(n, m));
            }
        }
        return lowestPoints;
    }

    static int sumLowestPoints(int[][] input) {
        return findAllLowestPoints(input)
            .stream()
            .reduce(0, (sum, point) -> sum + input[point._1][point._2] + 1, Integer::sum);
    }

    static int calculateBasinSize(int[][] input, Point point, List<Point> visited) {
        int N = input.length;
        int M = input[0].length;
        visited.add(point);
        for (Point shift : neighbours) {
            Point next = Point.of(point._1 + shift._1, point._2 + shift._2);
            if (next._1 >= 0 && next._1 < N && next._2 >= 0 && next._2 < M)
                if (!visited.contains(next) && input[next._1][next._2] < 9)
                    calculateBasinSize(input, next, visited);
        }
        return visited.size();
    }

    static int top3(int[][] input) {
        return findAllLowestPoints(input)
            .stream()
            .map(lowestPoint -> calculateBasinSize(input, lowestPoint, new ArrayList<>()))
            .sorted(Comparator.reverseOrder())
            .limit(3)
            .reduce(1, (mul, i) -> mul * i);
    }

    public static void main(String[] args) throws IOException {
        int[][] input = readInput("./input");
        System.out.println(sumLowestPoints(input));
        System.out.println(top3(input));
    }
}