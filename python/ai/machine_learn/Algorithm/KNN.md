# KNN算法

1. ### 作用

   ```
   分类算法
   预测一个数据的分类
   ```

2. ### 原理

   ```
   KNN 的原理就是当预测一个新的值 x 的时候，根据它距离最近的 K 个点是什么类别来判断 x 属于哪个类别
   ```

   ![image-20240429111856808](W:\note\python\ai\machine_learn\Algorithm\KNN\image-20240429111856808.png)

   ```
   图中绿色的点就是我们要预测的那个点，假设 K=3。那么 KNN 算法就会找到与它距离最近的三个点（这里用圆圈把它圈起来了），看看哪种类别多一些，比如这个例子中是蓝色三角形多一些，新来的绿色点就归类到蓝三角了。
   ```

3. ### 过程

   - #### 计算距离

     1. ##### 欧式距离

        ![image-20240429112203555](W:\note\python\ai\machine_learn\Algorithm\KNN\image-20240429112203555.png)

     2. ##### 曼哈顿距离

        d(i,j)=|X1-X2|+|Y1-Y2|.

   - #### k值选择

     选择邻居点个数

4. #### 算法实现

   ```python
   from sklearn.datasets import  load_iris
   from sklearn.model_selection import  train_test_split
   from sklearn.preprocessing import StandardScaler
   from sklearn.neighbors import KNeighborsClassifier
   
   def knn_iris():
       # 获取数据
       iris = load_iris()
       # 数据集划分
       x_train, x_test, y_train, y_test = train_test_split(iris.data, iris.target,
                                                        random_state=6)  # 训练集数据，测试集数据，训练集标签应变量，数据集标签
       # print("y_train\n,y_test:\n", x_train,y_test)
       # 特征工程 - 标准化
       transfer = StandardScaler()
       x_train = transfer.fit_transform(x_train)
       x_test = transfer.transform(x_test)
       # 算法预估 KNN
       estimator = KNeighborsClassifier(n_neighbors=8)
       estimator.fit(x_train, y_train)
       # 模型评估
       y_predict = estimator.predict(x_test)
       print("y_predice:\n", y_predict)
       print("直接对比真实值：\n", y_test == y_predict)
   
       score = estimator.score(x_test, y_test)
       print("准确率为:\n", score)
   
   
   if __name__ == '__main__':
       knn_iris()
   ```

   

   #### 

   

   

   