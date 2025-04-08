# 📚 IntelliRewrite：AI 智能文本重写工具
 [![许可证](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE) [![星标数](https://img.shields.io/github/stars/Monthlyaway/intellirewrite.svg)](https://github.com/Monthlyaway/intellirewrite/stargazers) [![问题反馈](https://img.shields.io/github/issues/Monthlyaway/intellirewrite.svg)](https://github.com/Monthlyaway/intellirewrite/issues)
[English](README.md) | [中文](README.zh-CN.md)
## 🚀 项目简介
IntelliRewrite 是一款强大的命令行工具，通过大语言模型帮助学生、研究人员和写作者在保留原意的前提下优化文本内容。它特别适用于：
- 📝 重写笔记与论文
- 🔄 提升文本清晰度与行文流畅度
- 📚 分段处理长篇文档
- 🌐 通过可配置接口支持多 AI 平台
### ✨ 核心功能
- **任务管理**：基于队列的多任务处理系统
- **智能分块**：将长文档分割为易处理片段
- **记忆上下文**：可配置的记忆功能保持分块间连贯性
- **灵活 API 支持**：兼容 OpenAI API
- **进度追踪**：实时显示详细处理进度
- **断点续传**：意外中断后可继续未完成任务
### 🎓 学生专用设计
专为学术场景优化：
- **学习笔记**：重塑笔记结构提升理解
- **论文优化**：保持原意的质量升级
- **研究文献**：学术长文档分段处理
- **语言学习**：通过 AI 改写观察语言表达技巧
### 🌍 多平台 API 支持
兼容任意 OpenAI 格式 API：
- **自定义接口**：自由配置 API 基地址
- **多模型支持**：兼容 OpenAI、DeepSeek 等多个平台，听说 Deepseek-R1 具备推理能力？当然！IntelliRewrite 完美适配。
## 🔄 工作流程演示
### 🎭 实际应用场景
假设你的线性代数教授布置了关于"特征值与特征向量"的第三、四章——就是让矩阵突然拥有"个性"、向量获得"特殊待遇"的那部分内容。
你：*盯着教材* "等等，他们是怎么从第二步直接跳到第七步的？我漏看了四页吗？"
**IntelliRewrite 来拯救：**
1. **提取转换**
   使用 [MinerU](https://github.com/opendatalab/MinerU) 将 PDF 转为 Markdown
2. **队列添加**
   ```bash
   python -m chapter_rewriter.cli add-task linear_algebra_ch3.md --chunk-size 800
   python -m chapter_rewriter.cli add-task linear_algebra_ch4.md --chunk-size 800
   ```
3. **通宵处理**
   ```bash
   python -m chapter_rewriter.cli process-tasks
   ```
4. **清晨收获**
   打开 `output/linear_algebra_ch3_rewritten.md` 和 `output/linear_algebra_ch4_rewritten.md`，收获展示完整推导过程、解释特征值现实意义的清晰版本！
   再也不见"显然可得..."但实际让人摸不着头脑的跳跃推导！
### 标准处理流程
1. **添加任务**
   将文档加入处理队列：
   ```bash
   python -m chapter_rewriter.cli add-task document1.md
   python -m chapter_rewriter.cli add-task document2.txt
   ```
2. **查看队列**
   查看待处理任务：
   ```bash
   python -m chapter_rewriter.cli list-tasks
   ```
   输出示例：
   ```
   任务ID | 状态     | 进度    | 文件
   ----------------------------------------
   1      | 待处理   | 0%      | document1.md
   2      | 队列中   | 0%      | document2.txt
   ```
3. **启动处理**
   开始 AI 重写：
   ```bash
   python -m chapter_rewriter.cli process-tasks
   ```
   实时进度：
   ```
   处理 document1.md [■■■■□□□□□□] 40%
   当前分块：12/30 (1024 字符)
   ```
输出文件存放于 `output` 文件夹
### 流程特色
- **批量处理**：先添加多个文件再统一处理（方便腾出时间社交）
- **优先级队列**：按添加顺序处理（记得提前充值 API 额度）
- **进度保存**：自动恢复中断任务，任务状态包括：待处理、处理中、已完成、失败。待处理和处理中任务会自动续接
## 🔧 分块大小配置
通过 `--chunk-size` 参数控制分块字符数（非 token 数），优化大语言模型处理效果：
**默认值**：800 字符
### 为何用字符计数？
字符分块策略确保跨语言公平计算：
- 英语：空格是必要分词元素
- 中文：极少使用分词空格
- 混合内容：提供统一度量标准
### Token 估算指南
| 语言        | 字符数       | Token 估值    | 推荐分块大小        |
|-------------|-------------|--------------|--------------------|
| 英语        | 1000        | ~300 tokens  | 1200-1800 字符     |
| 中文        | 1000        | ~600 tokens  | 500-1000 字符      |
| 混合内容    | 1000        | 动态变化       | 800-1200 字符      |
**实现细节：**
1. 分块始终在段落结尾（`\n\n`）处断开
2. 实际分块大小可能浮动
3. 命令行预估帮助避免 API 超额
**配置示例：**
```bash
# 中文主导内容
python -m chapter_rewriter.cli add-task --chunk-size 600 paper.md
# 英文技术文档
python -m chapter_rewriter.cli add-task --chunk-size 1500 thesis.txt
```
---
## 🛠️ 安装指南
### 前置条件
- Python 3.10 或更高
- pip (Python 包管理器)
### 快速安装
```bash
# 克隆仓库
git clone https://github.com/Monthlyaway/intellirewrite.git
cd intellirewrite
# 安装依赖
pip install -r requirements.txt
# 配置环境变量
cp .env.example .env
```
编辑 `.env` 文件配置 API 密钥：
```
API_KEY=你的API密钥
BASE_URL=API基地址
```
## 📖 使用说明
### 基础使用
```bash
# 添加任务到队列
python -m chapter_rewriter.cli add-task input.md
# 处理所有待办任务
python -m chapter_rewriter.cli process-tasks
```
## 📚 支持格式
- **Markdown**：`.md`
- **纯文本**：`.txt`
❌ **PDF**：`.pdf` (需使用 [矿工U](https://github.com/opendatalab/MinerU) 提取为 Markdown)
### 高级选项
```bash
# 自定义分块与记忆窗口
python -m chapter_rewriter.cli add-task --chunk-size 300 --memory-size 3 input.md
# 查看任务列表
python -m chapter_rewriter.cli list-tasks
# 查看任务详情
python -m chapter_rewriter.cli show-task 任务ID
```
获取完整帮助：
```bash
python -m chapter_rewriter.cli --help
python -m chapter_rewriter.cli add-task --help
python -m chapter_rewriter.cli process-tasks --help
python -m chapter_rewriter.cli list-tasks --help
python -m chapter_rewriter.cli show-task --help
```
### 清理缓存
```bash
./clean.bat  # Windows 用户
./clean.sh  # Linux 用户
```
## 🔧 配置说明
### 环境变量
- `API_KEY`：API 密钥
- `BASE_URL`：API 接口地址（可更换地区节点）
- `MAX_TOKENS`：限制模型响应长度，默认 4096。使用 Deepseek-R1 时建议设为 8192
### 任务参数
各任务独立配置（保存在 `task.json` 中）：
- `chunk_size`：文本分块大小
- `memory_size`：上下文记忆窗口数
## 🙏 致谢
- 感谢所有贡献者的支持
- 致敬开源社区的灵感和工具
---
<div align="center">
  <p>为全球学生和写作者用心打造 ❤️</p>
</div>