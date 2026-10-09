# identity-probe-toy

**测量一个 AI 的身份连续性，是什么样子——一篇方法说明 + 一个可运行的
玩具。[English](README.md) | 简体中文**

这是[组织主页](https://github.com/Idemstasis)里承诺的那件"方法"：
如果"身份连续性"要被**测量而不是被声明**，我们认为它该怎么被探测——
外加一个一秒内能跑完的玩具（纯标准库、不加载模型、不联网、结果确定），
它演示这个体裁，以及它的一个典型陷阱：**光有一致性分数，分不清
"保住的"和"又递回去的"；还得加上来源记录（provenance）。**

- **[docs/00_method.zh-CN.md](docs/00_method.zh-CN.md)** — 方法说明
  （[English](docs/00_method.md)）
- **[toy/00_identity_probe_toy.py](toy/00_identity_probe_toy.py)** —
  可运行的玩具；完整未剪辑的输出附在方法说明里

零第三方依赖。Python 3.8+。这里的一切都是对一种测量**体裁**的演示，
不是关于任何真实系统的证据——说明里写明了玩具拒绝展示什么。

如果你做评测、对话系统或 Agent 记忆，我们真心希望有人告诉我们这个
框架哪里天真：在**本组织的 GitHub Discussions** 开一个帖。

*名字陈述的是问题，不是答案。*
