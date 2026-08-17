import type { BirthdayInfo, BirthdayMessage } from "../types";

// ✏️ 前端可替换配置：即使不启动后端，也能用这份数据先预览。
export const FALLBACK_BIRTHDAY_INFO: BirthdayInfo = {
  recipientName: "廖思覃",
  birthdayDate: "8月17日",
  heroTitle: "廖思覃，生日快乐",
  blessingTitle: "给新一岁的你",
  blessingText: "愿你的每一天，都有微小的惊喜在等着你。",
  cardSalutation: "亲爱的廖思覃",
  cardMessage: "叮！按时长大！愿你新的一岁暴富暴美，快乐加倍！",
  musicUrl: "/Christina Perri - A Thousand Years.mp3",
};

// ✏️ 首页祝福段落会按顺序逐条显现。
export const BLESSING_LINES: string[] = [
  "新的一岁，不必急着成为谁。",
  "你可以继续好奇、继续发亮，也可以偶尔停下来。",
  "愿你被爱意稳稳接住，也拥有奔赴远方的勇气。",
  "生日快乐，亲爱的朋友。",
];

// ✏️ 相册照片：src 留空时会显示内置渐变占位图，也可以替换为本地或远程图片。
export interface PhotoItem {
  src: string;
  date: string;
  caption: string;
  gradient: [string, string];
  alt: string;
}

export const PHOTO_ITEMS: PhotoItem[] = [
  {
    src: "",
    date: "2022 / 08",
    caption: "那天的风刚刚好",
    gradient: ["#f3a0b8", "#7b5ea7"],
    alt: "回忆一",
  },
  {
    src: "",
    date: "2023 / 08",
    caption: "愿望是继续做小朋友",
    gradient: ["#e8bf6a", "#d16f8a"],
    alt: "回忆二",
  },
  {
    src: "",
    date: "2024 / 08",
    caption: "夏天和你的笑声",
    gradient: ["#7bd2c7", "#405f8d"],
    alt: "回忆三",
  },
  {
    src: "",
    date: "2025 / 08",
    caption: "一起走过更远的路",
    gradient: ["#b8a4e8", "#3b3d68"],
    alt: "回忆四",
  },
];

// ✏️ 后端不可用时的本地留言数据。当前已清空，留言墙从空状态开始。
export const FALLBACK_MESSAGES: BirthdayMessage[] = [];

// ✏️ 留言墙之后显示的一封信，可按需修改标题、称呼、段落、落款和署名。
export const LETTER_CONTENT = {
  greeting: "T0.廖",
  paragraphs: [
    "展信安。其实很少认认真真，坐下来给你写段话。我们之间，好像向来都是随口聊聊、有事直说，不擅长说太多煽情的话。",
    "可越长大越觉得，能有一个你这样的朋友，真的很珍贵。我们没有什么轰轰烈烈的经历，但总是可以给我带来快乐、化解烦恼。不用刻意讨好，不用小心翼翼，不用在对方面前假装坚强。",
    "很多人关心你飞得高不高、走得远不远，而我只希望你，别太累，别太苦，别什么事都自己硬扛。",
    "我们会各自忙碌，各自奔赴自己的人生，会有很长一段时间不常联系、不见面。但我从来没担心过，我们不会因此走散。真正的朋友，从不是天天黏在一起，而是心里一直有位置，久不联络也不会陌生。",
    "我不会说太多漂亮的祝福，只愿你接下来的路：",
    "“平安顺遂，少些波折，做自己喜欢的事，成为自己想成为的人，不必迎合谁，也不必勉强自己。”",
  ],
  closing: "人生这条路，风雨很多，幸好有你。\n不必时刻相伴，只要岁岁平安。\n仅此而已，足矣。",
  signature: "你的朋友\n徐浚函",
};
