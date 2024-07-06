#
# import tkinter as tk
# from tkinter import ttk
# from PIL import Image, ImageTk
#
#
# class FRCMApp(tk.Tk):
#     def __init__(self):
#         super().__init__()
#         self.title("Prediction of shear capacity and failure mode")
#         self.geometry("500x750")
#
#         self.grid_columnconfigure(0, minsize=10)  # 将第0列的最小宽度设置为100像素
#         self.grid_rowconfigure(0, minsize=50)  # 将第0行的最小高度设置为50像素
#
#         # 标题部分
#         title_frame = tk.Frame(self)
#         title_frame.grid(row=0, column=0, columnspan=1, sticky="nsew")
#
#         title_label1 = tk.Label(title_frame, text="Prediction of shear capacity and failure mode", font=("Arial", 14),
#                                 fg="red")
#         title_label1.pack()
#
#         title_label2 = tk.Label(title_frame, text="of RC beams strengthened with FRCM", font=("Arial", 14), fg="red")
#         title_label2.pack()
#
#         # 图片部分
#         img = Image.open("FRCM1.png")
#         img = img.resize((400, 100), Image.ANTIALIAS)
#         img = ImageTk.PhotoImage(img)
#
#         image_label = tk.Label(self, image=img)
#         image_label.image = img
#         image_label.grid(row=1, column=0, columnspan=1, sticky="nsew")
#
#         # 添加横线
#         tk.Label(self, text="─" * 55).grid(row=2, column=0, columnspan=2)
#
#         # 参数输入部分
#         params_frame = tk.Frame(self)
#         params_frame.grid(row=3, column=0, columnspan=1, padx=10, pady=5, sticky="n")
#
#         # 参数标签列表
#         param_labels = [
#             "Width of beam section (bw/mm)",
#             "Shear span (a/mm)",
#             "Sectional effective height (d/mm)",
#             "Shear span ratio (a/d)",
#             "Compressive strength of concrete (fc/MPa)",
#             "Reinforcement ratio of steel stirrups (ρw)",
#             "Yield strength of steel (fw/MPa)",
#             "Reinforcement ratio of longitudinal steel (ρl)",
#             "Yield strength of longitudinal steel (fl/MPa)",
#             "Shape of beam"
#         ]
#
#         # 创建输入框
#         self.entries = {}
#         for idx, text in enumerate(param_labels):
#             label = tk.Label(params_frame, text=text, font=("Arial", 10))
#             label.grid(row=idx, column=0, sticky="w", pady=1)  # 减少 pady
#             entry = tk.Entry(params_frame, font=("Arial", 10))
#             entry.grid(row=idx, column=1, pady=1, sticky="e")  # 减少 pady, 并使输入框横向拉伸
#             self.entries[text] = entry
#
#         # 梁的形状选项
#         shape_frame = tk.Frame(params_frame)
#         shape_frame.grid(row=9, column=1, pady=1, sticky="ew")  # 减少 pady 并使框横向拉伸
#         self.shape_var = tk.StringVar()
#         self.shape_var.set("T_SHAPE")
#         tk.Radiobutton(shape_frame, text="R_SHAPE", variable=self.shape_var, value="T_SHAPE", font=("Arial", 10)).pack(
#             side=tk.LEFT)
#         tk.Radiobutton(shape_frame, text="T_SHAPE", variable=self.shape_var, value="R_SHAPE", font=("Arial", 10)).pack(
#             side=tk.LEFT)
#
#         # FRCM部分标签
#         frcm_label = tk.Label(self, text="FRCM part", font=("Arial", 12), fg="purple")
#         frcm_label.grid(row=4, column=0, columnspan=1, pady=5)
#
#         # FRCM部分输入框

#         frcm_frame = tk.Frame(self)
#         frcm_frame.grid(row=5, column=0, columnspan=1, padx=10, pady=5, sticky="n")
#
#         # 新增的输入框
#         additional_labels = [
#             "Cementitious matrix compressive strength (fm/MPa)",
#             "Prestressing force (pf)",
#             "Elastic modulus of FRCM (Ef)",
#             "Strain in FRCM (strain)"
#         ]
#         for idx, text in enumerate(additional_labels):
#             label = tk.Label(frcm_frame, text=text, font=("Arial", 10))
#             label.grid(row=idx, column=0, sticky="w", pady=1)  # 减少 pady
#             entry = tk.Entry(frcm_frame, font=("Arial", 10))
#             entry.grid(row=idx, column=1, pady=1, sticky="e")  # 减少 pady, 并使输入框横向拉伸
#             self.entries[text] = entry
#
#         # 新增的选项按钮
#         options_frame = tk.Frame(self)
#         options_frame.grid(row=6, column=0, columnspan=1,pady=1, sticky="ew")
#
#         option_labels = ["ANCHOR", "DC", "Failure mode"]
#         self.option_vars = {}
#         for idx, text in enumerate(option_labels):
#             label = tk.Label(options_frame, text=text, font=("Arial", 10))
#             label.grid(row=idx, column=0, sticky="w", pady=1)  # 减少 pady
#             var = tk.StringVar()
#             var.set("a")
#             frame = tk.Frame(options_frame)
#             frame.grid(row=idx, column=1, pady=1, sticky="ew")  # 减少 pady 并使框横向拉伸
#             tk.Radiobutton(frame, text="a", variable=var, value="a", font=("Arial", 10)).pack(side=tk.LEFT)
#             tk.Radiobutton(frame, text="c", variable=var, value="b", font=("Arial", 10)).pack(side=tk.LEFT)
#             self.option_vars[text] = var
#
#         # self.grid_columnconfigure(0, minsize=5)
#         # 计算按钮
#         calc_button = tk.Button(self, text="Calculate", font=("Arial", 12), command=self.calculate)
#         calc_button.grid(row=7, column=0, columnspan=2, pady=5, sticky="nsew")
#
#         # 结果显示部分
#         result_frame = tk.Frame(self)
#         result_frame.grid(row=8, column=0, columnspan=2, padx=10, pady=5)
#         tk.Label(result_frame, text="Shear Strength", font=("Arial", 12), fg="red").grid(row=0, column=0, pady=5)
#         self.shear_strength_label = tk.Label(result_frame, text="", font=("Arial", 10), bg="white", width=30)
#         self.shear_strength_label.grid(row=0, column=1, pady=5)
#
#     def calculate(self):
#         product = 1  # 初始化乘积为1
#         for key in self.entries:
#             try:
#                 product *= float(self.entries[key].get())  # 将输入值转换为浮点数并计算乘积
#             except ValueError:
#                 pass  # 忽略无效输入
#
#         for key in self.option_vars:
#             try:
#                 product *= 1 if self.option_vars[key].get() == 'a' else 2  # 'a' 对应乘1，'b' 对应乘2
#             except ValueError:
#                 pass
#
#         self.shear_strength_label.config(text=str(product))  # 将结果显示在shear_strength_label中
#
#
# # 主程序入口
# if __name__ == "__main__":
#     app = FRCMApp()
#     app.mainloop()

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk


class FRCMApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Prediction of shear capacity and failure mode")
        self.geometry("500x750")

        # self.grid_columnconfigure(0, minsize=500)  # 将第0列的最小宽度设置为10像素
        # self.grid_rowconfigure(0, minsize=50)  # 将第0行的最小高度设置为50像素
        self.grid_columnconfigure(0, minsize=200, weight=1)
        self.grid_columnconfigure(1, minsize=100, weight=1)
        # self.grid_columnconfigure(2, minsize=100, weight=1)
        # self.grid_columnconfigure(3, minsize=100, weight=1)

        # 标题部分
        title_frame = tk.Frame(self)
        title_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")

        title_label1 = tk.Label(title_frame, text="Prediction of shear capacity and failure mode", font=("Arial", 14),
                                fg="red")
        title_label1.pack()

        title_label2 = tk.Label(title_frame, text="of RC beams strengthened with FRCM", font=("Arial", 14), fg="red")
        title_label2.pack()

        # 图片部分
        img = Image.open("FRCM1.png")
        # img = img.resize((400, 100), Image.ANTIALIAS)
        img = img.resize((400, 100), Image.Resampling.LANCZOS)
        img = ImageTk.PhotoImage(img)

        image_label = tk.Label(self, image=img)
        image_label.image = img
        image_label.grid(row=1, column=0, columnspan=2, sticky="nsew")

        # 添加横线
        tk.Label(self, text="─" * 55).grid(row=2, column=0, columnspan=2)

        # 参数输入部分
        params_frame = tk.Frame(self)
        params_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="n")

        # 参数标签列表
        param_labels = [
            "Width of beam section (bw/mm)",
            "Shear span (a/mm)",
            "Sectional effective height (d/mm)",
            "Shear span ratio (a/d)",
            "Compressive strength of concrete (fc/MPa)",
            "Reinforcement ratio of steel stirrups (ρw)",
            "Yield strength of steel (fw/MPa)",
            "Reinforcement ratio of longitudinal steel (ρl)",
            "Yield strength of longitudinal steel (fl/MPa)",
            "Shape of beam"
        ]

        # 创建输入框
        self.entries = {}
        for idx, text in enumerate(param_labels):
            label = tk.Label(params_frame, text=text, font=("Arial", 10))
            label.grid(row=idx, column=0, sticky="w", pady=1)  # 减少 pady
            entry = tk.Entry(params_frame, font=("Arial", 10))
            entry.grid(row=idx, column=1, pady=1, sticky="e")  # 减少 pady, 并使输入框横向拉伸
            self.entries[text] = entry

        # 梁的形状选项
        shape_frame = tk.Frame(params_frame)
        shape_frame.grid(row=9, column=1, pady=1, sticky="ew")  # 减少 pady 并使框横向拉伸
        self.shape_var = tk.StringVar()
        self.shape_var.set("T_SHAPE")
        tk.Radiobutton(shape_frame, text="R_SHAPE", variable=self.shape_var, value="T_SHAPE", font=("Arial", 10)).pack(
            side=tk.LEFT)
        tk.Radiobutton(shape_frame, text="T_SHAPE", variable=self.shape_var, value="R_SHAPE", font=("Arial", 10)).pack(
            side=tk.LEFT)

        # FRCM部分标签
        frcm_label = tk.Label(self, text="FRCM part", font=("Arial", 12), fg="purple")
        frcm_label.grid(row=4, column=0, columnspan=2, pady=5)

        # FRCM部分输入框
        frcm_frame = tk.Frame(self)
        frcm_frame.grid(row=5, column=0, columnspan=2, padx=10, pady=5, sticky="n")

        # 新增的输入框
        additional_labels = [
            "Cementitious matrix compressive strength (fm/MPa)",
            "Prestressing force (pf)",
            "Elastic modulus of FRCM (Ef)",
            "Strain in FRCM (strain)"
        ]
        for idx, text in enumerate(additional_labels):
            label = tk.Label(frcm_frame, text=text, font=("Arial", 10))
            label.grid(row=idx, column=0, sticky="w", pady=1)  # 减少 pady
            entry = tk.Entry(frcm_frame, font=("Arial", 10))
            entry.grid(row=idx, column=1, pady=1, sticky="e")  # 减少 pady, 并使输入框横向拉伸
            self.entries[text] = entry

        # 新增的选项按钮
        options_frame = tk.Frame(self)
        options_frame.grid(row=6, column=0, columnspan=2, padx=(25, 25), pady=10, sticky='we')
        # options_frame.grid(row=6, column=0, columnspan=2, pady=10, sticky='we')
        options_frame.grid_columnconfigure(0, minsize=1, weight=1)
        options_frame.grid_columnconfigure(1, minsize=1, weight=1)
        option_labels = ["ANCHOR", "DC", "Failure mode"]
        self.option_vars = {}
        option_values = [["yes", "no"], ["dc", "ndc"], ["Fexlure", "No Debond", "Debond"]]

        for idx, (text, values) in enumerate(zip(option_labels, option_values)):
            label = tk.Label(options_frame, text=text, font=("Arial", 10))
            label.grid(row=idx, column=0, sticky="w", pady=1)  # 减少 pady
            var = tk.StringVar()
            var.set(values[0])
            frame = tk.Frame(options_frame)
            frame.grid(row=idx, column=2, pady=1, sticky="w")  # 减少 pady 并使框横向拉伸
            for value in values:
                button = tk.Radiobutton(frame, pady=1,text=value, variable=var, value=value, font=("Arial", 10))
                button.pack(
                    side=tk.RIGHT)
            self.option_vars[text] = var

        # shape_frame = tk.Frame(params_frame)
        # shape_frame.grid(row=9, column=1, pady=5)
        # self.shape_var = tk.StringVar()
        # self.shape_var.set("T_SHAPE")
        # tk.Radiobutton(shape_frame, text="T_SHAPE", variable=self.shape_var, value="T_SHAPE").pack(side=tk.LEFT)
        # tk.Radiobutton(shape_frame, text="R_SHAPE", variable=self.shape_var, value="R_SHAPE").pack(side=tk.LEFT)

        # 计算按钮
        calc_button = tk.Button(self, text="Calculate", font=("Arial", 12), command=self.calculate)
        calc_button.grid(row=7, column=0, columnspan=2, pady=5, sticky="nsew")

        # 结果显示部分
        result_frame = tk.Frame(self)
        result_frame.grid(row=8, column=0, columnspan=2, padx=10, pady=5)
        tk.Label(result_frame, text="Shear Strength", font=("Arial", 12), fg="red").grid(row=0, column=0, pady=5)
        self.shear_strength_label = tk.Label(result_frame, text="", font=("Arial", 10), bg="white", width=30)
        self.shear_strength_label.grid(row=0, column=1, pady=5)

    def calculate(self):
        product = 1  # 初始化乘积为1
        for key in self.entries:
            try:
                product *= float(self.entries[key].get())  # 将输入值转换为浮点数并计算乘积
            except ValueError:
                pass  # 忽略无效输入

        for key in self.option_vars:
            try:
                product *= 1 if self.option_vars[key].get() in ['yes', 'dc',
                                                                'F'] else 2  # 'yes', 'dc', 'F' 对应乘1，其他选项对应乘2
            except ValueError:
                pass

        self.shear_strength_label.config(text=str(product))  # 将结果显示在shear_strength_label中


# 主程序入口
if __name__ == "__main__":
    app = FRCMApp()
    app.mainloop()
