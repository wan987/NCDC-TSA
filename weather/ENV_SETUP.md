# Weather 项目环境使用说明

## 1. 环境位置
- Conda 环境名称：`weather-ncdc`
- Conda 默认路径：`C:\anaconda3\envs\weather-ncdc`
  > 如果安装在其它路径，可在 Anaconda Prompt 中运行 `conda info --envs` 查看实际位置。

## 2. 创建环境（推荐）
在 **Anaconda Prompt** 或任何已运行 `conda init` 的终端中依次执行：
```bash
conda create -n weather-ncdc python=3.9 -y --solver=classic
conda activate weather-ncdc
pip install Django "pandas>=1.5.0" "numpy>=1.24.0"
pip install "SQLAlchemy>=2.0.0" "PyMySQL>=1.0.0"
```

## 3. 激活环境
- 在已初始化 conda 的终端中：
  ```bash
  conda activate weather-ncdc
  ```
- 如果未运行 `conda init`，也可以直接执行：
  ```bash
  C:\anaconda3\envs\weather-ncdc\Scripts\activate.bat
  ```

## 4. 启动项目
确保环境已激活，然后在项目根目录执行：
```bash
python manage.py runserver
```

## 5. 常见问题
- **提示运行 `conda init`**：打开 “Anaconda Prompt” 执行一次 `conda init cmd.exe`，关闭重开终端即可。
- **找不到环境目录**：确认路径 `C:\anaconda3\envs\weather-ncdc` 是否存在，若不存在请重新执行创建步骤。

## 6. 其它说明
- 运行 `pip list` 可查看已安装包。
- 运行 `conda deactivate` 可退出环境。


