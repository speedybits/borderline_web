# Turn 21 Victory Analysis

## User Claim
Red should have won on Turn 21 with a connection from row 0 to row 7.

## Analysis Result
**NO VICTORY** - The victory detection is working correctly. There is NO contiguous connection from row 0 to row 7.

## Board State at Turn 21

Red pieces:
- (0, 2): Full piece - rows 0-2, columns 6-8
- (1, 2): Full piece - rows 3-5, columns 6-8
- (2, 2): Full piece - rows 6-8, columns 6-8
- (3, 2): Center column - row 9-11, column 7 (plus row 10 cols 6-8)
- **(4, 1)**: R|_|_ / _|R|R / R|_|_ - rows 12-14, columns 3-5
- (4, 2): Center column - rows 12-14, column 7 (plus row 13 cols 6-8)
- (5, 0): Corner pattern - rows 15-17, columns 0-2
- (5, 2): Vertical line - rows 15-17, column 7
- (6, 1): Full piece - rows 18-20, columns 3-5
- (7, 1): Corner pattern - rows 21-23, columns 3-5

## The Break in Connectivity

### Component 1: Rows 0-17 (42 pips)
This component includes:
- All of pieces (0,2), (1,2), (2,2), (3,2)
- PART of piece (4,1): pips at (13, 4) and (13, 5)
- All of piece (4,2)
- All of piece (5,2)
- ISOLATED pips from pieces (4,1) and (5,0)

### Component 2: Rows 17-21 (12 pips)
This component includes:
- All of piece (6,1)
- All of piece (7,1)
- Some isolated pips from piece (5,0)

### Why They Don't Connect

**The critical gap is between rows 17 and 18:**

- Component 1 reaches as far as row 17, column 7 (from piece 5,2)
- Component 2 starts at row 18, with pips in columns 3-5 (from piece 6,1)

For a connection to exist, we would need:
- A pip at (17, 7) connected to a pip at (18, X) where X is 6, 7, or 8 (orthogonal)
- OR a pip at (17, 6) or (17, 8) connected diagonally to (18, 7) (both must be corners)

**What we actually have:**
- (17, 7) exists (from piece 5,2)
- (18, 3), (18, 4), (18, 5) exist (from piece 6,1)
- NO pip exists at (18, 6), (18, 7), or (18, 8)
- NO diagonal corner connection is possible

Therefore, the two components are **DISCONNECTED**.

## Internal Disconnection in Piece (4,1)

Additionally, piece (4,1) with pattern R|_|_ / _|R|R / R|_|_ is internally disconnected:

```
Row 12: (12, 3) [corner]
Row 13: (13, 4) [center], (13, 5) [not corner]
Row 14: (14, 3) [corner]
```

- (12, 3) cannot connect to (13, 4) because (13, 4) is not a corner (diagonal requires both to be corners)
- (12, 3) cannot connect to (13, 5) because they are not adjacent
- This creates two disconnected parts within the same piece!

## Conclusion

The flood fill algorithm is working CORRECTLY. Red does NOT have a winning connection at Turn 21. The game correctly continued past Turn 21 because no victory condition was met.

The disconnection is caused by:
1. Poor piece placement leaving gaps between rows 17 and 18
2. An internally disconnected piece at position (4,1)
