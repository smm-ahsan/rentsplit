# Examples

Real output from RentSplit, captured from actual runs.

## Equal split with bills

Command:

```bash
python3 rentsplit.py --rent 900 --bills 90 --people 3
```

Output:

```
Person 1: rent 300.00 + bills 30.00 = 330.00
Person 2: rent 300.00 + bills 30.00 = 330.00
Person 3: rent 300.00 + bills 30.00 = 330.00
Total: 990.00
```

## Weighted split by room size

The bigger room pays weight 2, the smaller room weight 1. No bills given, so bills are 0.

Command:

```bash
python3 rentsplit.py --rent 900 --share "Ahsan:2" --share "Bilal:1"
```

Output:

```
Ahsan: rent 600.00 + bills 0.00 = 600.00
Bilal: rent 300.00 + bills 0.00 = 300.00
Total: 900.00
```

## The awkward-cents case

100 split three ways does not divide cleanly. The extra cent goes to the largest payer (the first person, on a tie) so the parts sum to exactly 100.00.

Command:

```bash
python3 rentsplit.py --rent 100 --people 3
```

Output:

```
Person 1: rent 33.34 + bills 0.00 = 33.34
Person 2: rent 33.33 + bills 0.00 = 33.33
Person 3: rent 33.33 + bills 0.00 = 33.33
Total: 100.00
```
