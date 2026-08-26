"""
Spot-check the TARGET DOCUMENT's own printed closed form for
D^{*(21)}_r(0) (Sec.3.4 of the ATTEMPT.md, the 'representative
instance' block) against this referee's own ground_truth.D_star,
transcribed by hand from the document's text (coef(r), rem(r) as
printed), evaluated exactly at several concrete r.

D^{*(21)}_r(0) = coef(r) * varphi_r + rem(r)
"""
from fractions import Fraction
import math

from ground_truth import D_star as gt_D_star, varphi_r

# coef(r): list of (power, Fraction) as transcribed from the document
coef_terms = [
    (21, Fraction(67282234305, 1152921504606846976)),
    (20, Fraction(59101699231575, 576460752303423488)),
    (19, Fraction(74857893550250965, 3458764513820540928)),
    (18, Fraction(18222106392424142285, 15564440312192434176)),
    (17, Fraction(80221061678628360589, 5188146770730811392)),
    (16, Fraction(-87654986612590271920819, 1470839609502185029632)),
    (15, Fraction(-2910034888705227821675969, 4902798698340616765440)),
    (14, Fraction(1073957351962682453144939, 210119944214597861376)),
    (13, Fraction(-8666579961263612211340381, 653706493112082235392)),
    (12, Fraction(-528384082314035014618752697, 32358471409048070651904)),
    (11, Fraction(62931426527274494657537489, 280159925619463815168)),
    (10, Fraction(-2297987468004055006611438115, 2941679219004370059264)),
    (9, Fraction(26949293874782913893915777, 17509995351216488448)),
    (8, Fraction(-665153984333173182419966189, 367709902375546257408)),
    (7, Fraction(206087921935183819301653333, 204283279097525698560)),
    (6, Fraction(56511580623452656383022613, 183854951187773128704)),
    (5, Fraction(-1945917227091802380986503, 2188749418902061056)),
    (4, Fraction(612992945919459418495453, 1276770494359535616)),
    (3, Fraction(13246352637939039966527, 531987705983139840)),
    (2, Fraction(-1755807114380064545749, 16255179905040384)),
    (1, Fraction(120286097510180813, 4398046511104)),
]

rem_terms = [
    (20, Fraction(-5, 1572864)),
    (19, Fraction(-37639, 23592960)),
    (18, Fraction(-850069, 5160960)),
    (17, Fraction(-5122076591, 1114767360)),
    (16, Fraction(-10145992332797, 662171811840)),
    (15, Fraction(69516483968077, 220723937280)),
    (14, Fraction(-60343126900871, 78829977600)),
    (13, Fraction(-8744256774746851781, 1641634283520000)),
    (12, Fraction(219160539866070782832469, 4865804016353280000)),
    (11, Fraction(-47362280795819410229, 310418119065600)),
    (10, Fraction(328052681424454692887, 1301017116672000)),
    (9, Fraction(84499808343298394737, 18431075819520000)),
    (8, Fraction(-465981045762588971581, 438835138560000)),
    (7, Fraction(5059812737412590078189, 1843107581952000)),
    (6, Fraction(-59454690145506858403589, 15205637551104000)),
    (5, Fraction(22287585948893468255587, 6335682312960000)),
    (4, Fraction(-1049038073134805937851, 527973526080000)),
    (3, Fraction(2828728705843865537, 4399779384000)),
    (2, Fraction(-39529321243553, 436486050)),
]


def poly_eval_terms(terms, r):
    r = Fraction(r)
    total = Fraction(0)
    for power, c in terms:
        total += c * (r ** power)
    return total


def printed_D21_0(r):
    return poly_eval_terms(coef_terms, r) * varphi_r(r) + poly_eval_terms(rem_terms, r)


if __name__ == "__main__":
    checks = 0
    fails = 0
    for r in [21, 25, 50, 100, 150]:
        got = printed_D21_0(r)
        want = gt_D_star(21, r, 0)
        checks += 1
        status = "OK" if got == want else "MISMATCH"
        print(f"r={r}: printed-formula={'match' if got==want else 'DIFFERS'} [{status}]")
        if got != want:
            fails += 1
            print("  got: ", got)
            print("  want:", want)
    print(f"spotcheck_printed_p21_b0: {checks} checks, {fails} fails")
