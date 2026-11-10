# RentSplit

Split rent and bills fairly between flatmates: rent equally or weighted by room, bills always shared equally.

## When weighted shares help

Flatmates rarely have identical rooms. One person gets the big double room with the balcony, another gets the small single at the back — charging both the same rent does not feel fair. With `--share` you give each person a weight for the rent: the bigger room might pay weight 2 while the smaller room pays weight 1, so the big room costs double. Bills like electricity, water and internet are still split equally per person, because everyone uses them much the same.

## Requirements

- Python 3
- Standard library only — nothing to install

## Usage

Split a €900 rent and €90 of bills equally between 3 people:

```bash
python3 rentsplit.py --rent 900 --bills 90 --people 3
```

Split rent by room size with weights (bills would still be equal):

```bash
python3 rentsplit.py --rent 900 --share "Ahsan:2" --share "Bilal:1"
```

Handle the awkward cents so the parts sum exactly to the rent:

```bash
python3 rentsplit.py --rent 100 --people 3
```

Each person's total is rounded to 2 decimals; if rounding leaves the parts a cent or two short of the real total, the difference is added to the largest payer so the printed parts always sum exactly to the printed total.

See `examples.md` for real captured output.

## License

MIT — see `LICENSE`.
