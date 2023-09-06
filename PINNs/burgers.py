from tools import *
import torch
import torch.nn as nn
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

from scipy.stats import qmc
import scipy

#データの作成

#初期条件データ数
n_ic_points = 100
#上側境界条件データ数
n_bc1_points = 50
#下側境界条件データ数
n_bc2_points = 50

#scipy.stats.qmcクラスをインスタンス化(空間データと時間発展の初期及び境界データを生成するのに使用する。)
engine = qmc.LatinHypercube(d=1)

# 1[s]までの時間を乱数で生成
# 後から境界の下限と上限に割り振る。
t_d = engine.random(n=n_bc1_points + n_bc2_points)
# 初期条件なので時刻は0
temp = np.zeros([n_ic_points, 1]) 
# 初期条件と境界の時間を結合する。
t_d = np.append(temp, t_d, axis=0)

# 空間データ
# 初期の空間座標
x_d = engine.random(n=n_ic_points)
x_d = 2 * (x_d - 0.5)
# 境界の空間座標
temp1 = -1 * np.ones([n_bc1_points, 1]) # for BC1 ; x = -1
temp2 = +1 * np.ones([n_bc2_points, 1]) # for BC2 ; x = +1
# 初期条件と境界の座標を結合する。
x_d = np.append(x_d, temp1, axis=0)
x_d = np.append(x_d, temp2, axis=0)

# データポイントの可視化
plt.figure(figsize=(8, 3))
plt.scatter(t_d, x_d, marker="x", c="k")
plt.xlabel("t")
plt.ylabel("x")
plt.title("Data points (BCs & IC)")
# 初期条件、境界条件を設定する。

# 初期条件と境界条件で設定した空間ポイントだけ用意する。
y_d = np.zeros(x_d.shape)

# 0からn_ic_pointsは初期条件の領域
y_d[ : n_ic_points] = -np.sin(np.pi * x_d[:n_ic_points])

# 境界条件の設定
y_d[n_ic_points : n_bc1_points + n_ic_points] = 0
y_d[n_bc1_points + n_ic_points : n_bc1_points + n_ic_points + n_bc2_points] = 0

# 支配方程式を満たすべき時空間ポイント
Nc = 10000

# LHS for collocation points
engine = qmc.LatinHypercube(d=2)
data = engine.random(n=Nc)
# set x values between -1. and +1.
data[:, 1] = 2*(data[:, 1]-0.5)

# change names
t_c = np.expand_dims(data[:, 0], axis=1)
x_c = np.expand_dims(data[:, 1], axis=1)

t_c = np.vstack([t_c, t_d])
x_c = np.vstack([x_c, x_d])

# データポイントの可視化
plt.figure(figsize=(8, 3))
plt.scatter(t_c, x_c, marker="x", c="k")
plt.xlabel("t")
plt.ylabel("x")
plt.title("Data points (BCs & IC)")


pinns = PINNs(t_d, t_c, x_d, x_c, y_d, 0.07)
pinns.train()

#予測結果の可視化

x_star = np.linspace(-1.0 , 1.0 , 100)
t_star = np.linspace(0 , 1.0 , 100)
X, T = np.meshgrid(x_star, t_star)

X = X.reshape(-1, 1)
T = T.reshape(-1, 1)
u_pred, _ = pinns.predict(X, T)
u_pred = u_pred.reshape(100,100).T

# コンター図を作成
plt.figure(figsize=(8, 3))
plt.contourf(t_star, x_star, u_pred, 100, cmap='coolwarm')
plt.colorbar()

# 軸ラベルを設定
plt.scatter(t_d, x_d, marker="x", c="k")
plt.xlabel("t")
plt.ylabel("x")
plt.show()