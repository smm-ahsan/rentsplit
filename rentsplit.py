#!/usr/bin/env python3
"""RentSplit - split rent and bills fairly between flatmates.

Rent can be split equally or by weight (a bigger room pays more).
Bills (shared utilities) are always split equally per person.
Standard library only.
"""

import argparse
import sys


def parse_share(text, parser):
    """Parse one 'name:weight' share, exiting with code 2 when malformed."""
    name, sep, weight_text = text.rpartition(":")
    name = name.strip()
    if not sep or not name:
        parser.error(
            "bad --share format: %r (expected 'name:weight', e.g. 'Ahsan:2')" % text
        )
    try:
        weight = float(weight_text)
    except ValueError:
        parser.error(
            "bad --share weight: %r (weight must be a number, e.g. 'Ahsan:2')" % text
        )
    if weight <= 0:
        parser.error("bad --share weight: %r (weight must be greater than 0)" % text)
    return name, weight


def main():
    parser = argparse.ArgumentParser(
        description="Split rent and bills fairly between flatmates. "
        "Bills are always split equally; rent is split equally with "
        "--people or by weight with --share."
    )
    parser.add_argument("--rent", type=float, required=True,
                        help="total monthly rent, e.g. 900")
    parser.add_argument("--bills", type=float, default=0.0,
                        help="total shared bills/utilities, split equally (default 0)")
    parser.add_argument("--people", type=int, default=None,
                        help="number of people splitting everything equally")
    parser.add_argument("--share", action="append", default=None,
                        metavar="NAME:WEIGHT",
                        help="one person's weighted share of the rent, e.g. "
                        "'Ahsan:2'; repeat once per person")
    args = parser.parse_args()

    if args.rent <= 0:
        parser.error("--rent must be greater than 0")
    if args.bills < 0:
        parser.error("--bills cannot be negative")

    # Exactly one of --people / --share.
    if (args.people is None) == (args.share is None):
        parser.error("give exactly one of --people or --share")

    if args.people is not None:
        if args.people < 1:
            parser.error("--people must be at least 1")
        names = ["Person %d" % (i + 1) for i in range(args.people)]
        weights = [1.0] * args.people
    else:
        parsed = [parse_share(text, parser) for text in args.share]
        names = [name for name, _ in parsed]
        weights = [weight for _, weight in parsed]

    count = len(names)
    weight_total = sum(weights)
    bills_each = args.bills / count

    # Each person's rent part and bills part, each rounded to 2 decimals;
    # the person's total is the sum of the two rounded parts.
    rent_parts = [round(args.rent * w / weight_total, 2) for w in weights]
    bills_parts = [round(bills_each, 2) for _ in weights]
    totals = [round(r + b, 2) for r, b in zip(rent_parts, bills_parts)]

    # Fix rounding drift on the largest payer (first one on a tie) so the
    # printed parts sum exactly to rent + bills. The drift is applied to
    # that person's rent part too, so every printed line still adds up.
    target = round(args.rent + args.bills, 2)
    drift = round(target - sum(totals), 2)
    if drift != 0:
        idx = max(range(count), key=lambda i: totals[i])
        rent_parts[idx] = round(rent_parts[idx] + drift, 2)
        totals[idx] = round(totals[idx] + drift, 2)

    for name, rent_part, bills_part, total in zip(names, rent_parts, bills_parts, totals):
        print("%s: rent %.2f + bills %.2f = %.2f" % (name, rent_part, bills_part, total))
    print("Total: %.2f" % target)
    return 0


if __name__ == "__main__":
    sys.exit(main())
