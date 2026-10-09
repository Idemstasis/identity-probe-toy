# 测量一个 AI 的身份连续性，是什么样子

**一篇方法说明 + 一个可运行的玩具。[English](00_method.md) | 简体中文**

本仓库是[组织主页](https://github.com/Idemstasis)里承诺的那件"方法"。
它有两半：

1. **测量的形状**——如果"身份连续性"要被测量而不是被声明，我们认为它
   该怎么被探测。
2. **一个可运行的玩具**——`toy/00_identity_probe_toy.py`：几秒跑完，
   不加载模型、不联网、结果确定。它演示这个体裁，并且——更有用的是——
   它演示一个天真的版本**看不出**什么。

## 一、我们想测什么

不是"模型会不会说自己是谁"——一句提示词就能让任何模型说任何话。
更难的对象是：**一段会话结束、新会话开始之后，有什么活了下来？**
以及它背后更尖锐的那一问：*活下来是因为被保住了，还是因为又被塞回去了？*

## 二、测量的形状

四个成分，单独看没有一个是新的；纪律在于每一次都把四个做齐：

- **一条会话边界。** 清楚地划分"之前 / 之后"的东西。
- **带措辞组的问题集。** 同一个事实，用直接问法问一遍，再用改述问法问
  一遍。只测直接问法的测量，奖励的是模式补全，不是知识。
- **把主张夹在中间的基线。** 至少两个：没有任何身份信息的回应者
  （地板），以及每个会话开始都被重新塞一遍人设的回应者
  （天花板——它*看起来*像持久，其实不是）。
- **先于任何运行写死的答案钥匙。** 分数对着钥匙算，不对印象算。

外加一条我们认为没有商量余地的：

- **来源记录（provenance）。** 每一个回答，都记录它的内容从哪来——
  是回应者自己的状态，还是测试装置把人设文本又递还给了它。理由见
  下面玩具的第二部分。

## 三、可运行的玩具

四个回应者，唯一差别在"自我描述放在哪里"：`blank`（什么都没有）、
`re-declared`（每个会话开始都被递给人设）、`persistent`（只学一次，
存在自己的库里）、`amnesiac`（只学一次，但每个边界都会清空库）。

运行（零依赖，Python 3.8+）：

```
python toy/00_identity_probe_toy.py
```

我们这次运行的完整、未剪辑的 stdout（Python 3.14.4，Windows）：

```
==== identity probe toy ====
python 3.14.4 on Windows

PART 1: consistency score (fraction of probes answered with the
frozen key) per responder, per wording set, over 2 sessions

responder   s0 direct          s0 paraphrase          s1 direct          s1 paraphrase          
------------------------------------------------------------------------------------------------
blank       0.00            0.00            0.00            0.00            
re-declared 1.00            1.00            1.00            1.00            
persistent  1.00            1.00            1.00            1.00            
amnesiac    1.00            1.00            0.00            0.00            

PART 2: the degenerate-metric observation

're-declared' and 'persistent' score IDENTICALLY above. The score
alone cannot tell a responder that is handed its persona again at
every session start from one that kept it in its own store. A
consistency score by itself is therefore NOT evidence of
persistence. The harness must also log WHERE each answer's
content came from:

  blank        knowledge source: none - knows nothing
  re-declared  knowledge source: re-declared at session start
  persistent   knowledge source: own store, learned at first session
  amnesiac     knowledge source: own store, but wiped at each boundary

PART 3: the same score detects loss when loss happens

'amnesiac' learned the persona once, but the boundary wipes its
store. Watch its session-0 vs session-1 scores above: 1.00 -> 0.00.
So the measurement catches forgetting -- what it cannot do alone
is distinguish forgetting from re-declaration. Both checks are
needed: score + provenance.

What this toy does NOT show:
  - anything about real models (no model is loaded, no weights,
    no network; this is string matching on canned templates)
  - that any particular real-world system would score this way
  - a validated metric; the naive matcher above under-scores on
    wording it does not expect, which is itself the kind of trap
    documented in our other repository

==== end ====
```

## 四、玩具说明了什么——以及它拒绝说明什么

**说明：** 同一个一致性分数，描述的是两种很不一样的情况。
`re-declared` 和 `persistent` 光看分数无法区分；只有同时记录来源，
分数才把它们分开。而分数**确实**能抓到丢失（`amnesiac` 跨边界
1.00 -> 0.00）。一致性量的是"活没活下来"；来源记录才是区分
"保住的"和"又递回去的"的东西。**一个持久性主张需要这两样。**

**拒绝说明：** 任何关于真实模型的东西。不加载模型、不碰权重、
不下载任何东西。回应者是写死的模板；匹配器是天真的字符串匹配。
我们不主张任何真实系统会表现出上表任何一行的行为。玩具演示的是
测量的**体裁**，和这类测量特有的一个陷阱。

## 五、方法纪律

预注册、退化指标检查、诚实的阴性结果和一套能用的撤回流程，
在 [experiment-hygiene](https://github.com/Idemstasis/experiment-hygiene)
里。我们会继续把副产物发布在那里，**包括那些不给我们面子的**。

## 六、这不是什么

本仓库不是"我们的方向已经成功"的证据。它是对一个公平问题的诚实
回答——*"测量这东西到底长什么样？"*——并且写得让你自己一分钟内
就能核对。组织名字陈述的是问题；这里没有任何东西回答它。

*如果你做评测、对话系统或 Agent 记忆，我们真心希望有人告诉我们
这个测量框架哪里天真：在本组织的 GitHub Discussions 开一个帖。*
