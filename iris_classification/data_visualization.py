from sklearn.datasets import load_iris
import matplotlib.pyplot as plt
iris = load_iris()
x_org, y_org = iris.data, iris.target

x_setosa = x_org[y_org == 0]
x_versicolor = x_org[y_org == 1]
x_virginica = x_org[y_org == 2]

fig = plt.figure(figsize=(12, 6))
ax1 = fig.add_subplot(1, 2, 1)
ax2 = fig.add_subplot(1, 2, 2)

ax1.scatter(x_setosa[:, 0], x_setosa[:, 1], marker = 'x', c = 'red', label = 'setosa')
ax1.scatter(x_versicolor[:, 0], x_versicolor[:, 1], marker = 'o', c = 'blue', label = 'versicolor')
ax1.scatter(x_virginica[:, 0], x_virginica[:, 1], marker = ',',c = 'green', label = 'virginica' )

ax1.set_xlabel('sepal length [cm]')
ax1.set_ylabel('sepal width [cm]')

ax1.legend(fontsize = 12)
ax1.set_title('iris sepal data')


ax2.scatter(x_setosa[:, 2], x_setosa[:, 3], marker = 'x', c = 'red', label = 'setosa')
ax2.scatter(x_versicolor[:, 2], x_versicolor[:, 3], marker = 'o', c = 'blue', label = 'versicolor')
ax2.scatter(x_virginica[:, 2], x_virginica[:, 3], marker = ',',c = 'green', label = 'virginica' )

ax2.set_xlabel('petal length [cm]')
ax2.set_ylabel('petal width [cm]')

ax2.legend(fontsize = 12)
ax2.set_title('iris petal data')

plt.show()
