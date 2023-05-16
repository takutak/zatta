from sklearn.datasets import load_iris
import matplotlib.pyplot as plt
iris = load_iris()
x_org, y_org = iris.data, iris.target

x_setosa = x_org[y_org == 0]
x_versicolor = x_org[y_org == 1]
x_virginica = x_org[y_org == 2]

plt.scatter(x_setosa[:, 0], x_setosa[:, 1], marker = 'x', c = 'red', label = 'setosa')
plt.scatter(x_versicolor[:, 0], x_versicolor[:, 1], marker = 'o', c = 'blue', label = 'versicolor')
plt.scatter(x_virginica[:, 0], x_virginica[:, 1], marker = ',',c = 'green', label = 'virginica' )

plt.xlabel('sepal length [cm]')
plt.ylabel('sepal width [cm]')

plt.legend(fontsize = 12)
plt.title('iris sepal data')

plt.show()

plt.scatter(x_setosa[:, 2], x_setosa[:, 3], marker = 'x', c = 'red', label = 'setosa')
plt.scatter(x_versicolor[:, 2], x_versicolor[:, 3], marker = 'o', c = 'blue', label = 'versicolor')
plt.scatter(x_virginica[:, 2], x_virginica[:, 3], marker = ',',c = 'green', label = 'virginica' )

plt.xlabel('petal length [cm]')
plt.ylabel('petal width [cm]')

plt.legend(fontsize = 12)
plt.title('iris petal data')

plt.show()