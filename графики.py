{
 "cells": [
  {
   "cell_type": "markdown",
   "id": "557e4567-4ec8-4e89-8bf5-474553623163",
   "metadata": {},
   "source": [
    "## Задание №1"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "80e59509-cf1e-4788-bc71-5702ad930a9d",
   "metadata": {},
   "source": [
    "1. Задать отрезок точками 𝑃1\n",
    " и 𝑃2\n",
    " с радиус векторами 𝐩1\n",
    " и 𝐩2\n",
    ". Отобразить на рисунке точки\n",
    "и их обозначения"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "5c41127b-e1c3-4dc3-8774-e0beb554ec2f",
   "metadata": {},
   "outputs": [],
   "source": [
    "import numpy as np\n",
    "import matplotlib.pyplot as plt\n",
    "import matplotlib.patches as mpatches\n",
    "from ipywidgets import interact\n",
    "import ipywidgets as widgets\n",
    "from matplotlib.patches import Circle\n",
    "import matplotlib.patches as patches\n",
    "from matplotlib.animation import FuncAnimation\n",
    "from IPython.display import HTML"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "id": "457ca8c5-d018-477d-bf11-fc4376b625c1",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "iVBORw0KGgoAAAANSUhEUgAAAjUAAAGdCAYAAADqsoKGAAAAQHRFWHRTb2Z0d2FyZQBNYXRwbG90bGliIHZlcnNpb24zLjEwLjErZGZzZzEsIGh0dHBzOi8vbWF0cGxvdGxpYi5vcmcvzRIYmAAAAAlwSFlzAAAPYQAAD2EBqD+naQAAIgpJREFUeJzt3XtwVPX9//HXkjudZAUCCZGEgLUSRSgkiiRQZQpBwFSkI2ABYazMNxYKSapfEoSR4pfEglDahotBUmq9gMOtWLFDvBBAYgMxoQgUyhBIvkgmhkKWi+Z6fn/wY79uA5iFkE0++3zM7Iz7yTmb97rOOU/3FptlWZYAAADauQ6eHgAAAKAlEDUAAMAIRA0AADACUQMAAIxA1AAAACMQNQAAwAhEDQAAMAJRAwAAjODr6QFaSmNjo7788ksFBwfLZrN5ehwAANAMlmXpwoULioiIUIcOt/ZcizFR8+WXXyoyMtLTYwAAgJtQXl6uHj163NJtGBM1wcHBkq78SwkJCfHwNAAAoDkcDociIyOd5/FbYUzUXH3JKSQkhKgBAKCdaYm3jvBGYQAAYASiBgAAGIGoAQAARiBqAACAEYgaAABgBKIGAAAYgagBAABGIGoAAIARiBoAAGAEogYAABiBqAEAAEYgagAAgBGIGgAAYASiBgAAGIGoAQAARiBqAACAEYgaAABgBKIGAAAYgagBAABGIGoAAIARiBoAAGAEogYAABiBqAEAAEYgagAAgBGIGgAAYASiBgAAGIGoAQAARiBqAACAEYgaAABgBKIGAAAYgagBAABGIGoAAIARiBoAAGAEogYAABiBqAEAAEYgagAAgBGIGgAAYASiBgAAGIGoAQAARiBqAACAEYgaAABgBKIGAAAYgagBAABGcDtqdu3apaSkJEVERMhms2nr1q3fuU9+fr5iY2MVGBio3r17a/Xq1dfddv369bLZbBo7dqy7owEAAC/mdtRcunRJ/fv3V3Z2drO2Ly0t1ejRozV06FAVFxdr7ty5mjVrljZt2tRk21OnTun555/X0KFD3R0LAAB4OV93dxg1apRGjRrV7O1Xr16tqKgoLV++XJIUExOj/fv369VXX9VPf/pT53YNDQ2aNGmSfv3rX2v37t06f/68u6MBAAAvdtvfU1NQUKDExESXtZEjR2r//v2qq6tzri1cuFBdu3bVz3/+82bdbk1NjRwOh8sFAAB4r9seNRUVFQoLC3NZCwsLU319vaqqqiRJn376qdauXas1a9Y0+3azsrJkt9udl8jIyBadGwAAtC+t8uknm83mct2yLOf6hQsXNHnyZK1Zs0ahoaHNvs2MjAxVV1c7L+Xl5S06MwAAaF/cfk+Nu8LDw1VRUeGyVllZKV9fX3Xp0kWHDh3SyZMnlZSU5Px5Y2PjleF8fXX06FHdddddTW43ICBAAQEBt3d4AADQbtz2qBk8eLDee+89l7UdO3YoLi5Ofn5+6tOnjw4ePOjy83nz5unChQv63e9+x8tKAACgWdyOmosXL+r48ePO66WlpSopKVHnzp0VFRWljIwMnT59Wm+88YYkKTk5WdnZ2UpLS9P06dNVUFCgtWvX6p133pEkBQYGqm/fvi6/44477pCkJusAAADX43bU7N+/X8OGDXNeT0tLkyRNnTpV69at05kzZ1RWVub8ea9evbR9+3alpqZqxYoVioiI0O9//3uXj3MDAADcKpt19V277ZzD4ZDdbld1dbVCQkI8PQ4AAGiGljx/87efAACAEYgaAABgBKIGAAAYgagBAABGIGoAAIARiBoAAGAEogYAABiBqAEAAEYgagAAgBGIGgAAYASiBgAAGIGoAQAARiBqAACAEYgaAABgBKIGAAAYgagBAABGIGoAAIARiBoAAGAEogYAABiBqAEAAEYgagAAgBGIGgAAYASiBgAAGIGoAQAARiBqAACAEYgaAABgBKIGAAAYgagBAABGIGoAAIARiBoAAGAEogYAABiBqAEAAEYgagAAgBGIGgAAYASiBgAAGIGoAQAARiBqAACAEYgaAABgBKIGAAAYgagBAABGIGoAAIARiBoAAGAEogYAABiBqAEAAEYgagAAgBGIGgAAYASiBgAAGIGoAQAARiBqAACAEYgaAABgBKIGAAAYgagBAABGIGoAAIARiBoAAGAEogYAABiBqAEAAEZwO2p27dqlpKQkRUREyGazaevWrd+5T35+vmJjYxUYGKjevXtr9erVLj9fs2aNhg4dqk6dOqlTp04aPny4CgsL3R0NAAB4Mbej5tKlS+rfv7+ys7ObtX1paalGjx6toUOHqri4WHPnztWsWbO0adMm5zY7d+7UU089pU8++UQFBQWKiopSYmKiTp8+7e54AADAS9ksy7JuemebTVu2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AABGIGoAAIARiBoAAGAEogYAABiBqAEAAEYgagAAgBGIGgAAYASiBgAAGIGoAQAARiBqAACAEYgaAABgBKIGAAAYgagBAABGIGoAAIARiBoAAGAEogYAABiBqAEAAEYgagAAgBGIGgAAYASiBgAAGIGoAQAARiBqAACAEYgaAABgBKIGAAAYgagBAABGIGoAAIARiBoAAGAEogYAABiBqAEAAEYgagAAgBGIGgAAYASiBgAAGOGmomblypXq1auXAgMDFRsbq927d99w+xUrVigmJkZBQUG655579MYbbzTZZvny5brnnnsUFBSkyMhIpaam6ptvvrmZ8QAAgBfydXeHDRs2KCUlRStXrlRCQoJee+01jRo1SocPH1ZUVFST7VetWqWMjAytWbNGDzzwgAoLCzV9+nR16tRJSUlJkqS33npL6enpys3NVXx8vI4dO6Zp06ZJkn7729/e2j0EAABewWZZluXODoMGDdLAgQO1atUq51pMTIzGjh2rrKysJtvHx8crISFBS5Ysca6lpKRo//792rNnjyRp5syZOnLkiD766CPnNr/61a9UWFj4nc8CXeVwOGS321VdXa2QkBB37hIAAPCQljx/u/XyU21trYqKipSYmOiynpiYqL17915zn5qaGgUGBrqsBQUFqbCwUHV1dZKkIUOGqKioSIWFhZKkEydOaPv27RozZow74wEAAC/m1stPVVVVamhoUFhYmMt6WFiYKioqrrnPyJEj9frrr2vs2LEaOHCgioqKlJubq7q6OlVVVal79+6aOHGivvrqKw0ZMkSWZam+vl7PPfec0tPTrztLTU2NampqnNcdDoc7dwUAABjmpt4obLPZXK5bltVk7ar58+dr1KhReuihh+Tn56fHH3/c+X4ZHx8fSdLOnTu1aNEirVy5Up9//rk2b96sv/71r3r55ZevO0NWVpbsdrvzEhkZeTN3BQAAGMKtqAkNDZWPj0+TZ2UqKyubPHtzVVBQkHJzc3X58mWdPHlSZWVlio6OVnBwsEJDQyVdCZ8pU6bo2Wef1f33368nnnhCmZmZysrKUmNj4zVvNyMjQ9XV1c5LeXm5O3cFAAAYxq2o8ff3V2xsrPLy8lzW8/LyFB8ff8N9/fz81KNHD/n4+Gj9+vV67LHH1KHDlV9/+fJl5z9f5ePjI8uydL33MQcEBCgkJMTlAgAAvJfb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",
      "text/plain": [
       "<Figure size 640x480 with 1 Axes>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "x=[2, 8]\n",
    "y=[1, 1]\n",
    "plt.plot(x, y, marker='o', linestyle='-', color='black')\n",
    "labels=['p1', 'p2']\n",
    "plt.scatter(x, y)\n",
    "for i in range(len(labels)):\n",
    "    plt.text(x[i]+0.005, y[i]+0.005,labels[i], fontsize=12)\n",
    "plt.xlim(0, 10)\n",
    "#plt.grid(True)\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "6cee2435-05fa-4109-9405-c4dfcd849196",
   "metadata": {},
   "source": [
    "2. С помощью формулы для 𝐩(𝑡) = 𝐩1(1 − 𝑡) + 𝐩2\n",
    "𝑡 отобразить точку, расположенную в середине отрезка"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "id": "73b4dfd6-7b5d-4e84-9235-b1ddf4ed2d80",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "iVBORw0KGgoAAAANSUhEUgAAAjUAAAGdCAYAAADqsoKGAAAAQHRFWHRTb2Z0d2FyZQBNYXRwbG90bGliIHZlcnNpb24zLjEwLjErZGZzZzEsIGh0dHBzOi8vbWF0cGxvdGxpYi5vcmcvzRIYmAAAAAlwSFlzAAAPYQAAD2EBqD+naQAAI51JREFUeJzt3XtU1HX+x/HXCAi4BybzwkVAtG1LM12FMlFSziqmxWZtqaWmvzbPobVVYdujlJ7c9gitpmu7eEmTdTuV2RF0bZf2SBdRkxY1dA1dXX+iEMkxXGO8FML4/f3Bj9km1BhFBj7zfJwzp+Yz3xne03Dm++w7F2yWZVkCAABo5zp4ewAAAICWQNQAAAAjEDUAAMAIRA0AADACUQMAAIxA1AAAACMQNQAAwAhEDQAAMIK/twdoKZcuXdIXX3yhkJAQ2Ww2b48DAACawbIsnT17VpGRkerQ4fqOtRgTNV988YWio6O9PQYAALgGFRUVioqKuq7bMCZqQkJCJDX8RwkNDfXyNAAAoDkcDoeio6Nd+/HrYUzUNL7kFBoaStQAANDOtMRbR3ijMAAAMAJRAwAAjEDUAAAAIxA1AADACEQNAAAwAlEDAACMQNQAAAAjEDUAAMAIRA0AADACUQMAAIxA1AAAACMQNQAAwAhEDQAAMAJRAwAAjEDUAAAAIxA1AADACEQNAAAwAlEDAACMQNQAAAAjEDUAAMAIRA0AADACUQMAAIxA1AAAACMQNQAAwAhEDQAAMAJRAwAAjEDUAAAAIxA1AADACEQNAAAwAlEDAACMQNQAAAAjEDUAAMAIRA0AADACUQMAAIxA1AAAACMQNQAAwAhEDQAAMAJRAwAAjEDUAAAAIxA1AADACEQNAAAwAlEDAACMQNQAAAAjeBw127dvV0pKiiIjI2Wz2bR58+bvvU5hYaHi4uIUFBSk3r17a9WqVVfc9u2335bNZtO4ceM8HQ0AAPgwj6Pm/PnzGjBggLKzs5u1fVlZmcaOHavExESVlJToueee08yZM5Wbm9tk2xMnTujZZ59VYmKip2MBAAAf5+/pFcaMGaMxY8Y0e/tVq1YpJiZGy5YtkyT16dNHe/bs0csvv6yf/exnru2cTqcmTZqk3/zmN9qxY4e++uorT0cDAAA+7Ia/p6aoqEjJyclua6NHj9aePXtUV1fnWnvxxRfVrVs3/fznP2/W7dbW1srhcLidAACA77rhUVNVVaWwsDC3tbCwMNXX16u6ulqS9PHHH2vt2rVas2ZNs283KytLdrvddYqOjm7RuQEAQPvSKp9+stlsbucty3Ktnz17VpMnT9aaNWvUtWvXZt9mRkaGampqXKeKiooWnRkAALQvHr+nxlPh4eGqqqpyWzt16pT8/f3VpUsXlZaW6vjx40pJSXFdfunSpYbh/P11+PBh3XLLLU1uNzAwUIGBgTd2eAAA0G7c8KgZMmSI3n33Xbe1rVu3Kj4+XgEBAbr99tt14MABt8vnzZuns2fP6pVXXuFlJQAA0CweR825c+d09OhR1/mysjLt27dPN998s2JiYpSRkaHKykq9/vrrkqTU1FRlZ2crPT1d06dPV1FRkdauXav169dLkoKCgtSvXz+3n3HTTTdJUpN1AACAK/E4avbs2aOkpCTX+fT0dEnS1KlTtW7dOp08eVLl5eWuy3v16qX8/HylpaVp+fLlioyM1B/+8Ae3j3MDAABcL5vV+K7dds7hcMhut6umpkahoaHeHgcAADRDS+6/+dtPAADACEQNAAAwAlEDAACMQNQAAAAjEDUAAMAIRA0AADACUQMAAIxA1AAAACMQNQAAwAhEDQAAMAJRAwAAjEDUAAAAIxA1AADACEQNAAAwAlEDAACMQNQAAAAjEDUAAMAIRA0AADACUQMAAIxA1AAAACMQNQAAwAhEDQAAMAJRAwAAjEDUAAAAIxA1AADACEQNAAAwAlEDAACMQNQAAAAjEDUAAMAIRA0AADACUQMAAIxA1AAAACMQNQAAwAhEDQAAMAJRAwAAjEDUAAAAIxA1AADACEQNAAAwAlEDAACMQNQAAAAjEDUAAMAIRA0AADACUQMAAIxA1AAAACMQNQAAwAhEDQAAMAJRAwAAjEDUAAAAIxA1AADACEQNAAAwAlEDAACMQNQAAAAjEDUAAMAIRA0AADACUQMAAIxA1AAAACN4HDXbt29XSkqKIiMjZbPZtHnz5u+9TmFhoeLi4hQUFKTevXtr1apVbpevWbNGiYmJ6ty5szp37qyRI0equLjY09EAAIAP8zhqzp8/rwEDBig7O7tZ25eVlWns2LFKTExUSUmJnnvuOc2cOVO5ubmubbZt26bHHntMH330kYqKihQTE6Pk5GRVVlZ6Oh4AAPBRNsuyrGu+ss2mTZs2ady4cVfcZs6cOdqyZYsOHTrkWktNTdX+/ftVVFR02es4nU517txZ2dnZeuKJJ5o1i8PhkN1uV01NjUJDQz26HwAAwDtacv99w99TU1RUpOTkZLe10aNHa8+ePaqrq7vsdS5cuKC6ujrdfPPNV7zd2tpaORwOtxMAAPBdNzxqqqqqFBYW5rYWFham+vp6VVdXX/Y6c+fOVY8ePTRy5Mgr3m5WVpbsdrvrFB0d3aJzAwCA9qVVPv1ks9nczje+4vXddUlatGiR1q9fr7y8PAUFBV3xNjMyMlRTU+M6VVRUtOzQAACgXfG/0T8gPDxcVVVVbmunTp2Sv7+/unTp4rb+8ssvKzMzU++//7769+9/1dsNDAxUYGBgi88LAADapxt+pGbIkCEqKChwW9u6davi4+MVEBDgWlu8eLF++9vf6u9//7vi4+Nv9FgAAMAwHkfNuXPntG/fPu3bt09Sw0e29+3bp/LyckkNLwt9+xNLqampOnHihNLT03Xo0CHl5ORo7dq1evbZZ13bLFq0SPPmzVNOTo5iY2NVVVWlqqoqnTt37jrvHgAA8BUef6R727ZtSkpKarI+depUrVu3TtOmTdPx48e1bds212WFhYVKS0tTaWmpIiMjNWfOHKWmprouj42N1YkTJ5rc5gsvvKAFCxY0ay4+0g0AQPvTkvvv6/qemraEqAEAoP1pV99TAwAA0BqIGgAAYASiBgAAGIGoAQAARiBqAACAEYgaAABgBKIGAAAYgagBAABGIGoAAIARiBoAAGAEogYAABiBqAEAAEYgagAAgBGIGgAAYASiBgAAGIGoAQAARiBqAACAEYgaAABgBKIGAAAYgagBAABGIGoAAIARiBoAAGAEogYAABiBqAEAAEYgagAAgBGIGgAAYASiBgAAGIGoAQAARiBqAACAEYgaAABgBKIGAAAYgagBAABGIGrQJuzcuVNPPfWU4uLiFBgYKJvNpuPHj3t7LLRF69ZJNlvDadu2ppdblvTDHzZcPmJEKw8HEzmdTi1dulT33XefoqKi1KlTJ/Xp00dz587VV1995e3x8C1EDdqEDz74QO+//75iYmKUkJDg7XHQHoSESGvXNl0vLJT+938bLgdawNdff60FCxaoZ8+eWrZsmfLz8zV9+nStXr1aQ4cO1ddff+3tEfH//L09ACBJ8+fP1wsvvCBJevnll7Xtcv8HDnzbhAnSm29Ky5dLoaH/XV+7VhoyRHI4vDcbjBIcHKyysjJ16dLFtTZixAjFxMTo0UcfVW5uriZPnuzFCdGIIzW4oRYsWCCbzaaSkhI9/PDDCg0Nld1u1+TJk/Xll1+6tuvQgV9FeOixxxr+uX79f9dqaqTcXOnJJ70zE9qd5jxH+fn5uQVNo7vvvluSVFFR0aoz48rYk6BVPPTQQ/rhD3+ojRs3asGCBdq8ebNGjx6turo6b4+G9io0VHrkESkn579r69dLHTo0HMUBPHAtz1EffvihJOmOO+5orTHxPXj5Ca3i4Ycf1qJFiyRJycnJCgsL06RJk/TOO+9o0qRJXp4O7daTT0pJSVJpqXTHHQ2B8+ijvJ8GHvP0OaqyslJz585VfHy8HnjggdYeF1fAkRq0iu8+KYwfP17+/v766KOPvDQRjDB8uHTLLQ0xc+CAtHs3Lz3hmnjyHPWf//xHY8eOlWVZ2rBhAy+ftyEcqUGrCA8Pdzvv7++vLl266PTp016aCEaw2aT/+R/pD3+QvvlG+tGPpMREb0+Fdqi5z1FnzpzRqFGjVFlZqQ8//FC9e/duzTHxPchLtIqqqiq38/X19Tp9+vRl33wHeGTaNKm6Wlq1qiFwgGvQnOeoM2fOaOTIkSorK1NBQYH69+/f2mPiexA1aBVvvvmm2/l33nlH9fX1GsGXo+F69egh/frXUkqKNHWqt6dBO/V9z1GNQXPs2DFt3bpVAwcO9MKU+D68/IRWkZeXJ39/f40aNUqlpaWaP3++BgwYoPHjx0uSvvzySxUWFkqSDhw4IEl677331K1bN3Xr1k3Dhw/32uxoB156ydsToJ272nPU119/rdGjR6ukpETLli1TfX29PvnkE9d1u3XrpltuucWL06MRUYNWkZeXpwULFmjlypWy2WxKSUnRsmXL1LFjR0lSaWmpHn30Ubfr/OIXv5AkDR8+nC/jA3BDXe056vjx49q9e7ckadasWU2uO3XqVK1bt66VJ8blEDVoFTExMdqyZcsVLx8xYoQsy2rFidBuTZvWcPo+n312oyeBQa72HBUbG8vzUzvBe2oAAIARiBoAAGAEm2XIMTWHwyG73a6amhqFfvuP2wEAgDarJfffHKkBAABGIGoAAIARiBoAAGAEogYAABiBqAEAAEYgagAAgBGIGgAAYAT+TAJalNPp1I4dO3Ty5ElFREQoMTFRfn5+3h4L7ZnTKe3YIZ08KUVESImJEr9TuA48T5nL4yM127dvV0pKiiIjI2Wz2bR58+bvvU5hYaHi4uIUFBSk3r17a9WqVU22yc3NVd++fRUYGKi+fftq06ZNno4GL8vLy1NsbKySkpL0+OOPKykpSbGxscrLy/P2aGiv8vKk2FgpKUl6/PGGf8bGNqwD14DnKbN5HDXnz5/XgAEDlJ2d3azty8rKNHbsWCUmJqqkpETPPfecZs6cqdzcXNc2RUVFmjBhgqZMmaL9+/drypQpGj9+vP7xj394Oh68JC8vT4888og+//xzt/XKyko98sgjPGHAc3l50iOPSN/5nVJlZcM6v1PwEM9T5ruuP5Ngs9m0adMmjRs37orbzJkzR1u2bNGhQ4dca6mpqdq/f7+KiookSRMmTJDD4dB7773n2ua+++5T586dtX79+mbNwp9J8B6n06nY2NgmTxSNbDabevToodLSUg7xonmcTgX37StbZaVsl7nYstlk9eihr0tLeSkKzeJ0OtW3b19VVlZe9nKbzaaoqCiVlZXxPNXKWnL/fcPfU1NUVKTk5GS3tdGjR2vt2rWqq6tTQECAioqKlJaW1mSbZcuWXfF2a2trVVtb6zrvcDhadG40344dO64YNJJkWZY+//xz2e32VpwK7dlwSduucrnNsmT7/HPdb7ersJVmgtksy1JFRYV27NihESNGeHscXKMb/umnqqoqhYWFua2FhYWpvr5e1dXVV92mqqrqireblZUlu93uOkVHR7f88GiWkydPensEGCaihbcDmovns/atVT79ZLO5H0BufMXr2+uX2+a7a9+WkZGh9PR013mHw0HYeElERPN2Lfn5+br33ntv8DQwQYft26WxY793u5z8fL3G7xSaYfv27RrbjN+p5j6foW264VETHh7e5IjLqVOn5O/vry5dulx1m+8evfm2wMBABQYGtvzA8FhiYqKioqJUWVmpy71Fq/G16uTkZF6rRvMkJ0tRUQ1vCr7c2/5sNikqSsHJybynBs2SnJzcrOepxMREL0yHlnLDX34aMmSICgoK3Na2bt2q+Ph4BQQEXHWbhISEGz0eWoCfn59eeeUVSU2PuDWeX7ZsGUGD5vPzk/7/d0rfPWLbeH7ZMoIGzcbzlI+wPHT27FmrpKTEKikpsSRZS5cutUpKSqwTJ05YlmVZc+fOtaZMmeLa/tixY1anTp2stLQ06+DBg9batWutgIAAa+PGja5tPv74Y8vPz8966aWXrEOHDlkvvfSS5e/vb33yySfNnqumpsaSZNXU1Hh6l9BCcnNzraioKEuS6xQdHW3l5uZ6ezS0V7m5lhUVZVkNx2saTtHRDevANeB5qu1pyf23xx/p3rZtm5KSkpqsT506VevWrdO0adN0/Phxbdu2zXVZYWGh0tLSVFpaqsjISM2ZM0epqalu19+4caPmzZunY8eO6ZZbbtHChQv18MMPN3suPtLdNvBNnWhxfKMwWhjPU21LS+6/r+t7atoSogYAgPanJfff/EFLAABgBKIGAAAYgagBAABGIGoAAIARiBoAAGAEogYAABiBqAEAAEYgagAAgBGIGgAAYASiBgAAGIGoAQAARiBqAACAEYgaAABgBKIGAAAYgagBAABGIGoAAIARiBoAAGAEogYAABiBqAEAAEYgagAAgBGIGgAAYASiBgAAGIGoAQAARiBqAACAEYgaAABgBKIGAAAYgagBAABGIGoAAIARiBoAAGAEogYAABiBqAEAAEYgagAAgBGIGgAAYASiBgAAGIGoAQAARiBqAACAEYgaAABgBKIGAAAYgagBAABGIGoAAIARiBoAAGAEogYAABiBqAEAAEYgagAAgBGIGgAAYASiBgAAGIGoAQAARiBqAACAEYgaAABgBKIGAAAYgagBAABGIGoAAIARiBoAAGAEogYAABiBqAEAAEYgagAAgBGuKWpWrFihXr16KSgoSHFxcdqxY8dVt1++fLn69Omj4OBg3XbbbXr99debbLNs2TLddtttCg4OVnR0tNLS0vTNN99cy3gAAMAH+Xt6hQ0bNmj27NlasWKFhg4dqldffVVjxozRwYMHFRMT02T7lStXKiMjQ2vWrNFdd92l4uJiTZ8+XZ07d1ZKSook6c0339TcuXOVk5OjhIQEHTlyRNOmTZMk/f73v7++ewgAAHyCzbIsy5MrDB48WIMGDdLKlStda3369NG4ceOUlZXVZPuEhAQNHTpUixcvdq3Nnj1be/bs0c6dOyVJzzzzjA4dOqQPPvjAtc2vfvUrFRcXf+9RoEYOh0N2u101NTUKDQ315C4BAAAvacn9t0cvP128eFF79+5VcnKy23pycrJ27dp12evU1tYqKCjIbS04OFjFxcWqq6uTJA0bNkx7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",
      "text/plain": [
       "<Figure size 640x480 with 1 Axes>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "p1=(2,1)\n",
    "p2=(8,1)\n",
    "x=[p1[0],p2[0]]\n",
    "y=[p1[1],p2[1]]\n",
    "plt.plot(x,y,marker='o',linestyle='-',color='black',zorder=1)\n",
    "labels=['p1','p2']\n",
    "for i in range(len(labels)):\n",
    "    plt.text(x[i]+0.005,y[i]+0.005,labels[i],fontsize=12)\n",
    "plt.xlim(0,10)\n",
    "t=0.5\n",
    "M_x=p1[0]*(1-t)+p2[0]*t\n",
    "M_y=p1[1]*(1-t)+p2[1]*t\n",
    "plt.text(M_x+0.005,M_y+0.005,'M',fontsize=12,color='red',zorder=2)\n",
    "plt.scatter(M_x, M_y,color='red')\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "212c10c7-def2-4751-9cf7-417f2763309e",
   "metadata": {},
   "source": [
    "3. Создать ползунок, с помощью которого можно будет перемещать точку\n",
    "отрезка от начальной точки 𝑃1\n",
    " до конечной 𝑃2\n",
    ". Какую переменную нужно привязать к\n",
    "ползунку для этого?"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "id": "380e839f-bb27-497c-bfc6-cdfc28f6a34b",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "application/vnd.jupyter.widget-view+json": {
       "model_id": "6ed6feaee74e43fca644a1ee234d17b4",
       "version_major": 2,
       "version_minor": 0
      },
      "text/plain": [
       "interactive(children=(FloatSlider(value=0.0, description='t', max=1.0, step=0.01), Output()), _dom_classes=('w…"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    },
    {
     "data": {
      "text/plain": [
       "<function __main__.plot_circle(t=0)>"
      ]
     },
     "execution_count": 4,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "max_t=0\n",
    "def plot_circle(t=0):\n",
    "    global max_t\n",
    "    if t>max_t:\n",
    "        max_t=t\n",
    "    p1=(2,1)\n",
    "    p2=(8,1)\n",
    "    x=[p1[0],p2[0]]\n",
    "    y=[p1[1],p2[1]]\n",
    "    plt.plot(x,y,marker='o',linestyle='-',color='black',zorder=1)\n",
    "    labels=['p1','p2']\n",
    "    for i in range(len(labels)):\n",
    "        plt.text(x[i]+0.005,y[i]+0.005,labels[i],fontsize=12)\n",
    "    plt.xlim(0,10)\n",
    "    M_x=p1[0]*(1-t)+p2[0]*t\n",
    "    M_y=p1[1]*(1-t)+p2[1]*t\n",
    "    M_x = p1[0]*(1-max_t)+p2[0]*max_t\n",
    "    M_y = p1[1]\n",
    "    plt.text(M_x+0.005,M_y+0.005,'M',fontsize=12,color='red',zorder=2)\n",
    "    plt.scatter(M_x, M_y,color='red')\n",
    "    plt.show()\n",
    "interactive_plot = interact(plot_circle, t=(0, 1, 0.01))\n",
    "interactive_plot"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "7a3da26a-7439-4f8b-a5dc-c59d486e0278",
   "metadata": {},
   "source": [
    "4. Сделайте так, чтобы точка двигалась в обратном направлении — от 𝑃2\n",
    " к 𝑃1"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "id": "9884106d-cec0-49f1-9135-af306a7d6fde",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "application/vnd.jupyter.widget-view+json": {
       "model_id": "dab44d17cfee4dd78e455c442bc8abcf",
       "version_major": 2,
       "version_minor": 0
      },
      "text/plain": [
       "interactive(children=(FloatSlider(value=1.0, description='t', max=1.0, step=0.01), Output()), _dom_classes=('w…"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    },
    {
     "data": {
      "text/plain": [
       "<function __main__.plot_circle(t=1)>"
      ]
     },
     "execution_count": 5,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "min_t=1\n",
    "def plot_circle(t=1):\n",
    "    global min_t\n",
    "    if t<min_t:\n",
    "        min_t=t\n",
    "    p1=(2,1)\n",
    "    p2=(8,1)\n",
    "    x=[p1[0],p2[0]]\n",
    "    y=[p1[1],p2[1]]\n",
    "    plt.plot(x,y,marker='o',linestyle='-',color='black',zorder=1)\n",
    "    labels=['p1','p2']\n",
    "    for i in range(len(labels)):\n",
    "        plt.text(x[i]+0.005,y[i]+0.005,labels[i],fontsize=12)\n",
    "    plt.xlim(0,10)\n",
    "    M_x=p1[0]*(1-t)+p2[0]*t\n",
    "    M_y=p1[1]*(1-t)+p2[1]*t\n",
    "    M_x = p1[0]*(1-min_t)+p2[0]*min_t\n",
    "    M_y = p1[1]\n",
    "    plt.text(M_x+0.005,M_y+0.005,'M',fontsize=12,color='red',zorder=2)\n",
    "    plt.scatter(M_x, M_y,color='red')\n",
    "    plt.show()\n",
    "interactive_plot = interact(plot_circle, t=(0, 1, 0.01))\n",
    "interactive_plot"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "e344661c-09e5-4f24-a22f-9f8dc9fa206c",
   "metadata": {},
   "source": [
    "двигается в разные стороны:"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "id": "e22870b8-db2e-4d96-bcae-f741357b6722",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "application/vnd.jupyter.widget-view+json": {
       "model_id": "3ed6b88bea0c446db934c8224bb2ddc8",
       "version_major": 2,
       "version_minor": 0
      },
      "text/plain": [
       "interactive(children=(FloatSlider(value=0.5, description='t', max=1.0, step=0.01), Output()), _dom_classes=('w…"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    },
    {
     "data": {
      "text/plain": [
       "<function __main__.plot_circle(t=0.5)>"
      ]
     },
     "execution_count": 6,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "def plot_circle(t=0.5):\n",
    "    p1=(2,1)\n",
    "    p2=(8,1)\n",
    "    x=[p1[0],p2[0]]\n",
    "    y=[p1[1],p2[1]]\n",
    "    plt.plot(x,y,marker='o',linestyle='-',color='black',zorder=1)\n",
    "    labels=['p1','p2']\n",
    "    for i in range(len(labels)):\n",
    "        plt.text(x[i]+0.005,y[i]+0.005,labels[i],fontsize=12)\n",
    "    plt.xlim(0,10)\n",
    "    M_x=p1[0]*(1-t)+p2[0]*t\n",
    "    M_y=p1[1]*(1-t)+p2[1]*t\n",
    "    plt.text(M_x+0.005,M_y+0.005,'M',fontsize=12,color='red',zorder=2)\n",
    "    plt.scatter(M_x, M_y,color='red')\n",
    "    plt.show()\n",
    "interactive_plot = interact(plot_circle, t=(0, 1, 0.01))\n",
    "interactive_plot"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "1d756222-8c30-4540-a39f-bbaf26513809",
   "metadata": {},
   "source": [
    "5. Не изменяя функции сделайте так, чтобы точка могла выходить за границы отрезка в\n",
    "обе стороны"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "id": "90f24bd5-29b3-4596-997b-e2a8bc66b27d",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "application/vnd.jupyter.widget-view+json": {
       "model_id": "b41d4eb8549c477d9f2741d65ad49494",
       "version_major": 2,
       "version_minor": 0
      },
      "text/plain": [
       "interactive(children=(FloatSlider(value=0.5, description='t', max=1.0, step=0.01), Output()), _dom_classes=('w…"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    },
    {
     "data": {
      "text/plain": [
       "<function __main__.plot_circle(t=0.5)>"
      ]
     },
     "execution_count": 7,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "def plot_circle(t=0.5):\n",
    "    p1=(2,1)\n",
    "    p2=(8,1)\n",
    "    x=[p1[0],p2[0]]\n",
    "    y=[p1[1],p2[1]]\n",
    "    z1=(1,1)\n",
    "    z2=(9,1)\n",
    "    z=[z1[0],z2[0]]\n",
    "    w=[z1[1],z2[1]]\n",
    "    plt.plot(x,y,marker='o',linestyle='-',color='black',zorder=1)\n",
    "    plt.plot(z,w,linestyle='-',color='black',zorder=2)\n",
    "    labels=['p1','p2']\n",
    "    for i in range(len(labels)):\n",
    "        plt.text(x[i]+0.005,y[i]+0.005,labels[i],fontsize=12)\n",
    "    plt.xlim(0,10)\n",
    "    M_x=z1[0]*(1-t)+z2[0]*t\n",
    "    M_y=z1[1]*(1-t)+z2[1]*t\n",
    "    plt.text(M_x+0.005,M_y+0.005,'M',fontsize=12,color='red',zorder=3)\n",
    "    plt.scatter(M_x, M_y,color='red')\n",
    "    plt.show()\n",
    "interactive_plot = interact(plot_circle, t=(0, 1, 0.01))\n",
    "interactive_plot"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "61cec0df-6751-4f35-aab7-e6b3a5af4d77",
   "metadata": {},
   "source": [
    "## Задание №2"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "17483d99-a627-41bb-a18b-500b616229cc",
   "metadata": {},
   "source": [
    "1. Пусть даны два вектора 𝐚 = (\n",
    "𝑎𝑥\n",
    "𝑎𝑦\n",
    ") и 𝐛 = (\n",
    "𝑏𝑥\n",
    "𝑏𝑦\n",
    "), оба имеют единичную длину, вектор 𝐚\n",
    "направлен под углом 10\n",
    "°\n",
    " к оси 𝑂𝑥, а 𝐛 под углом 40\n",
    "°\n",
    ". Вычислите их компоненты. Что\n",
    "делать в общем случае, когда мы хотим построить единичный вектор, направленный\n",
    "под определенным углом?"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "id": "0a03d80b-1457-4054-9452-6e29b4b86746",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "a = (0.984807753012208, 0.17364817766693033)\n",
      "b = (0.766044443118978, 0.6427876096865393)\n"
     ]
    },
    {
     "data": {
      "image/png": "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",
      "text/plain": [
       "<Figure size 600x600 with 1 Axes>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "a_x, a_y = np.cos(np.radians(10)), np.sin(np.radians(10))\n",
    "b_x, b_y = np.cos(np.radians(40)), np.sin(np.radians(40))\n",
    "print(f\"a = ({a_x}, {a_y})\")\n",
    "print(f\"b = ({b_x}, {b_y})\")\n",
    "plt.figure(figsize=(6,6))\n",
    "plt.quiver(0, 0, a_x, a_y, angles='xy', scale_units='xy', scale=1, label='a')\n",
    "plt.quiver(0, 0, b_x, b_y, angles='xy', scale_units='xy', scale=1, color='blue', label='b')\n",
    "plt.xlim(-0.2, 1.2)\n",
    "plt.ylim(-0.2, 1.2)\n",
    "plt.grid(alpha=0.3)\n",
    "plt.axhline(0, linewidth=0.5)\n",
    "plt.axvline(0, linewidth=0.5)\n",
    "plt.legend()\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "8095f80d-aa86-41ae-887c-ca59dcc7b156",
   "metadata": {},
   "source": [
    "2. Нарисуйте векторы 𝐚 и 𝐛 как это показано на Рис. 2. В каком месте координатной плоскости вы будете их рисовать? Обязаны ли они быть отложены от одной точки?\n"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "01715657-c887-4bf2-96a3-ea8ebeb03fcc",
   "metadata": {},
   "source": [
    "в предыдущем пункте нарисовала векторы как на рис.2, располагаются в первой четверти к.п, векторы не обязаны исходить из одной точки, но в данном случае это так"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "14f8aca8-07e0-4d63-9709-c4b9de7a098b",
   "metadata": {},
   "source": [
    "3. Вычислите площадь треугольника, построенного на векторах 𝐚 и 𝐛. Вычислите площадь\n",
    "параллелограмма, построенного на тех же векторах. Вычислите ориентированные\n",
    "площади треугольника и параллелограмма.\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 36,
   "id": "cdb5302b-ec4b-49a7-81fc-b14a7ad0c8ca",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "a = (0.984807753012208, 0.17364817766693033)\n",
      "b = (0.766044443118978, 0.6427876096865393)\n",
      "площадь параллелограмма = 0.49999999999999994\n",
      "площадь треугольника = 0.24999999999999997\n",
      "ориентированная площадь п-а = 0.49999999999999994\n",
      "ориентированная площадь треугольника т-а = 0.24999999999999997\n"
     ]
    },
    {
     "data": {
      "image/png": "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",
      "text/plain": [
       "<Figure size 600x600 with 1 Axes>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "a_x, a_y = np.cos(np.radians(10)), np.sin(np.radians(10))\n",
    "b_x, b_y = np.cos(np.radians(40)), np.sin(np.radians(40))\n",
    "print(f\"a = ({a_x}, {a_y})\")\n",
    "print(f\"b = ({b_x}, {b_y})\")\n",
    "plt.figure(figsize=(6,6))\n",
    "plt.quiver(0, 0, a_x, a_y, angles='xy', scale_units='xy', scale=1, label='a')\n",
    "plt.quiver(0, 0, b_x, b_y, angles='xy', scale_units='xy', scale=1, color='blue', label='b')\n",
    "\n",
    "c = a_x*b_y-a_y*b_x\n",
    "print(f\"площадь параллелограмма = {abs(c)}\")\n",
    "print(f\"площадь треугольника = {abs(c)/2}\")\n",
    "print(f\"ориентированная площадь п-а = {c}\")\n",
    "print(f\"ориентированная площадь треугольника т-а = {c/2}\")\n",
    "plt.quiver(a_x, a_y, b_x, b_y, angles='xy', scale_units='xy', scale=1, color='lightblue')\n",
    "plt.quiver(b_x, b_y, a_x, a_y, angles='xy', scale_units='xy', scale=1, color='lightblue')\n",
    "\n",
    "plt.xlim(-0.2, 2)\n",
    "plt.ylim(-0.2, 1.2)\n",
    "plt.grid(alpha=0.3)\n",
    "plt.axhline(0, linewidth=0.5)\n",
    "plt.axvline(0, linewidth=0.5)\n",
    "plt.legend()\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "9a9c6df5-8671-40ef-8278-cf51a1699e72",
   "metadata": {},
   "source": [
    "4. Вычислите ориентированную площадь треугольника, построенного на векторах 𝐛 и 𝐚\n",
    "(это не опечатка, дублирующая предыдущее задание)."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 37,
   "id": "a1a9d9d8-321f-47b4-9e73-e4bbcea093c9",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "np.float64(-0.49999999999999994)"
      ]
     },
     "execution_count": 37,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "c_a=b_x*a_y-b_y*a_x\n",
    "c_a"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "80efbd1c-f5ca-4e80-a3db-37a67887574c",
   "metadata": {},
   "source": [
    "5. Задайте теперь не векторы 𝐚 и 𝐛, а два комплексных числа 𝑧1 = 𝑎𝑥 + 𝑎𝑦\n",
    "𝑖 и 𝑧2 = 𝑏𝑥 + 𝑏𝑦\n",
    "𝑖.\n",
    "Как их отобразить на комплексной плоскости? Откуда их следует откладывать? Вычислите 𝑒\n",
    "10\n",
    "°\n",
    "𝑖\n",
    " и 𝑒\n",
    "40\n",
    "°\n",
    "𝑖\n",
    ".\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "3823c212-9826-4ce9-bc4e-d14e7ac96911",
   "metadata": {},
   "outputs": [],
   "source": [
    "z1 = a_x + a_y*1j\n",
    "z2 = b_x + b_y*1j\n",
    "e10 = np.exp(1j*np.radians(10))\n",
    "e40 = np.exp(1j*np.radians(40))\n",
    "print(f\"\\ne^(i·10) = {e10}\")\n",
    "print(f\"e^(i·40) = {e40}\")\n",
    "plt.figure(figsize=(6, 6))\n",
    "plt.scatter(z1.real, z1.imag, color='red',label='z1(10)')\n",
    "plt.scatter(z2.real, z2.imag, color='blue',label='z2(40)')\n",
    "plt.quiver(0, 0, z1.real, z1.imag, angles='xy', scale_units='xy', scale=1)\n",
    "plt.quiver(0, 0, z2.real, z2.imag, angles='xy', scale_units='xy', scale=1)\n",
    "plt.text(z1.real+0.03, z1.imag+0.03, 'z1', fontsize=12)\n",
    "plt.text(z2.real+0.03, z2.imag+0.03, 'z2', fontsize=12)\n",
    "plt.text(0.03, 0.03, '0', fontsize=12)\n",
    "plt.xlim(-1.2, 1.2)\n",
    "plt.ylim(-1.2, 1.2)\n",
    "plt.grid(alpha=0.3)\n",
    "plt.axhline(0)\n",
    "plt.axvline(0)\n",
    "plt.legend()\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "ab1ecd66-acc8-4b54-a5f8-598c2d6178dd",
   "metadata": {},
   "source": [
    "## Задание №3"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "2000f3b6-38d4-4f3e-961a-54b912e2972c",
   "metadata": {},
   "source": [
    "В предыдущем задании вы должны были научиться задавать вектор, направленный\n",
    "под определенным углом к оси 𝑂𝑥. Такой вектор можно использовать, чтобы отобразить\n",
    "прямую для которой он будет служить направляющим вектором. Для этого следует\n",
    "использовать формулу\n",
    "𝐩(𝑡) = 𝐩0 + 𝐯𝑡,\n",
    "где 𝐩0\n",
    " — некоторая точка прямой, а 𝐯 — направляющий вектор прямой.\n",
    "1. Используйте вышеуказанную формулу для отображения прямой. Для этого вам нужно"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "e4def5d3-1e71-4142-a362-41b81b3b9ecc",
   "metadata": {},
   "outputs": [],
   "source": [
    "v_x = np.cos(np.radians(10))\n",
    "v_y = np.sin(np.radians(10))\n",
    "t=np.linspace(-1,1)\n",
    "p0_x, p0_y = 0, 0\n",
    "p1_x=p0_x+v_x*t\n",
    "p1_y=p0_y+v_y*t\n",
    "plt.figure(figsize=(6, 6))\n",
    "plt.plot(p1_x, p1_y,color='black', zorder=1)\n",
    "plt.quiver(p0_x, p0_y, v_x, v_y, color='red', scale=3, zorder=2)\n",
    "plt.xlim(-1.2, 1.2)\n",
    "plt.ylim(-1.2, 1.2)\n",
    "plt.grid(alpha=0.3)\n",
    "plt.axhline(0,zorder=0)\n",
    "plt.axvline(0,zorder=0)\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "4755984e-34c7-431f-bfe2-af7f8bd144d3",
   "metadata": {},
   "source": [
    "2. Создать ползунок, который будет управлять направлением вектора 𝐯 в градусах.\n",
    "Отобразить прямую и двигая ползунок изменять ее наклон. Прямая всегда должна\n",
    "отображаться как бесконечная прямая, а не как отрезок то есть при любом размере\n",
    "координатной плоскости оба конца прямой должны упираться в границу картинки."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "eaeb1831-2c1e-4772-8a78-8153d96987a6",
   "metadata": {},
   "outputs": [],
   "source": [
    "def plot_line(angle):\n",
    "    v_x = np.cos(np.radians(angle))\n",
    "    v_y = np.sin(np.radians(angle))\n",
    "    t=np.linspace(-5,5)\n",
    "    p0_x, p0_y = 0, 0\n",
    "    p1_x=p0_x+v_x*t + 0.5\n",
    "    p1_y=p0_y+v_y*t \n",
    "    plt.figure(figsize=(6, 6))\n",
    "    plt.plot(p1_x, p1_y,color='black', zorder=1)\n",
    "    #plt.quiver(p0_x, p0_y, v_x, v_y, color='red', scale=3, zorder=2)\n",
    "    plt.xlim(-1.2, 1.2)\n",
    "    plt.ylim(-1.2, 1.2)\n",
    "    plt.grid(alpha=0.3)\n",
    "    plt.axhline(0,zorder=0)\n",
    "    plt.axvline(0,zorder=0)\n",
    "    plt.show()\n",
    "interact(plot_line, angle=widgets.IntSlider(min=0, max=360, step=5))"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "09f62b65-2db1-4cc6-ba95-00fb6c55ce32",
   "metadata": {},
   "source": [
    "3. Вручную реализовать требования предыдущего пункта довольно тяжело. Поэтому в\n",
    "Matplotlib существует функция axline для отображения бесконечной прямой. Выяснить и уметь объяснить математический смысл всех аргументов данной функции.\n",
    "Задать угол наклона прямой (в градусах) с помощью ползунка. Отобразить прямую\n",
    "теперь уже только с помощью axline и менять ее наклон ползунком также как и в\n",
    "предыдущем пункте с шагом в 1\n",
    "°\n",
    "."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "fe981fc7-3844-4087-9aeb-0a8e568ca8a1",
   "metadata": {},
   "outputs": [],
   "source": [
    "def plot_line(angle):\n",
    "    v_x = np.cos(np.radians(angle))\n",
    "    v_y = np.sin(np.radians(angle))\n",
    "    p0_x, p0_y = 0, 0\n",
    "    plt.figure(figsize=(6, 6))\n",
    "    plt.axline((p0_x, p0_y), (p0_x+v_x, p0_y+v_y), color='black', zorder=1)\n",
    "    p1_x=p0_x+v_x*t\n",
    "    p1_y=p0_y+v_y*t\n",
    "    #plt.plot(p1_x, p1_y,color='black', zorder=1)\n",
    "    plt.quiver(p0_x, p0_y, v_x, v_y, color='red', scale=3, zorder=2)\n",
    "    plt.xlim(-1.2, 1.2)\n",
    "    plt.ylim(-1.2, 1.2)\n",
    "    plt.grid(alpha=0.3)\n",
    "    plt.axhline(0)\n",
    "    plt.axvline(0)\n",
    "    plt.show()\n",
    "interact(plot_line, angle=widgets.IntSlider(min=0, max=360, step=1))"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "92cb164a-65d4-4a37-a440-5c89ec780e82",
   "metadata": {},
   "source": [
    "## Задание №4"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "8e380d28-562c-4477-bd3d-d5ecb6087505",
   "metadata": {},
   "source": [
    "1. Нарисуйте без заливки цветом окружность с центром в точке O, радиуса 𝑅 = 1 с помощью примитива Circle из модуля patches.\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "e6ab8ecf-044e-4b9b-bcf5-63797e6c1940",
   "metadata": {},
   "outputs": [],
   "source": [
    "circle = Circle((0, 0), radius=1, fill=False)\n",
    "plt.figure(figsize=(6, 6))\n",
    "plt.gca().add_patch(circle)\n",
    "plt.xlim(-1.2, 1.2)\n",
    "plt.ylim(-1.2, 1.2)\n",
    "plt.grid(alpha=0.3)\n",
    "plt.axhline(0)\n",
    "plt.axvline(0)\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "f51e2ae4-b2a9-4c85-8378-4b3aa7e5fb81",
   "metadata": {},
   "source": [
    "2. Отобразите радиус окружности в виде стрелки или в виде отрезка."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "b15d9998-753a-40c7-9336-cea675f07a37",
   "metadata": {},
   "outputs": [],
   "source": [
    "a_x, a_y = np.cos(np.radians(45)), np.sin(np.radians(45))\n",
    "plt.figure(figsize=(6,6))\n",
    "plt.quiver(0, 0, a_x, a_y, angles='xy', scale_units='xy', scale=1)\n",
    "circle = Circle((0, 0), radius=1, fill=False)\n",
    "plt.gca().add_patch(circle)\n",
    "plt.xlim(-1.2, 1.2)\n",
    "plt.ylim(-1.2, 1.2)\n",
    "plt.grid(alpha=0.3)\n",
    "plt.axhline(0)\n",
    "plt.axvline(0)\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "381567f6-0059-4347-a761-2545cbe32832",
   "metadata": {},
   "source": [
    "3. Создайте ползунок, который будет вращать радиус окружности по часовой стрелке с\n",
    "шагом в 1\n",
    "°\n",
    ". По периметру окружности проставьте цифры циферблата часов"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "c63f4b77-4b9a-4582-a39d-bc25ab09bbdb",
   "metadata": {},
   "outputs": [],
   "source": [
    "def plot_line(angle_input):\n",
    "    if angle_input>0:\n",
    "        angle=360-angle_input\n",
    "    else:\n",
    "        angle=0\n",
    "    a_x, a_y = np.cos(np.radians(angle)), np.sin(np.radians(angle))\n",
    "    plt.figure(figsize=(6,6))\n",
    "    plt.quiver(0, 0, a_x, a_y, angles='xy', scale_units='xy', scale=1)\n",
    "    circle = Circle((0, 0), radius=1, fill=False)\n",
    "    plt.gca().add_patch(circle)\n",
    "    for i in range(12):\n",
    "        angle = np.radians(90-i*30)\n",
    "        x = np.cos(angle)\n",
    "        y = np.sin(angle)\n",
    "        if i==0:\n",
    "            number=12\n",
    "        else:\n",
    "            number=i\n",
    "        plt.scatter(x, y, color='black', zorder=3)\n",
    "        plt.text(x*1.2, y*1.2, str(number),fontsize=10)\n",
    "    plt.xlim(-1.5, 1.5)\n",
    "    plt.ylim(-1.5, 1.5)\n",
    "    plt.grid(alpha=0.3)\n",
    "    plt.axhline(0,linewidth=0.5)\n",
    "    plt.axvline(0,linewidth=0.5)\n",
    "    plt.show()\n",
    "interact(plot_line, angle_input=widgets.IntSlider(min=0, max=360, step=1))"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "bfd6ade3-f012-4cc5-9567-3d4ed5ca25a7",
   "metadata": {},
   "source": [
    "4. Используйте параметрическое уравнение окружности\n",
    "𝐩(𝑡) = [\n",
    "𝑅 cos𝑡\n",
    "𝑅 sin 𝑡\n",
    "] ⇔ {\n",
    "𝑥(𝑡) = 𝑅 cos𝑡,\n",
    "𝑦(𝑡) = 𝑅 sin 𝑡,\n",
    "для того, чтобы нарисовать цифры в нужных местах окружности."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "c8011a6d-de45-4d99-a52f-7a1da3a4151b",
   "metadata": {},
   "outputs": [],
   "source": [
    "a_x, a_y=np.cos(np.radians(45)), np.sin(np.radians(45))\n",
    "plt.figure(figsize=(6,6))\n",
    "plt.quiver(0, 0, a_x, a_y, angles='xy', scale_units='xy', scale=1)\n",
    "circle=Circle((0, 0), radius=1, fill=False)\n",
    "plt.gca().add_patch(circle)\n",
    "r=1\n",
    "for hour in range(1,13):\n",
    "    if hour==12:\n",
    "        t=np.pi/2\n",
    "    else:\n",
    "        t=np.pi/2-hour*2*np.pi/12\n",
    "    x=r*np.cos(t)\n",
    "    y=r*np.sin(t)\n",
    "    plt.scatter(x, y, color='black',zorder=3)\n",
    "    plt.text(x*1.2, y*1.2,hour,fontsize=12)\n",
    "plt.xlim(-1.5, 1.5)\n",
    "plt.ylim(-1.5, 1.5)\n",
    "plt.grid(alpha=0.3)\n",
    "plt.axhline(0,linewidth=0.5)\n",
    "plt.axvline(0,linewidth=0.5)\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "75113e86-b8c7-42dd-999d-55a278c47378",
   "metadata": {},
   "source": [
    "## Задание №5"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "3caf976f-b33e-477f-8ac1-79477347fafc",
   "metadata": {},
   "source": [
    "1. Нарисуйте прямоугольник (не квадрат) с помощью примитива Polygon из модуля\n",
    "patches. Нарисуйте его так, чтобы центр пересечения диагоналей лежал в начале\n",
    "координат."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "018b83dd-d4fd-43d2-8ae4-4978e725c160",
   "metadata": {},
   "outputs": [],
   "source": [
    "pr, ox = plt.subplots()\n",
    "rect=patches.Rectangle((1, 0.5), -2, -1, edgecolor='black', facecolor='none') #x0,yo,ширина,высота\n",
    "ox.add_patch(rect)\n",
    "x0,y0=-1,-0.5  #лн\n",
    "x1,y1=1,-0.5  #пн\n",
    "x2,y2=1,0.5  #пв\n",
    "x3,y3=-1,0.5  #лв\n",
    "plt.plot([x0, x2],[y0, y2],color='black')\n",
    "plt.plot([x3, x1],[y3, y1],color='black')\n",
    "plt.xlim(-1.5, 1.5)\n",
    "plt.ylim(-1.5, 1.5)\n",
    "plt.grid(alpha=0.3)\n",
    "plt.axhline(0,linewidth=0.5)\n",
    "plt.axvline(0,linewidth=0.5)\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "8bb74924-002e-4009-a537-2dd31e8d6e38",
   "metadata": {},
   "source": [
    "2. Умножьте все радиус векторы вершин прямоугольника на матрицу\n",
    "[[1,-1], [1,1]]\n",
    "и отобразите во что преобразовался после этого исходный прямоугольник."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "876eb0a7-05aa-4702-a101-052a7dc40664",
   "metadata": {},
   "outputs": [],
   "source": [
    "x0, y0 = -1, -0.5\n",
    "width, height = 2, 1\n",
    "vertices = np.array([[x0, y0],[x0+width, y0],[x0+width, y0+height],[x0, y0+height],[x0, y0]])\n",
    "M = np.array([[1,-1],[1,1]])\n",
    "trans = vertices @ M.T\n",
    "plt.figure(figsize=(10, 5))\n",
    "plt.plot(trans[:, 0],trans[:, 1],color='black')\n",
    "plt.grid(alpha=0.3)\n",
    "plt.axhline(0, color='black', linewidth=0.5)\n",
    "plt.axvline(0, color='black', linewidth=0.5)\n",
    "plt.xlim(-2, 2)\n",
    "plt.ylim(-2, 2)\n",
    "plt.gca().set_aspect('equal')\n",
    "plt.tight_layout()\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "0d100976-7e55-42d2-be29-4e233eabc388",
   "metadata": {},
   "source": [
    "3. Вычислите ориентированную площадь исходного прямоугольника. В каком порядке\n",
    "нужно перечислить вершины прямоугольника, чтобы ориентированная площадь имела положительный знак?"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "54dfa69f-d841-4e98-81e0-51d751e63010",
   "metadata": {},
   "outputs": [],
   "source": [
    "x0, y0 = -1, -0.5\n",
    "width, height = 2, 1\n",
    "vertices = np.array([[x0, y0],[x0+width, y0],[x0+width, y0+height],[x0, y0+height],[x0, y0]])\n",
    "def oriented_area(vertices):\n",
    "    n=len(vertices)\n",
    "    area=0\n",
    "    for i in range(n):\n",
    "        x1, y1 = vertices[i]\n",
    "        x2, y2 = vertices[(i+1)%n]\n",
    "        area+=x1*y2-x2*y1\n",
    "    return area/2\n",
    "area = oriented_area(vertices)\n",
    "print(area) #нужно перечислять вершины против часовой стрелки"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "3d7412dc-0e88-4183-9710-81d0bf1f373a",
   "metadata": {},
   "source": [
    "4. Вновь умножьте радиус векторы вершин на матрицу [[-1,1], [1,1]]\n",
    "и вновь вычислите ориентированную площадь. Объясните изменение ее знака и\n",
    "абсолютной величины."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "c34edefb-06be-4c6f-a639-157f3c455051",
   "metadata": {},
   "outputs": [],
   "source": [
    "x0, y0 = -1, -0.5\n",
    "width, height = 2, 1\n",
    "vertices = np.array([[x0, y0],[x0+width, y0],[x0+width, y0+height],[x0, y0+height],[x0, y0]])\n",
    "def oriented_area(vertices):\n",
    "    n=len(vertices)\n",
    "    area=0\n",
    "    for i in range(n):\n",
    "        x1, y1 = vertices[i]\n",
    "        x2, y2 = vertices[(i+1)%n]\n",
    "        area+=x1*y2-x2*y1\n",
    "    return area/2\n",
    "M=np.array([[-1,1],[1,1]])\n",
    "trans_vertices=vertices @ M.T\n",
    "new_area=oriented_area(trans_vertices)\n",
    "det = np.linalg.det(M)\n",
    "print(f\"определитель: {det}\")\n",
    "print(f\"о-я площадь: {new_area}\") #знак изменился (как и абсолютная величина) из-за определителя"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "ea84a184-bb97-4c89-b1ff-ee76a20e3568",
   "metadata": {},
   "source": [
    "## Задание №6"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "67714f24-7a4c-4a90-a398-836752a7284b",
   "metadata": {},
   "source": [
    "1. Нарисуйте эллипс с помощью функции plot, используя его параметрическое уравнение:\n",
    "𝐩(𝑡) = [\n",
    "𝑎 cos𝑡\n",
    "𝑏 sin 𝑡\n",
    "] ⇔ {\n",
    "𝑥(𝑡) = 𝑎 cos𝑡,\n",
    "𝑦(𝑡) = 𝑏 sin 𝑡,\n",
    "с помощью аргументов marker, markersize, markevery отобразите точки эллипса,\n",
    "соответствующие значениям параметра 𝑡. Сколько значений параметра вы взяли?"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "1f83a42d-af5b-4f88-bfc6-fa7a8cd5d539",
   "metadata": {},
   "outputs": [],
   "source": [
    "a=3 #x\n",
    "b=1 #y\n",
    "points=40\n",
    "t=np.linspace(0,2*np.pi,points)\n",
    "x=a*np.cos(t)\n",
    "y=b*np.sin(t)\n",
    "plt.figure(figsize=(6, 6))\n",
    "plt.plot(x,y)\n",
    "plt.plot(x, y, 'ro', markersize=5, markevery=1)\n",
    "plt.grid(alpha=0.3)\n",
    "plt.axhline(0,linewidth=0.5)\n",
    "plt.axvline(0,linewidth=0.5)\n",
    "plt.xlim(-a-0.5, a+0.5)\n",
    "plt.ylim(-b-0.5, b+0.5)\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "3bf15ab3-7221-4528-a77b-f652db0cff6a",
   "metadata": {},
   "source": [
    "2. Используйте трансляцию, чтобы переместить эллипс из центра координат в точку (1, 1)."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "d7d8f4a8-3ab7-4036-9a1f-e91f83812359",
   "metadata": {},
   "outputs": [],
   "source": [
    "a, b = 3, 1\n",
    "center = np.array([1, 1])\n",
    "t = np.linspace(0, 2*np.pi, 50)\n",
    "x0 = a*np.cos(t)\n",
    "y0 = b*np.sin(t)\n",
    "ellipse0 = np.column_stack([x0, y0])\n",
    "ellipse = ellipse0 + center\n",
    "plt.figure(figsize=(6, 6))\n",
    "plt.plot(ellipse0[:, 0], ellipse0[:, 1], 'b--', alpha=0.5)\n",
    "plt.plot(ellipse[:, 0], ellipse[:, 1], 'r-')\n",
    "plt.scatter([0, center[0]], [0, center[1]],zorder=5)\n",
    "plt.grid(alpha=0.3)\n",
    "plt.axhline(0,linewidth=0.5)\n",
    "plt.axvline(0,linewidth=0.5)\n",
    "plt.xlim(-4, 5)\n",
    "plt.ylim(-2, 3)\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "e4b2517e-3aee-459b-90d0-e674a630cbad",
   "metadata": {},
   "source": [
    "3. Нарисуйте одну ветвь гиперболы с помощью параметрического уравнения:\n",
    "𝐩(𝑡) = [\n",
    "𝑎 ch 𝑡\n",
    "𝑏 sh 𝑡\n",
    "] ⇔ {\n",
    "𝑥(𝑡) = 𝑎 ch 𝑡,\n",
    "𝑦(𝑡) = 𝑏 sh 𝑡"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "0126b3bb-b922-40b6-aa95-899031a06a63",
   "metadata": {},
   "outputs": [],
   "source": [
    "a=2\n",
    "b=1\n",
    "t=np.linspace(-2,2)\n",
    "x=a*np.cosh(t)\n",
    "y=b*np.sinh(t)\n",
    "plt.figure(figsize=(6, 6))\n",
    "plt.plot(x, y)\n",
    "plt.scatter(a,0,zorder=5)\n",
    "plt.grid(alpha=0.3)\n",
    "plt.axhline(0,linewidth=0.5)\n",
    "plt.axvline(0,linewidth=0.5)\n",
    "plt.xlim(-1, 5)\n",
    "plt.ylim(-3, 3)\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "f00c91c1-e6fa-44ec-9ffb-1bfcd2c0fcd3",
   "metadata": {},
   "source": [
    "4. Выясните геометрический смысл параметров 𝑎, 𝑏."
   ]
  },
  {
   "cell_type": "markdown",
   "id": "3b78769f-5308-4f0b-ac6f-9095fb67c0b3",
   "metadata": {},
   "source": [
    "a - положение вершины\n",
    "b - наклон асимптот"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "f1a40ca6-5635-4442-b58d-35bd6120913f",
   "metadata": {},
   "outputs": [],
   "source": [
    "a=2\n",
    "b=2\n",
    "t=np.linspace(-2,2)\n",
    "x=a*np.cosh(t)\n",
    "y=b*np.sinh(t)\n",
    "plt.figure(figsize=(6, 6))\n",
    "t_line=np.linspace(-3,3)\n",
    "plt.plot(a*t_line, b*t_line, 'r--', alpha=0.5)\n",
    "plt.plot(a*t_line, -b*t_line, 'r--', alpha=0.5)\n",
    "plt.plot(x, y)\n",
    "plt.scatter(a,0,zorder=5)\n",
    "plt.grid(alpha=0.3)\n",
    "plt.axhline(0,linewidth=0.5)\n",
    "plt.axvline(0,linewidth=0.5)\n",
    "plt.xlim(-1, 5)\n",
    "plt.ylim(-3, 3)\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "1f25cf96-b2ea-4180-ba4c-4f533662670c",
   "metadata": {},
   "source": [
    "5. Создайте два ползунка, которыми можно менять значения параметров 𝑎 и 𝑏 и изучите\n",
    "как при этом меняется вид кривой?"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "98819279-00f9-4e5e-8830-8083c63e020a",
   "metadata": {},
   "outputs": [],
   "source": [
    "def plot_line(a):\n",
    "    b=2\n",
    "    t=np.linspace(-2,2)\n",
    "    x=a*np.cosh(t)\n",
    "    y=b*np.sinh(t)\n",
    "    plt.figure(figsize=(6, 6))\n",
    "    t_line=np.linspace(-3,3)\n",
    "    plt.plot(a*t_line, b*t_line, 'r--', alpha=0.5)\n",
    "    plt.plot(a*t_line, -b*t_line, 'r--', alpha=0.5)\n",
    "    plt.plot(x, y)\n",
    "    plt.scatter(a,0,zorder=5)\n",
    "    plt.grid(alpha=0.3)\n",
    "    plt.axhline(0,linewidth=0.5)\n",
    "    plt.axvline(0,linewidth=0.5)\n",
    "    plt.xlim(-1, 5)\n",
    "    plt.ylim(-3, 3)\n",
    "    plt.show()\n",
    "def plot_lint(b):\n",
    "    a=2\n",
    "    t=np.linspace(-2,2)\n",
    "    x=a*np.cosh(t)\n",
    "    y=b*np.sinh(t)\n",
    "    plt.figure(figsize=(6, 6))\n",
    "    t_line=np.linspace(-3,3)\n",
    "    plt.plot(a*t_line, b*t_line, 'r--', alpha=0.5)\n",
    "    plt.plot(a*t_line, -b*t_line, 'r--', alpha=0.5)\n",
    "    plt.plot(x, y)\n",
    "    plt.scatter(a,0,zorder=5)\n",
    "    plt.grid(alpha=0.3)\n",
    "    plt.axhline(0,linewidth=0.5)\n",
    "    plt.axvline(0,linewidth=0.5)\n",
    "    plt.xlim(-1, 5)\n",
    "    plt.ylim(-3, 3)\n",
    "    plt.show()\n",
    "interact(plot_line, a=widgets.FloatSlider(min=0, max=3, step=0.1, value=2))\n",
    "interact(plot_lint, b=widgets.FloatSlider(min=0, max=3, step=0.1, value=1))"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "88007008-f6a3-4554-ad80-d0049b81947a",
   "metadata": {},
   "source": [
    "## Задание №7"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "9541e877-0377-4acd-bfee-08a7d843fc76",
   "metadata": {},
   "source": [
    "1. Сделайте часы с циферблатом в виде окружности. Сделайте так, чтобы по циферблату\n",
    "сама собой двигалась секундная стрелка\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "8b55070d-4efb-410e-a8fe-40a3fc316ae8",
   "metadata": {},
   "outputs": [],
   "source": [
    "fig, ax = plt.subplots(figsize=(8, 8))\n",
    "ax.set_xlim(-1.2, 1.2)\n",
    "ax.set_ylim(-1.2, 1.2)\n",
    "ax.grid(alpha=0.3)\n",
    "ax.axhline(0,linewidth=0.5)\n",
    "ax.axvline(0,linewidth=0.5)\n",
    "t=np.linspace(0,2*np.pi)\n",
    "ax.plot(np.cos(t), np.sin(t), 'b-', linewidth=2)\n",
    "ar,=ax.plot([],[],'r-',linewidth=2) #запятая нужна, чтобы получить сам объект, а не список с одним объектом, пустой объект линии (без точек)\n",
    "def update(frame):\n",
    "    angle = np.radians(90-frame*6)\n",
    "    x=0.9*np.cos(angle)\n",
    "    y=0.9*np.sin(angle)\n",
    "    ar.set_data([0,x], [0,y]) #обновление линии\n",
    "    return ar,\n",
    "for hour in range(1,13):\n",
    "    if hour==12:\n",
    "        t=np.pi/2\n",
    "    else:\n",
    "        t=np.pi/2-hour*2*np.pi/12\n",
    "    x=r*np.cos(t)\n",
    "    y=r*np.sin(t)\n",
    "    plt.scatter(x, y, color='black',zorder=3)\n",
    "    plt.text(x*1.1, y*1.1,hour,fontsize=12)\n",
    "ani=FuncAnimation(fig, update, frames=60, interval=1000, blit=True)\n",
    "plt.close()\n",
    "HTML(ani.to_jshtml())"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "a80758d8-0083-4f03-af98-15c3f86f3198",
   "metadata": {},
   "source": [
    "2. Сделайте такие же часы, но с циферблатом в виде эллипса. В каких точках нужно разместить цифры, чтобы секундная стрелка адекватно отображала время?"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "d423dfb8-6721-4f64-af6e-c55a75f6434e",
   "metadata": {},
   "outputs": [],
   "source": [
    "a, b = 2, 1\n",
    "fig, ax = plt.subplots(figsize=(8, 8))\n",
    "ax.set_xlim(-a-0.3, a+0.3)\n",
    "ax.set_ylim(-b-0.3, b+0.3)\n",
    "ax.grid(alpha=0.3)\n",
    "ax.axhline(0, linewidth=0.5)\n",
    "ax.axvline(0, linewidth=0.5)\n",
    "t = np.linspace(0, 2*np.pi, 100)\n",
    "ax.plot(a*np.cos(t), b*np.sin(t), 'b-', linewidth=2)\n",
    "for hour in range(1, 13):\n",
    "    angle = np.pi/2-hour*2*np.pi/12\n",
    "    x=a*np.cos(angle)\n",
    "    y=b*np.sin(angle)\n",
    "    plt.scatter(x, y, color='black',zorder=3)\n",
    "    plt.text(x*1.1, y*1.1,hour,fontsize=12)\n",
    "ar, = ax.plot([], [], 'r-', linewidth=2)\n",
    "def update(frame):\n",
    "    angle=np.radians(90-frame*6)\n",
    "    length_f=0.9\n",
    "    x_end=length_f*a*np.cos(angle)\n",
    "    y_end=length_f*b*np.sin(angle)\n",
    "    ar.set_data([0, x_end], [0, y_end])\n",
    "    return ar,\n",
    "ani = FuncAnimation(fig, update, frames=60, interval=1000, blit=True)\n",
    "plt.close()\n",
    "HTML(ani.to_jshtml())"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.13.5"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
