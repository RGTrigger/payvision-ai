import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from main import forecast_transactions

OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

def adoption_heatmap():
    _, _, _, years, upi, cash = forecast_transactions()

    data = np.vstack([upi, cash])

    plt.figure(figsize=(12,4))
    plt.imshow(data, aspect='auto', cmap="plasma")
    plt.colorbar(label="Transaction Intensity")

    plt.yticks([0,1], ["UPI","Cash"])
    plt.xticks(
        np.linspace(0, len(years)-1, 6),
        [str(int(y)) for y in np.linspace(years[0], years[-1], 6)]
    )

    plt.title("Digital Adoption Intensity Heatmap")

    plt.savefig(OUTPUT_DIR / "heatmap.png", dpi=300, bbox_inches="tight")
    plt.show()
