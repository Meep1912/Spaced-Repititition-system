import numpy as np
import matplotlib.pyplot as plt

# rating per review: 1 = pass, 0 = fail (review 5 fails)
ratings = [1, 1, 1, 1, 0, 1, 1, 1, 1, 1]

ease, interval, repeats = 2.5, 0, 0
t = 0                      # current day
K = 0.105                  # -ln(0.9): retention is 90% when the review is due
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 8))

for n, rating in enumerate(ratings, start=1):
    if rating == 0:
        repeats = 0
        interval = 0
        ease = max(1.3, ease - 0.2)
        ax1.scatter(t, 90, color="red", marker="x", s=100, zorder=5)
        ax1.annotate(f"review {n}: FAIL", (t, 90), textcoords="offset points",
                     xytext=(-10, 12), color="red")
    else:
        if repeats == 0:
            interval = 1
        elif repeats == 1:
            interval = 3
        else:
            interval = round(interval * ease)
        repeats += 1
        ease += 0.05

        S = interval / K                       # stability: bigger interval = flatter curve
        x = np.linspace(t, t + interval, 100)
        ax1.plot(x, 100 * np.exp(-(x - t) / S))
        t += interval

    ax2.scatter(n, ease, color="red" if rating == 0 else "C0")
    ax2.plot(n, ease, color="C0")

ax1.set_xlabel("Days")
ax1.set_ylabel("Retention (%)")
ax1.set_title("Retention with a failure on review 5")
ax1.set_xscale("symlog")

# ease over time
eases, e = [], 2.5
for r in ratings:
    e = max(1.3, e - 0.2) if r == 0 else e + 0.05
    eases.append(e)
ax2.clear()
ax2.plot(range(1, len(ratings) + 1), eases, marker="o")
ax2.axvline(5, color="red", linestyle="--", label="fail")
ax2.set_xlabel("Review number")
ax2.set_ylabel("Ease")
ax2.legend()

plt.tight_layout()
plt.savefig("failure.png", dpi=120)