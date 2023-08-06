# W-SLN
A python library for W-SLN construction from raw text.

# TODO


- [ ] 疑问句
- [ ] 找openIE数据集测试准确率
- [ ] 加入推理规则
- [ ] 修改
- [ ] 在kg-qa上实验
    1. 证明语言迁移性
    2. embedding的有效性

- [ ] 测试pythonrouge包




<!-- - [ ] ！！！parser解决match pattern中的equal问题  -->
- [ ] resolver中的Tag分配给SLN一个，注意判断symbol的相等性

- [x] Co-occur link
- [ ] 抽取出的链接中的层次性：写模板的时候S的问题
- [ ] 界面完善
- [x] 第一个词、最后一个词如果是名词，就不单独成snippet
- [x] matched_elements都修改了，加入namedtuple，重构extract_links_from_sentence
- [ ] 动词原型恢复
- [ ] 指带消解

- [ ] 规则推理出来之后，还要考虑如何哪个链接的词加入到推理出来的链接指示词中
- [ ] Abstractive Summarizer, 挑选link组成完整的句子，调研一下相关工作

- [ ] 投稿EMNLP2021
    - 用到的数据集squad, newsqa
    - 特点
        - 主要引入时序信息，时序知识表示
        - 从文本中学到1）推理规则 2）时间的对应关系
        - 从文本中学到 「词义消歧」的方法
            - 苹果/微软/香蕉
        - 计算实体间的相似度
            - 链接类型、词之间的杰卡德相似度
        - 计算链接间的相似度
            - 实体（算上抽象的part-of实体）之间的相似度「？」
    - 1-1，1-N，N-1，N-N之间的关系
    - 模糊推理，有些conditions不满足也可以，只是满足了会增加置信度
    - 程雪琪 参考文献 62、63

- [ ] 适用于中文

- [ ] kind of 这类的noun snippet切分问题

- [ ] 当一个名词独立成为semantic node时，看看是否他已经被其他link抽取了，优先级最低

- [ ] 根据W-SLN来生成句子，检查语法

- [ ] our / own link



ACL 论文

{'redundant': 11463, 'sit, cond, temp, cause, means, pur to_node is same': 204, 'abstract redundant': 270, 'attr,sim,own all same': 27, 'as well as': 57, 'pur is complex': 15}
[({'d_r': 0, 'desired_length': 120, 'simplified_proportion': 0}, {'rouge-1': {'f': 28.03, 'r': 31.68, 'p': 26.46}, 'rouge-2': {'f': 4.44, 'r': 4.99, 'p': 4.21}, 'rouge-l': {'f': 23.09, 'r': 26.04, 'p': 21.83}}), ({'d_r': 0, 'desired_length': 120, 'simplified_proportion': 0.1}, {'rouge-1': {'f': 28.0, 'r': 31.66, 'p': 26.43}, 'rouge-2': {'f': 4.42, 'r': 4.98, 'p': 4.2}, 'rouge-l': {'f': 23.06, 'r': 26.02, 'p': 21.8}}), ({'d_r': 0, 'desired_length': 120, 'simplified_proportion': 0.2}, {'rouge-1': {'f': 28.02, 'r': 31.68, 'p': 26.45}, 'rouge-2': {'f': 4.43, 'r': 4.98, 'p': 4.2}, 'rouge-l': {'f': 23.07, 'r': 26.04, 'p': 21.81}}), ({'d_r': 0, 'desired_length': 150, 'simplified_proportion': 0}, {'rouge-1': {'f': 28.3, 'r': 32.82, 'p': 26.19}, 'rouge-2': {'f': 4.57, 'r': 5.28, 'p': 4.25}, 'rouge-l': {'f': 23.38, 'r': 27.08, 'p': 21.66}}), ({'d_r': 0, 'desired_length': 150, 'simplified_proportion': 0.1}, {'rouge-1': {'f': 28.44, 'r': 33.47, 'p': 26.0}, 'rouge-2': {'f': 4.64, 'r': 5.45, 'p': 4.26}, 'rouge-l': {'f': 23.54, 'r': 27.69, 'p': 21.55}}), ({'d_r': 0, 'desired_length': 150, 'simplified_proportion': 0.2}, {'rouge-1': {'f': 28.56, 'r': 33.94, 'p': 25.91}, 'rouge-2': {'f': 4.7, 'r': 5.56, 'p': 4.28}, 'rouge-l': {'f': 23.68, 'r': 28.11, 'p': 21.5}}), ({'d_r': 0.3, 'desired_length': 120, 'simplified_proportion': 0}, {'rouge-1': {'f': 28.78, 'r': 33.65, 'p': 26.47}, 'rouge-2': {'f': 4.84, 'r': 5.64, 'p': 4.47}, 'rouge-l': {'f': 23.93, 'r': 27.95, 'p': 22.03}}), ({'d_r': 0.3, 'desired_length': 120, 'simplified_proportion': 0.1}, {'rouge-1': {'f': 28.92, 'r': 33.41, 'p': 26.88}, 'rouge-2': {'f': 4.94, 'r': 5.69, 'p': 4.6}, 'rouge-l': {'f': 24.1, 'r': 27.81, 'p': 22.43}}), ({'d_r': 0.3, 'desired_length': 120, 'simplified_proportion': 0.2}, {'rouge-1': {'f': 29.04, 'r': 33.21, 'p': 27.21}, 'rouge-2': {'f': 5.02, 'r': 5.73, 'p': 4.71}, 'rouge-l': {'f': 24.25, 'r': 27.7, 'p': 22.75}}), ({'d_r': 0.3, 'desired_length': 150, 'simplified_proportion': 0}, {'rouge-1': {'f': 29.36, 'r': 33.68, 'p': 27.4}, 'rouge-2': {'f': 5.18, 'r': 5.95, 'p': 4.83}, 'rouge-l': {'f': 24.57, 'r': 28.17, 'p': 22.96}}), ({'d_r': 0.3, 'desired_length': 150, 'simplified_proportion': 0.1}, {'rouge-1': {'f': 29.64, 'r': 34.07, 'p': 27.58}, 'rouge-2': {'f': 5.32, 'r': 6.12, 'p': 4.94}, 'rouge-l': {'f': 24.87, 'r': 28.56, 'p': 23.17}}), ({'d_r': 0.3, 'desired_length': 150, 'simplified_proportion': 0.2}, {'rouge-1': {'f': 29.85, 'r': 34.38, 'p': 27.72}, 'rouge-2': {'f': 5.43, 'r': 6.27, 'p': 5.02}, 'rouge-l': {'f': 25.09, 'r': 28.87, 'p': 23.32}})]


500 CNN 新闻

{'redundant': 7722, 'attr,sim,own all same': 198, 'sit, cond, temp, cause, means, pur to_node is same': 1821, 'abstract redundant': 1125, 'pur is complex': 96, 'as well as': 78}

[({'d_r': 0, 'desired_length': 120, 'simplified_proportion': 0}, {'rouge-1': {'f': 24.63, 'r': 47.92, 'p': 16.78}, 'rouge-2': {'f': 7.51, 'r': 14.83, 'p': 5.09}, 'rouge-l': {'f': 22.13, 'r': 43.04, 'p': 15.07}}), ({'d_r': 0, 'desired_length': 120, 'simplified_proportion': 0.1}, {'rouge-1': {'f': 24.61, 'r': 47.9, 'p': 16.76}, 'rouge-2': {'f': 7.5, 'r': 14.82, 'p': 5.08}, 'rouge-l': {'f': 22.11, 'r': 43.02, 'p': 15.06}}), ({'d_r': 0, 'desired_length': 120, 'simplified_proportion': 0.2}, {'rouge-1': {'f': 24.63, 'r': 47.93, 'p': 16.78}, 'rouge-2': {'f': 7.51, 'r': 14.82, 'p': 5.09}, 'rouge-l': {'f': 22.13, 'r': 43.05, 'p': 15.07}}), ({'d_r': 0, 'desired_length': 150, 'simplified_proportion': 0}, {'rouge-1': {'f': 24.4, 'r': 49.25, 'p': 16.43}, 'rouge-2': {'f': 7.54, 'r': 15.48, 'p': 5.05}, 'rouge-l': {'f': 21.98, 'r': 44.38, 'p': 14.8}}), ({'d_r': 0, 'desired_length': 150, 'simplified_proportion': 0.1}, {'rouge-1': {'f': 24.27, 'r': 50.07, 'p': 16.23}, 'rouge-2': {'f': 7.57, 'r': 15.89, 'p': 5.03}, 'rouge-l': {'f': 21.91, 'r': 45.2, 'p': 14.65}}), ({'d_r': 0, 'desired_length': 150, 'simplified_proportion': 0.2}, {'rouge-1': {'f': 24.17, 'r': 50.57, 'p': 16.09}, 'rouge-2': {'f': 7.57, 'r': 16.13, 'p': 5.01}, 'rouge-l': {'f': 21.84, 'r': 45.7, 'p': 14.54}}), ({'d_r': 0.3, 'desired_length': 120, 'simplified_proportion': 0}, {'rouge-1': {'f': 24.23, 'r': 50.06, 'p': 16.2}, 'rouge-2': {'f': 7.58, 'r': 15.94, 'p': 5.04}, 'rouge-l': {'f': 21.91, 'r': 45.26, 'p': 14.64}}), ({'d_r': 0.3, 'desired_length': 120, 'simplified_proportion': 0.1}, {'rouge-1': {'f': 24.28, 'r': 49.68, 'p': 16.29}, 'rouge-2': {'f': 7.59, 'r': 15.81, 'p': 5.07}, 'rouge-l': {'f': 21.96, 'r': 44.94, 'p': 14.73}}), ({'d_r': 0.3, 'desired_length': 120, 'simplified_proportion': 0.2}, {'rouge-1': {'f': 24.32, 'r': 49.39, 'p': 16.36}, 'rouge-2': {'f': 7.6, 'r': 15.7, 'p': 5.08}, 'rouge-l': {'f': 22.0, 'r': 44.68, 'p': 14.79}}), ({'d_r': 0.3, 'desired_length': 150, 'simplified_proportion': 0}, {'rouge-1': {'f': 24.29, 'r': 49.72, 'p': 16.29}, 'rouge-2': {'f': 7.64, 'r': 15.93, 'p': 5.1}, 'rouge-l': {'f': 22.0, 'r': 45.05, 'p': 14.75}}), ({'d_r': 0.3, 'desired_length': 150, 'simplified_proportion': 0.1}, {'rouge-1': {'f': 24.26, 'r': 50.0, 'p': 16.23}, 'rouge-2': {'f': 7.68, 'r': 16.12, 'p': 5.11}, 'rouge-l': {'f': 21.99, 'r': 45.36, 'p': 14.71}}), ({'d_r': 0.3, 'desired_length': 150, 'simplified_proportion': 0.2}, {'rouge-1': {'f': 24.23, 'r': 50.23, 'p': 16.18}, 'rouge-2': {'f': 7.7, 'r': 16.28, 'p': 5.12}, 'rouge-l': {'f': 21.99, 'r': 45.62, 'p': 14.68}})]


500 legal case

{'redundant': 3461, 'sit, cond, temp, cause, means, pur to_node is same': 147, 'attr,sim,own all same': 34, 'abstract redundant': 68, 'pur is complex': 3, 'as well as': 4}

{'redundant': 45978, 'sit, cond, temp, cause, means, pur to_node is same': 1983, 'attr,sim,own all same': 462, 'abstract redundant': 912, 'pur is complex': 21, 'as well as': 39}
[({'d_r': 0, 'desired_length': 120, 'simplified_proportion': 0}, {'rouge-1': {'f': 19.09, 'r': 18.66, 'p': 40.32}, 'rouge-2': {'f': 3.91, 'r': 3.78, 'p': 8.82}, 'rouge-l': {'f': 17.54, 'r': 17.1, 'p': 37.29}}), ({'d_r': 0, 'desired_length': 120, 'simplified_proportion': 0.1}, {'rouge-1': {'f': 19.07, 'r': 18.68, 'p': 40.28}, 'rouge-2': {'f': 3.9, 'r': 3.78, 'p': 8.81}, 'rouge-l': {'f': 17.52, 'r': 17.12, 'p': 37.25}}), ({'d_r': 0, 'desired_length': 120, 'simplified_proportion': 0.2}, {'rouge-1': {'f': 19.07, 'r': 18.67, 'p': 40.3}, 'rouge-2': {'f': 3.9, 'r': 3.78, 'p': 8.82}, 'rouge-l': {'f': 17.52, 'r': 17.1, 'p': 37.27}}), ({'d_r': 0, 'desired_length': 150, 'simplified_proportion': 0}, {'rouge-1': {'f': 19.39, 'r': 19.2, 'p': 40.07}, 'rouge-2': {'f': 3.98, 'r': 3.9, 'p': 8.76}, 'rouge-l': {'f': 17.83, 'r': 17.61, 'p': 37.09}}), ({'d_r': 0, 'desired_length': 150, 'simplified_proportion': 0.1}, {'rouge-1': {'f': 19.58, 'r': 19.51, 'p': 39.95}, 'rouge-2': {'f': 4.02, 'r': 3.97, 'p': 8.72}, 'rouge-l': {'f': 18.02, 'r': 17.91, 'p': 36.99}}), ({'d_r': 0, 'desired_length': 150, 'simplified_proportion': 0.2}, {'rouge-1': {'f': 19.71, 'r': 19.72, 'p': 39.88}, 'rouge-2': {'f': 4.05, 'r': 4.02, 'p': 8.71}, 'rouge-l': {'f': 18.15, 'r': 18.11, 'p': 36.94}}), ({'d_r': 0.3, 'desired_length': 120, 'simplified_proportion': 0}, {'rouge-1': {'f': 19.6, 'r': 19.57, 'p': 40.11}, 'rouge-2': {'f': 4.08, 'r': 4.06, 'p': 8.87}, 'rouge-l': {'f': 18.06, 'r': 17.98, 'p': 37.17}}), ({'d_r': 0.3, 'desired_length': 120, 'simplified_proportion': 0.1}, {'rouge-1': {'f': 19.53, 'r': 19.46, 'p': 40.3}, 'rouge-2': {'f': 4.1, 'r': 4.08, 'p': 8.99}, 'rouge-l': {'f': 18.0, 'r': 17.88, 'p': 37.36}}), ({'d_r': 0.3, 'desired_length': 120, 'simplified_proportion': 0.2}, {'rouge-1': {'f': 19.47, 'r': 19.37, 'p': 40.43}, 'rouge-2': {'f': 4.12, 'r': 4.1, 'p': 9.09}, 'rouge-l': {'f': 17.95, 'r': 17.8, 'p': 37.49}}), ({'d_r': 0.3, 'desired_length': 150, 'simplified_proportion': 0}, {'rouge-1': {'f': 19.58, 'r': 19.53, 'p': 40.57}, 'rouge-2': {'f': 4.19, 'r': 4.2, 'p': 9.21}, 'rouge-l': {'f': 18.06, 'r': 17.96, 'p': 37.65}}), ({'d_r': 0.3, 'desired_length': 150, 'simplified_proportion': 0.1}, {'rouge-1': {'f': 19.66, 'r': 19.65, 'p': 40.63}, 'rouge-2': {'f': 4.25, 'r': 4.28, 'p': 9.3}, 'rouge-l': {'f': 18.14, 'r': 18.09, 'p': 37.73}}), ({'d_r': 0.3, 'desired_length': 150, 'simplified_proportion': 0.2}, {'rouge-1': {'f': 19.74, 'r': 19.76, 'p': 40.71}, 'rouge-2': {'f': 4.3, 'r': 4.35, 'p': 9.38}, 'rouge-l': {'f': 18.23, 'r': 18.2, 'p': 37.82}})]


TF:










{'summary': {<LinkType.ACTION: 1>: 2605, <LinkType.PURPOSE: 10>: 674, <LinkType.SITUATION: 6>: 1039, <LinkType.SEQUENTIAL: 4>: 661, <LinkType.OWN: 13>: 611, <LinkType.ATTRIBUTE: 2>: 508, <LinkType.CONJ_OR: 5.5>: 58, <LinkType.ABSTRACT: 9>: 2821, <LinkType.MEANS: 12>: 311, <LinkType.CONJ_AND: 5>: 441, <LinkType.CAUSE_EFFECT: 8>: 26, <LinkType.CONDITION: 7>: 34, <LinkType.NEGATIVE: 3>: 23, <LinkType.SIMILAR: 11>: 8}, 'text': {<LinkType.CONJ_AND: 5>: 14837, <LinkType.SITUATION: 6>: 32417, <LinkType.ACTION: 1>: 82006, <LinkType.ATTRIBUTE: 2>: 18946, <LinkType.OWN: 13>: 21015, <LinkType.SEQUENTIAL: 4>: 39931, <LinkType.PURPOSE: 10>: 19605, <LinkType.ABSTRACT: 9>: 77804, <LinkType.CONDITION: 7>: 1456, <LinkType.MEANS: 12>: 10304, <LinkType.NEGATIVE: 3>: 650, <LinkType.CONJ_OR: 5.5>: 2794, <LinkType.CAUSE_EFFECT: 8>: 1170, <LinkType.SIMILAR: 11>: 251}}
cnn-corpus: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 5443/5443 [00:00<00:00, 8311.23it/s]
{'summary': {<LinkType.SEQUENTIAL: 4>: 10655, <LinkType.ACTION: 1>: 34674, <LinkType.ATTRIBUTE: 2>: 4147, <LinkType.ABSTRACT: 9>: 22363, <LinkType.SITUATION: 6>: 10477, <LinkType.PURPOSE: 10>: 7246, <LinkType.OWN: 13>: 7993, <LinkType.CONJ_AND: 5>: 2356, <LinkType.MEANS: 12>: 2321, <LinkType.CONJ_OR: 5.5>: 498, <LinkType.CAUSE_EFFECT: 8>: 326, <LinkType.CONDITION: 7>: 247, <LinkType.NEGATIVE: 3>: 275, <LinkType.SIMILAR: 11>: 125}, 'text': {<LinkType.SITUATION: 6>: 177646, <LinkType.ACTION: 1>: 493618, <LinkType.OWN: 13>: 120981, <LinkType.SEQUENTIAL: 4>: 194010, <LinkType.CONJ_AND: 5>: 76198, <LinkType.ABSTRACT: 9>: 335951, <LinkType.MEANS: 12>: 36310, <LinkType.PURPOSE: 10>: 110758, <LinkType.ATTRIBUTE: 2>: 75659, <LinkType.SIMILAR: 11>: 3575, <LinkType.CONDITION: 7>: 7928, <LinkType.CONJ_OR: 5.5>: 15905, <LinkType.CAUSE_EFFECT: 8>: 6973, <LinkType.NEGATIVE: 3>: 4234}}

# badcase

- [x] Jack John hate you 句子有bug
- [ ] See the call for papers for further important details about the submission process
    - 缺少call-see->call链接
- [ ] I love you because of your beauty
- [ ] I love and hit your dog

- [ ] your beauty
- [ ] neuralcoref
- [ ] 

- [ ]         {
            "type": "instance",
            "patterns": [
                {
                    "pattern": "N1 BE I(a) N2",
                    "from_id": "N1",
                    "indicator": "I",
                    "to_id": "N2"
                }
            ]
        },

# DONE

- [x] 标点符号解决

## 一些时间的思考

### 周期性的时间

* morning, Monday算是周期性的时间词，每天、每周都会有的，只不过last morning是yesterday的morning，应该不算是基准时间，而是一种周期时间
* first day, first month并不能成为一月，一号的标准，只是作为修饰符号，后面用推理手段找
    * It's my first day to work.
    * I will go to work in 14th day of January.
    * 如果是现在完成时+morning就不是周期
    * I work in the morning. 默认是周期
    * I work in this morning.
    * I will work in next morning.
    * I will work in morning. 周期


# NLTK pos tag

CC 连词 and, or,but, if, while,although
CD 数词 twenty-four, fourth, 1991,14:24
DT 限定词 the, a, some, most,every, no
EX 存在量词 there, there's
FW 外来词 dolce, ersatz, esprit, quo,maitre
IN 介词连词 on, of,at, with,by,into, under
JJ 形容词 new,good, high, special, big, local
JJR 比较级词语 bleaker braver breezier briefer brighter brisker
JJS 最高级词语 calmest cheapest choicest classiest cleanest clearest
LS 标记 A A. B B. C C. D E F First G H I J K
MD 情态动词 can cannot could couldn't
NN 名词 year,home, costs, time, education
NNS 名词复数 undergraduates scotches
NNP 专有名词 Alison,Africa,April,Washington
NNPS 专有名词复数 Americans Americas Amharas Amityvilles
PDT 前限定词 all both half many
POS 所有格标记 ' 's
PRP 人称代词 hers herself him himself hisself
PRP$ 所有格 her his mine my our ours
RB 副词 occasionally unabatingly maddeningly
RBR 副词比较级 further gloomier grander
RBS 副词最高级 best biggest bluntest earliest
RP 虚词 aboard about across along apart
SYM 符号 % & ' '' ''. ) )
TO 词to to
UH 感叹词 Goodbye Goody Gosh Wow
VB 动词 ask assemble assess
VBD 动词过去式 dipped pleaded swiped
VBG 动词现在分词 telegraphing stirring focusing
VBN 动词过去分词 multihulled dilapidated aerosolized
VBP 动词现在式非第三人称时态 predominate wrap resort sue
VBZ 动词现在式第三人称时态 bases reconstructs marks
WDT Wh限定词 who,which,when,what,where,how
WP WH代词 that what whatever
WP$ WH代词所有格 whose
WRB WH副词


===========after 37 texts =====
only rank rouge-1 f:  0.3204422438004861
only simplified rouge-1 f:  0.32289774592459525
only adjust rouge-1 f:  0.31758280678527695
simplified + adjust rouge-1 f:  0.31945951161835
only rank rouge-1 p:  0.27013281466385064
only simplified rouge-1 p:  0.2744362383070383
only adjust rouge-1 p:  0.26905776530865094
simplified + adjust rouge-1 p:  0.2708465803078671
only rank rouge-1 r:  0.41648730115947125
only simplified rouge-1 r:  0.41430129190803966
only adjust rouge-1 r:  0.40925810318111777
simplified + adjust rouge-1 r:  0.4094198159087048
only rank rouge-2 f:  0.0775734375987485
only simplified rouge-2 f:  0.07246249998668594
only adjust rouge-2 f:  0.07727438390874337
simplified + adjust rouge-2 f:  0.0729512285244575
only rank rouge-2 p:  0.06445480241624334
only simplified rouge-2 p:  0.061086592562278524
only adjust rouge-2 p:  0.06445487122735902
simplified + adjust rouge-2 p:  0.06106292781969101
only rank rouge-2 r:  0.10338417623374582
only simplified rouge-2 r:  0.09418332395102662
only adjust rouge-2 r:  0.10275255833617453
simplified + adjust rouge-2 r:  0.09598499196277437
only rank rouge-l f:  0.27089594126067296
only simplified rouge-l f:  0.2733452980423118
only adjust rouge-l f:  0.2713839817809443
simplified + adjust rouge-l f:  0.273718600898758
only rank rouge-l p:  0.23596295233361156
only simplified rouge-l p:  0.2387663316939823
only adjust rouge-l p:  0.23945165665898294
simplified + adjust rouge-l p:  0.2410054702361848
only rank rouge-l r:  0.33238508184593635
only simplified rouge-l r:  0.3335665911836341
only adjust rouge-l r:  0.32544615137302785
simplified + adjust rouge-l r:  0.3282505012695482