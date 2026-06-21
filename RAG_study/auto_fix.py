import json
import os

# 1. 准确定位到 text2vec_model 内部的 1_Pooling 文件夹
pooling_dir = "D:/RAG_study/text2vec_model/1_Pooling"
pooling_config_path = os.path.join(pooling_dir, "config.json")

# 2. 如果文件夹不存在，帮你自动创建（防止路径有些微差异）
if not os.path.exists(pooling_dir):
    os.makedirs(pooling_dir)
    print(f"已自动创建缺失的文件夹: {pooling_dir}")

# 3. 如果配置文件存在，读取并修改；如果不存在，直接新建一个完整的
if os.path.exists(pooling_config_path):
    with open(pooling_config_path, "r", encoding="utf-8") as f:
        try:
            config = json.load(f)
        except Exception:
            config = {}
    print("重写已存在的 1_Pooling/config.json ...")
else:
    config = {}
    print("正在创建全新的 1_Pooling/config.json ...")

# 4. 强行注入缺失的底层核心校验参数
config["word_embedding_dimension"] = 768
config["embedding_dimension"] = 768
config["pooling_mode_cls_token"] = False
config["pooling_mode_mean_tokens"] = True
config["pooling_mode_max_tokens"] = False
config["pooling_mode_mean_sqrt_len_tokens"] = False

# 5. 保存写回
with open(pooling_config_path, "w", encoding="utf-8") as f:
    json.dump(config, f, indent=2)

print("【成功】Pooling 配置文件已完美修复！")