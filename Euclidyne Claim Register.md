# Euclidyne Claim Register

This note records how `Euclidorithm QA.md` was filtered into the current Euclidyne direction.

## Verified

| Claim | Confidence | Notes | Sources |
|---|---:|---|---|
| The Euclidean algorithm on positive integers yields the finite continued fraction of `a / b`. | High | Core mathematical spine of the app. | Bell; Euclid Book VII |
| Extended Euclid produces coefficients `x` and `y` with `a*x + b*y = gcd(a, b)`. | High | Safe for explorer, calculator, and identity views. | Bell |
| If `gcd(a, b) = 1`, the `x` coefficient gives the inverse of `a mod b`. | High | Safe for modular-inverse demonstrations. | Bell |
| Rectangle-to-squares dissection follows the same quotient sequence as the Euclidean algorithm. | High | Safe for geometry and continued-fraction visualizations. | Bell |
| The logarithmic-spiral story belongs to the special golden-rectangle case, not to every Euclidean rectangle dissection. | High | Keep the golden special case, not a generic spiral claim. | Mathematical Gazette article |

## Analogy Only

| Claim | Confidence | Notes | Sources |
|---|---:|---|---|
| One Euclidean division step can be visualized as `q` full turns plus residual phase `r / b`. | Medium-High | Good as a one-step animation if clearly labeled as analogy rather than autonomous computation. | Bell; Cambridge gear meshing |
| The current "Phase Lab" style story is a one-step cycle analogy, not a complete mechanical Euclid machine. | High | This is an app-labeling decision, not a theorem claim. | Bell; Cambridge gear meshing |
| Automatic compound-gear or sliding-gear Euclid machines. | Medium (~65%) | I could not find an authoritative description of a specific compound-gear or sliding-gear mechanism that automatically performs Euclid's quotient/remainder steps as an exact algorithm for arbitrary inputs. What is well supported is that ordinary gear trains realize fixed rational speed ratios determined by geometry and tooth counts, and that continued fractions are used as design-time ratio tools. As a result, "gears as Euclid machine" is supportable only as a conceptual analogy unless sensing, control, and reconfiguration are added beyond a simple train. | Cambridge gear meshing |

## False

| Claim | Confidence | Reasoning | Sources |
|---|---:|---|---|
| Claims that a sliding center shift equals the integer remainder exactly. | High (~90%) | For involute gears, varying center distance within operating limits preserves conjugate action and leaves the speed ratio unchanged. Center-distance changes mainly affect pressure angle and contact conditions, not a discrete integer remainder. | Cambridge gear meshing |
| Generic inward-spiral or logarithmic-spiral claims for gear or rectangle models. | High (~93%) | The "golden spiral" is a logarithmic spiral tied to the self-similarity of the golden rectangle subdivision. That self-similarity is not generic to arbitrary rectangles or Euclidean tilings. | Springer chapter on the golden spiral |
| Historical claims that compound gear trains themselves implemented Euclid as an exact mechanical algorithm. | Medium-High (~80%) | The supported historical direction is the reverse: continued fractions and Euclid-style reduction help choose useful rational gear ratios, and compound trains then realize those fixed ratios. A fixed compound train does not by itself execute Euclid's iterative quotient/remainder procedure for arbitrary inputs. | GlobalSpec continued-fractions gear-ratio reference |

## Core Sources

- Jordan Bell, "The Euclidean algorithm and finite continued fractions"
  - https://jordanbell.info/LaTeX/euclideanalgorithm/euclideanalgorithm.pdf
- Clark University, "Euclid's Elements, Book VII"
  - http://aleph0.clarku.edu/~djoyce/elements/bookVII/bookVII.html
- Cambridge DANotes, "Gear Meshing"
  - https://www-mdp.eng.cam.ac.uk/web/library/enginfo/textbooks_dvd_only/DAN/gears/meshing/meshing.html
- The Mathematical Gazette, "Golden rectangles and the logarithmic spiral"
  - https://www.cambridge.org/core/services/aop-cambridge-core/content/view/8B3A00A26C1E9FF5CB8A4D9340D87EBD/S0008439500004603a.pdf/div-classtitleGolden-rectangles-and-the-logarithmic-spiraldiv.pdf
- G. S. Chirikjian, "The Golden Spiral"
  - https://link.springer.com/chapter/10.1007/978-3-662-68931-8_8
- GlobalSpec, "Graphical method of using continued fractions to find the best gear ratio"
  - https://www.globalspec.com/reference/68680/203279/graphical-method-of-using-continued-fractions-to-find-the-best-gear-ratio
