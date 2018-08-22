# DeeCamp-13
## qqbot的使用
- 训练好模型
- 运行主目录下的run.py
- 运行主目录下的test_port2.py
- 通过ftp或者什么办法打开z主目录下的v.jpg,用qq扫这个二维码
- 发送!+你想说的话（没有加号）给上面扫二维码的qq号
- test_port2.py中的type==0时使用深度学习模型，type==1时使用检索模型
## 深度学习模型的使用
- 参照本模型大部分代码来源</url>https://github.com/qhduan/just_another_seq2seq<url>做词向量
- 将清洗好的数据（文件名为zhihu.csv，格式为每一行为问句+','+答句）复制到chatbot_cut内
- 运行chatbot_cut/my_e_csv.py读入数据
- 运行chatbot_cut/train_anti.py训练模型
- 运行chatbot_cut/test_anti.py测试模型
- 测试的输入文件均位于chatbot_cut/test_input.txt,输出文件位于chatbot_cut/test_output.txt
## 传统检索模型的使用
- 将清洗好的数据（文件名为zhihu.csv，格式为每一行为问句+','+答句）复制到chatbot_cut内
- 运行generateQA.py处理数据
- 运行runModel.py训练模型，测试模型
- 测试的输入文件均位于dataset/test_input.txt,输出文件位于dataset/test_output.txt
## todolist
- ~~修正多层rnn的写法~~（发现不需要修正）
- ~~发现qqbot本地可用，linux服务器上出bug了，待修复~~(已修复）
- 调整各种参数，佛系炼丹
- ~~修复长度惩罚的bug~~（已修复）
- ~~大幅优化qqbot的速度~~（已修复）
- ~~验证qqbot在服务器运行效果~~（已成功）
