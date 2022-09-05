"""
业务逻辑层
retranslateUi附带一部分qt Designer无法完成的部分
"""
from app_ui import Ui_Form
import xgboost as xgb
import numpy as np


FEATURE_NUM = 11  # 使用的指标数目
MIN_VALUE = -999  # 最小值

class My_Ui_Form(Ui_Form):
    def retranslateUi(self, Ui_Form):
        super(My_Ui_Form, self).retranslateUi(Ui_Form)
        # 按钮事件
        self.pushButton.clicked.connect(self.update_ass)

    def update_ass(self):
        # 获取数据
        data = self.get_data(self.tableWidget_content)
        if np.all(np.isnan(data)):
            return
        # 预测
        y_prob = self.ass_prediction(data, 'files/ass_model.model')
        # 显示结果
        self.lineEdit_critical.setText(str("%.2f" % (100 * y_prob)))

    def is_number(self, s):
        try:
            float(s)
            return True
        except ValueError:
            pass

        try:
            import unicodedata
            unicodedata.numeric(s)
            return True
        except (TypeError, ValueError):
            pass

        return False

    def get_data(self, tableWidget_content):
        """
        从表格获取数据
        """
        data = []
        for row in range(FEATURE_NUM):
            obj = tableWidget_content.item(row, 0)
            if obj is None:
                data.append(np.nan)
            else:
                s = obj.text()
                # s是否为空或均为空格
                if len(s) == 0 or s.isspace() is True:
                    data.append(np.nan)
                elif self.is_number(s):
                    data.append(float(s))
                else:
                    data.append(s)
        return data

    def ass_prediction(self, data, modelFilePath):
        # 获取预测模型 model
        model = xgb.Booster()
        model.load_model(modelFilePath)

        # 生成用于模型预测的数据 predict_data
        importance = model.get_score()
        # keys表示所用到的特征，为：'f23','f27',..., 'f94', 特征名称根据训练数据列数从f0开始
        keys = list(importance.keys())
        # 对应于模型特征最大下标需要生成的 predict_data 维度，即需要生成 95 列的数据用于预测
        n_features = int(keys[-1][1:]) + 1
        predict_data = np.zeros(n_features)  # 用于预测的数据
        i = 0
        for key in keys:
            index = int(key[1:])
            predict_data[index] = data[i]
            i += 1

        # 使用模型 model 和数据 predict_data 预测结果
        predict_data = xgb.DMatrix(np.array(predict_data)[np.newaxis, :])
        y_prob = model.predict(predict_data)[0]  # 危重概率
        return y_prob
