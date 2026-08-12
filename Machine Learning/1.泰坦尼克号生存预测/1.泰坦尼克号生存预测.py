import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 设置 DataFrame 表格打印显示格式
pd.set_option('display.max_columns', None)  # 设置最大显示列数：None代表全部列都显示
pd.set_option('display.width', 2000)        # 设置输出表格宽度，数值调大，单位字符
pd.set_option('display.max_colwidth', 30)   # 每列最大字符长度

# 获取泰坦尼克号数据
url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
df = pd.read_csv(url)

# 打印一些基本信息看看
print(f"数据前 5 项预览：\n{df.head()}")
print(f"\n数据集形状：", df.shape)
print(f"\n数据类型与缺失值情况：")
print(df.info())

# 数值列统计描述
print("==== 数值特征统计描述 ====")
print(df.describe())

# 统计每列缺失值数量、缺失占比
print("\n==== 缺失值统计 ====")
missing = pd.DataFrame({
    "缺失数量": df.isnull().sum(),
    "缺失占比(%)": round(df.isnull().sum() / len(df) *100, 2)
})
print(missing)

plt.figure(figsize=(8, 5))
# Pclass:客舱等级 1一等，2二等，3三等
survive_pclass = df.groupby("Pclass")["Survived"].mean()
survive_pclass.plot(kind="bar", color=["#87CEEB", "#90EE90", "#FFA07A"])
plt.title("不同客舱等级的生存率")
plt.ylabel("生存率")
plt.xlabel("客舱等级Pclass")
plt.xticks([0, 1, 2], ["一等舱", "二等舱", "三等舱"], rotation=0)
plt.show()

plt.figure(figsize=(7, 4))
survive_sex = df.groupby("Sex")["Survived"].mean()
survive_sex.plot(kind="bar", color=["lightcoral", "lightblue"])
plt.title("不同性别生存率")
plt.ylabel("生存率")
plt.xlabel("性别")
plt.xticks([0, 1], ["女性", "男性"], rotation=0)
plt.show()

# 1. 删除Cabin列，缺失太多无利用价值
df = df.drop("Cabin", axis=1)

# 2. Age用中位数填充
df["Age"] = df["Age"].fillna(df["Age"].median())

# 3. Embarked用众数填充
df["Embarked"] = df["Embarked"].fillna(df["Embarked"].mode()[0])

# 4. 特征衍生：新增家庭大小特征 FamilySize = SibSp + Parch +1，把 SibSp 和 Parch 合并，重新跑模型，看指标是否提升（可合并也可不合并）
"""
合并之前：(逻辑回归, 随机森林) accuracy: (80.45%, 81.56%)
合并之后：(逻辑回归, 随机森林) accuracy: (80.45%, 81.01%)
"""
df["FamilySize"] = df["SibSp"] + df["Parch"] + 1

# 检查处理后是否还存在缺失
print("处理完缺失后的缺失统计：")
print(df.isnull().sum())

# 1 删除无用列
drop_cols = ["PassengerId", "Name", "Ticket"]
df = df.drop(columns=drop_cols)

# 2 One‑Hot独热编码，处理文本类别特征
df = pd.get_dummies(df, columns=["Sex", "Embarked"], drop_first=True)

print("处理完特征之后的列名：")
print(df.columns.tolist())
print("\n查看前3行数据: ")
print(df.head(3))

# X：全部特征，去掉目标列 Survived
X = df.drop("Survived", axis=1)
# y：预测标签，是否存活
y = df["Survived"]

# 划分训练集、测试集
# test_size=0.2: 测试集占20%
# stratify=y: 分层抽样，保证两集合存活比例一致
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

print(f"训练集大小 X_train:{X_train.shape}, y_train:{y_train.shape}")
print(f"测试集大小 X_test:{X_test.shape}, y_test:{y_test.shape}")

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

lr_model = LogisticRegression(max_iter=200)
lr_model.fit(X_train_scaled, y_train)

y_pred = lr_model.predict(X_test_scaled)

print("========逻辑回归（标准化后）模型评估========")
print(f"测试集准确率 accuracy: {accuracy_score(y_test, y_pred)*100:.2f}%")
print("\n混淆矩阵：")
print(confusion_matrix(y_test, y_pred))
print("\n分类报告：")
print(classification_report(y_test, y_pred))

rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

y_pred_rf = rf_model.predict(X_test)

print("======== 随机森林模型评估 ========")
print(f"测试集准确率 accuracy: {accuracy_score(y_test, y_pred_rf)*100:.2f}%")
print("\n混淆矩阵：")
print(confusion_matrix(y_test, y_pred_rf))
print("\n分类报告：")
print(classification_report(y_test, y_pred_rf))

# 输出特征重要性
print("\n==== 特征重要性（数值越大对生存预测影响越大）====")
feature_importance = pd.DataFrame({
    "feature":X_train.columns,
    "importance":rf_model.feature_importances_
}).sort_values("importance", ascending=False)

print(feature_importance)

# 获取测试集预测结果
test_result = X_test.copy()
test_result["真实_Survived"] = y_test
test_result["预测_Survived"] = y_pred_rf

# 输出csv文件，保存到你当前VSCode工作目录
test_result.to_csv("1.titanic_test_predict.csv", index=False, encoding="utf_8_sig")
print("1.预测文件已保存：titanic_test_predict.csv")

# 1、设置要搜索的参数字典
param_grid = {
    "n_estimators": [50, 100, 150], # 森林中决策树棵数
    "max_depth": [3, 5, 7, 9, 11]   # 树最大深度，重点！
}

# 2、基础随机森林模型
rf = RandomForestClassifier(random_state=42)

# 3、网格搜索，5折交叉验证
grid_search = GridSearchCV(
    estimator=rf,
    param_grid=param_grid,
    cv=5,                # 5折交叉验证
    scoring="accuracy",  # 评估指标用准确率
    n_jobs=-1            # n_jobs=-1 使用电脑全部CPU，加速搜索
)

# ⚠️注意：fit只用训练集！绝对不能把X_test放进来！
grid_search.fit(X_train, y_train)

# 输出最优参数、最优交叉验证得分
print("✅网格搜索得到的最优参数：")
print(grid_search.best_params_)
print(f"\n训练集上5折交叉验证最优准确率：{grid_search.best_score_*100:.2f}%")

# 获取调参完毕的最优模型
best_rf = grid_search.best_estimator_

# 使用最优模型，在【从未见过的测试集】上评估！
y_pred_best = best_rf.predict(X_test)

print("\n======== 调参后最优模型，测试集评估 ========")
print(f"测试集准确率：{accuracy_score(y_test, y_pred_best)*100:.2f}%")
print(classification_report(y_test, y_pred_best))

feature_importance = pd.DataFrame({
    "feature":X_train.columns,
    "importance":best_rf.feature_importances_
}).sort_values("importance", ascending=False)

print("\n调参后特征重要性：")
print(feature_importance)